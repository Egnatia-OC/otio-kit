"""Task 0.4 LLM baseline harness.

Feeds the specimen brief to an LLM, expects spec v0 YAML, compiles it with the
otio-kit emitter, and diffs against the hand-authored golden timeline.

Gate metric (per plan): a cut point matches if it lands within +/-2 frames of a
hand-authored boundary; match rate = matched / hand-authored cuts. >= 90% with
correct track structure -> full-gen; else template-first.

Known-benign normalisation (recorded in docs/llm-baseline.md): media paths in
the model's output are re-pointed by basename onto the local DNxHR fixtures.
Media resolution is not the skill under test; cut-point fidelity is.

Providers: ollama (local) | cloud (OpenAI-compatible chat completions:
GLM/Z.ai, MiniMax).
"""

import argparse
import json
import pathlib
import re
import sys
import tempfile
import time
import urllib.request

REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "core"))

from otio_kit.emit_otio import EmitError, emit, write_otio
from otio_kit.media import MediaMissingError, resolve_media
from otio_kit.spec import SpecError, load_spec

SYSTEM = (
    "You are a timeline compiler. Read the editing brief and output ONLY a "
    "YAML document that validates against the provided JSON Schema. No prose, "
    "no code fences, no explanation. Durations are seconds. Track names and "
    "media keys are given by the brief; invent nothing beyond the brief."
)


def ollama_generate(base_url: str, model: str, prompt: str, num_ctx: int = 8192):
    body = json.dumps({
        "model": model,
        "system": SYSTEM,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0, "num_ctx": num_ctx},
    }).encode()
    req = urllib.request.Request(
        f"{base_url}/api/generate", data=body,
        headers={"Content-Type": "application/json"},
    )
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=1800) as resp:
        payload = json.loads(resp.read())
    wall = time.time() - t0
    return payload.get("response", ""), {
        "wall_s": round(wall, 2),
        "prompt_tokens": payload.get("prompt_eval_count", 0),
        "output_tokens": payload.get("eval_count", 0),
        "eval_s": round(payload.get("eval_duration", 0) / 1e9, 2),
    }


def cloud_generate(base_url: str, api_path: str, model: str, api_key: str,
                   prompt: str, max_tokens: int = 4096, extra=None):
    """OpenAI-compatible chat completions (GLM/Z.ai, MiniMax)."""
    body_dict = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0,
        "max_tokens": max_tokens,
        "stream": False,
    }
    if extra:
        body_dict.update(extra)
    body = json.dumps(body_dict).encode()
    req = urllib.request.Request(
        base_url.rstrip("/") + api_path, data=body,
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {api_key}"},
    )
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=900) as resp:
        payload = json.loads(resp.read())
    wall = time.time() - t0
    message = payload["choices"][0]["message"]
    text = message.get("content") or ""
    usage = payload.get("usage", {})
    details = usage.get("completion_tokens_details") or {}
    return text, {
        "wall_s": round(wall, 2),
        "prompt_tokens": usage.get("prompt_tokens", 0),
        "output_tokens": usage.get("completion_tokens", 0),
        "reasoning_tokens": details.get("reasoning_tokens", 0),
        "finish_reason": payload["choices"][0].get("finish_reason"),
    }


def extract_yaml(text: str) -> str:
    fence = re.search(r"```(?:ya?ml)?\s*\n(.*?)```", text, re.DOTALL)
    if fence:
        return fence.group(1).strip()
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if re.match(r"^\s*(spec_version|name|fps)\s*:", line):
            return "\n".join(lines[i:]).strip()
    return text.strip()


def normalize_media(yaml_text: str, fixture_dir: pathlib.Path) -> str:
    """Point every media value at the local DNxHR fixture (absolute path)."""
    fixes = {
        "clip_a": "clip_a_dnx.mov", "clip_b": "clip_b_dnx.mov",
        "clip_c": "clip_c_dnx.mov", "title": "title.png", "music": "music.m4a",
    }
    out = []
    in_media = False
    for line in yaml_text.splitlines():
        if re.match(r"^media\s*:", line):
            in_media = True
            out.append(line)
            continue
        if in_media:
            m = re.match(r"^(\s+)([\w.-]+)\s*:\s*(\S+)\s*$", line)
            if m and m.group(2) in fixes:
                abs_path = fixture_dir / "media" / fixes[m.group(2)]
                line = f"{m.group(1)}{m.group(2)}: {abs_path}"
            elif line and not line[0].isspace():
                in_media = False
        out.append(line)
    return "\n".join(out) + "\n"


