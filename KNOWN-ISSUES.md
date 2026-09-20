# Known issues

Open items and known limitations. Fidelity open items (per-Resolve-release)
also live in `docs/fidelity-log.md`; this file is the defect/limitation log.

## Unverified platforms

- **macOS Free: unverified** — the second open item. **Windows Free 21.1
  is now verified** (2026-09-20, independent control run on 21.1.0.0017;
  H.264 kit specimen, stock-fade build — `docs/fidelity-registry.md`).
  Linux Free 21.1 (21.1.0.0017) remains the hardest target (no H.264
  decode).
- **20.3 / 21.0 comparison column** — planned, not tested; no speculation
  shipped about pre-21.1 behavior.

## Resolved: empty-timeline OTIO imports (2026-09-20)

The original H.264 kit specimen imported as an **empty timeline with no
dialog** on Windows 21.1.0.0014 (first control run) and 21.1.0.0017
(retest). Cause: the kit shipped a custom `AudioFadeIn_1` effect schema,
which Resolve's OTIO importer treats as fatal
(`Import Log (Fatal) - failed to import OTIO timeline`) — the same failure
first documented on Linux (`docs/fidelity-log.md`, root cause #2). The kit
was rebuilt with the stock `Effect.1` representation and imported cleanly
on 21.1.0.0017 (registry, 2026-09-20 row). Not a platform or build issue;
no evidence implicates the .0014 importer.

## Audio

- **Audio is structurally unverified on the test machine** — no sound card:
  PCM tones are verified in the files; in-Resolve metering/audibility is an
  open item (fidelity log).
- **Audio fade-in is intent metadata, not an applied fade** — unverified on
  import (no audio path on the test machine). See
  `docs/spec-scope-v0.md` (excluded table).
- **AAC-only music (music.m4a)** — expected silent on Free Linux (H.264/H.265
  and AAC decode is Studio+NVIDIA-only there). Ship PCM/WAV-class audio.

## Evidence

- **Matrix screenshots** (`t1-menu.xwd`, `t2-console.xwd`) — captured
  2026-09-15, not preserved (host `/tmp` cleared); re-capture pending.
- **LLM baseline** — single sample per model at temperature 0, on a
  well-structured brief; real-world briefs are messier (retry + schema-repair
  pass is the next engineering item).

## Documented model behaviour (not bugs)

- **Frame quantization** — durations are quantized per clip
  (`round(duration × fps)`); at fractional fps (23.976, 29.97) the total may
  differ from the nominal duration by a few frames. See
  `docs/spec-scope-v0.md`.
- **Committed test media are empty stubs** — the golden suite proves emitter
  determinism, not import fidelity (that is the Resolve import run in
  `docs/fidelity-log.md`). Regenerate the real specimen media from the recipe
  in `specimen/BUILD.md` (ffmpeg + DNxHR transcode + `make_title.py`);
  `build_specimen.py` assembles the timeline only.
