# Task 0.4 — LLM baseline: full-gen vs template-first

Per plan: "LLM baseline test: feed the brief to one Ollama-local + one cloud
API, measure cut-point accuracy vs the hand-authored golden. Record models,
prompts, diffs, costs. Gate: >=90% cut points within +/-2 frames and correct
track structure → full-gen; else template-first."

**Completed day 1 (2026-09-15): gate PASSED on local hardware and on two cloud
models. All capable models pass full-gen; the sub-1B control fails, confirming
the gate discriminates. Verdict: full-gen with a mandatory human review step;
template-first as fallback for weak models and messy briefs.**

## Method

- Harness: `bench/llm_baseline.py` (committed, re-runnable).
- Input: the same brief as the golden (`specimen/brief.md`) + the spec v0 JSON
  schema, at temperature 0, single sample per model.
- Pipeline: model output → extract YAML → **media-path normalisation** (see
  below) → `load_spec` → `resolve_media` → `emit` → diff vs golden.
- Metric: per track, clip start times (frames at 24 fps); a golden cut point
  matches if an emitted one lands within ±2 frames. Transitions consume no
  track time (matches the verified Resolve display).
- Gate: match rate ≥ 90% AND identical track structure (names + kinds) →
  full-gen; otherwise template-first.

### Media-path normalisation (recorded, benign)

Models emit the brief's relative media names (`media/clip_a.mp4`). The harness
re-points each media key by basename onto the local DNxHR fixture with an
absolute path before compiling. Media resolution is not the skill under test —
the emitter's job is to place what it is given; the skill measured is
cut-point fidelity from a prose brief. (In production the same normalisation is
what media-resolution is *for*.)

## Results

| Model | Provider | Compile | Cuts matched | Structure | Gate | Wall | Tokens (in/out) | Cost/brief |
|---|---|---|---|---|---|---|---|---|
| qwen3.8:27b | Ollama, local (RTX 3090) | ok | 5/5 (100%) | match | **full-gen** | 30.3 s | 1,626 / 2,265 | $0 |
| **GLM-5.3-Flash** | cloud (Z.ai) | ok | 5/5 (100%) | match | **full-gen** | 32.2 s | 1,480 / 1,354 (incl. 1,123 reasoning) | ~$0.0009 |
| **MiniMax-M2.7** | cloud (MiniMax) | ok | 5/5 (100%) | match | **full-gen** | 44.8 s | 1,490 / 2,775 | ~$0.0038 |
| qwen3:0.6b | Ollama, local (control) | FAILED (invalid YAML — indentation collapse) | — | — | template-first | 18.1 s | 1,516 / 528 | $0 |

Costs from measured token counts × official list prices
(docs.z.ai, 2026-09-15: GLM-5.3-Flash $0.15/$0.50 per M; MiniMax docs:
M2.7 $0.30/$1.20 per M). **A full timeline compile costs a fraction of a
cent per brief** — the per-render LLM tax the pricing rules forbid is
structurally tiny; the real cost driver is human review time.

## Per-model notes

- **qwen3.8:27b (local)**: first run produced a perfect spec — all five cut
  points exact, dissolve only between shots 1–2, 5 s title, 2 s fade, both
  markers with names and colors. Verbatim YAML below.
- **GLM-5.3-Flash (Z.ai coding endpoint)**: perfect spec, first try. Hybrid
  reasoner: 1,123 of its 1,354 output tokens were thinking; final answer was
  clean, fence-free YAML. 32 s wall includes API round-trip.
- **MiniMax-M2.7**: perfect spec once configured correctly. API quirk (not a
  model failure): without `reasoning_split: true` its thinking consumed the
  4,096-token budget and returned empty `content`; with the split flag and a
  16k budget it finished with `finish_reason: stop` and clean YAML in 45 s.
- **qwen3:0.6b (control)**: YAML indentation collapsed ("could not find
  expected ':'"). Expected for a sub-1B model; proves the gate separates
  capable from incapable rather than rubber-stamping.

## qwen3.8:27b emitted YAML (verbatim)

```yaml
name: specimen-60
spec_version: 0
fps: 24
output_duration: 60
tracks:
  - name: V1
    kind: video
    clips:
      - media: clip_a
        duration: 20
        transition_in:
          type: dissolve
          duration: 1
      - media: clip_b
        duration: 20
      - media: clip_c
        duration: 20
  - name: V2
    kind: video
    clips:
      - media: title
        start: 0
        duration: 5
  - name: A1
    kind: audio
    clips:
      - media: music
        start: 0
        duration: 60
        fade_in: 2
media:
  clip_a: media/clip_a.mp4
  clip_b: media/clip_b.mp4
  clip_c: media/clip_c.mp4
  title: media/title.png
  music: media/music.m4a
markers:
  - time: 10
    label: beat-1
    color: blue
  - time: 45
    label: outro
    color: red
```

## Verdict (feeds day-7 strike + product design)

- **Full-gen is the hero flow**, with a mandatory human review step on every
  compile (per plan; also the palatability line — the AI never drives the
  NLE, humans approve).
- **Template-first** is the documented fallback: weak/local models, messy
  real-world briefs, or any compile that fails the emitter's loud errors.
- **Cost**: sub-cent per compile even on paid cloud; local is $0. The pricing
  rules (no per-render LLM tax) hold — this is a flat, negligible input cost.
- The specimen brief is "specimen-class" (well-structured prose, explicit
  timings). Messier real-world briefs are the next benchmark; the review step
  is the safety net that makes full-gen safe even when the model stumbles.

## Caveats

- Single sample per model at temperature 0 (per plan scope); production will
  add retries and a schema-repair pass.
- Cloud rows ran through the standard API endpoints (Z.ai coding endpoint for
  GLM; MiniMax `chatcompletion_v2` with `reasoning_split` for M2.7).
- Metric counts clip starts per track (5 total on the specimen). A richer
  metric (transitions, fades, markers) is a follow-up; structure equality and
  the compile gate already cover most of it.