def collect_cuts(tl_json: dict, fps: int = 24):
    """Clip start times in frames (cumulative clip durations; transitions
    consume no track time — matches how Resolve displayed the golden file)."""
    cuts = {}
    for track in tl_json["tracks"]["children"]:
        name = track["name"]
        t = 0.0
        points = []
        for child in track["children"]:
            if child["OTIO_SCHEMA"].startswith("Clip"):
                points.append(round(t * fps))
                rt = child["source_range"]["duration"]
                t += rt["value"] / rt["rate"]
        cuts[name] = points
    return cuts


def diff_metrics(golden_json: dict, out_json: dict, fps: int = 24, tol: int = 2):
    g_cuts = collect_cuts(golden_json, fps)
    o_cuts = collect_cuts(out_json, fps)
    total = matched = 0
    per_track = {}
    for tname, gpts in g_cuts.items():
        opts = o_cuts.get(tname, [])
        ok = sum(1 for gp in gpts if any(abs(gp - op) <= tol for op in opts))
        total += len(gpts)
        matched += ok
        per_track[tname] = {"golden": gpts, "emitted": opts, "matched": ok}
    g_tracks = [(t["name"], t["kind"]) for t in golden_json["tracks"]["children"]]
    o_tracks = [(t["name"], t["kind"]) for t in out_json["tracks"]["children"]]
    return {
        "match_rate": round(matched / total, 4) if total else 0.0,
        "matched": matched,
        "hand_authored_cuts": total,
        "track_structure_match": g_tracks == o_tracks,
        "per_track": per_track,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--provider", choices=["ollama", "cloud"], default="ollama")
    ap.add_argument("--base-url", default="http://127.0.0.1:11434")
    ap.add_argument("--api-path", default="/chat/completions",
                    help="cloud: path appended to base URL "
                         "(MiniMax: /text/chatcompletion_v2)")
    ap.add_argument("--api-key-env", default="API_KEY",
                    help="cloud: env var holding the API key")
    ap.add_argument("--max-tokens", type=int, default=4096)
    ap.add_argument("--extra-body", default="",
                    help="cloud: JSON merged into the request body "
                         '(e.g. \'{"reasoning_split": true}\')')
    ap.add_argument("--brief",
                    default="/home/oc/tmp/resources/research/cutlist-p0/specimen/brief.md")
    ap.add_argument("--out", default=None, help="write result JSON here")
    ap.add_argument("--num-ctx", type=int, default=8192)
    args = ap.parse_args()

    brief = pathlib.Path(args.brief).read_text(encoding="utf-8")
    schema = (REPO / "core" / "otio_kit" / "schema" / "spec-v0.schema.json").read_text()
    golden = json.loads((REPO / "tests" / "golden" / "specimen60.golden.otio").read_text())
    fixture_dir = REPO / "tests" / "golden"

    prompt = (
        f"# JSON Schema (spec v0)\n{schema}\n\n"
        f"# Editing brief\n{brief}\n\n"
        "Output the YAML document now. Remember: no prose, no fences."
    )

    if args.provider == "cloud":
        import os
        key = os.environ.get(args.api_key_env)
        if not key:
            print(f"error: env var {args.api_key_env} is not set", file=sys.stderr)
            return 2
        extra = json.loads(args.extra_body) if args.extra_body else None
        text, usage = cloud_generate(args.base_url, args.api_path, args.model,
                                     key, prompt, args.max_tokens, extra)
    else:
        text, usage = ollama_generate(args.base_url, args.model, prompt, args.num_ctx)

    yaml_text = extract_yaml(text)
    normalized = normalize_media(yaml_text, fixture_dir)

    result = {
        "model": args.model,
        "provider": args.provider,
        "usage": usage,
        "raw_response_chars": len(text),
        "yaml_extracted": bool(yaml_text),
    }

    spec_path = pathlib.Path(tempfile.gettempdir()) / f"llm-spec-{int(time.time())}.yaml"
    spec_path.write_text(normalized)
    try:
        spec = load_spec(spec_path)
        media = resolve_media(spec)
        timeline = emit(spec, media)
        out_otio = pathlib.Path(tempfile.gettempdir()) / "llm-out.otio"
        write_otio(timeline, out_otio)
        out_json = json.loads(out_otio.read_text())
        result["compile"] = "ok"
        result["diff"] = diff_metrics(golden, out_json)
        result["gate"] = (
            "full-gen" if result["diff"]["match_rate"] >= 0.9
            and result["diff"]["track_structure_match"] else "template-first"
        )
    except (SpecError, MediaMissingError, EmitError) as exc:
        result["compile"] = f"failed: {exc}"
        result["gate"] = "template-first (compile failed)"

    result["emitted_yaml"] = yaml_text
    print(json.dumps(result, indent=1))
    if args.out:
        pathlib.Path(args.out).write_text(json.dumps(result, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
