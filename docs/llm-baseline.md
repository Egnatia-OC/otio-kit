# Task 0.4 — LLM baseline: can a model write the spec from the brief?

**Date:** 2026-09-15 (day 1). **Method:** the 0.2 specimen brief
(`specimen/brief.md`) + the spec v0 JSON Schema → model → spec YAML →
`otio-kit compile` → diff against the hand-authored golden timeline
(`tests/golden/specimen60.golden.otio`).

**Gate metric (plan):** a cut point *matches* if within ±2 frames of a
hand-authored boundary; **match rate = matched ÷ hand-authored cuts**;
≥ 90% with correct track structure ⇒ the hero flow ships **full-gen**.
Below ⇒ **template-first**. The review step ships either way.

**Harness:** [`bench/llm_baseline.py`](../bench/llm_baseline.py). Temperature 0,
single run per model, Ollama `generate` API. One recorded normalisation: media
paths in the model's YAML are re-pointed by basename onto the local DNxHR
fixtures — file resolution is not the skill under test; cut-point fidelity is.

## Results

| Model | Compile | Match rate | Structure | Wall | Tokens (in/out) | Gate |
|---|---|---|---|---|---|---|
| qwen3.8:27b (local, Ollama, RTX 3090) | ✅ ok | **1.00 (5/5)** | ✅ match | 30.3 s | 1,626 / 2,265 | **FULL-GEN** |
| qwen3:0.6b (control) | ❌ invalid YAML | n/a | ❌ | 18.1 s | 1,516 / 528 | template-first |

Cost: local inference — no API spend. Cloud-model row pending (same harness,
OpenAI-compatible endpoint).

## The 27B output, verbatim

The model's emitted spec — note the dissolve placed *between* shots 1 and 2
only, the 5 s title, the 2 s fade on the music bed, and both markers with
correct names and colors:

```yaml
spec_version: 0
name: "Specimen 60"
fps: 24
media:
  clip_a: media/clip_a.mp4
  clip_b: media/clip_b.mp4
  clip_c: media/clip_c.mp4
  title: media/title.png
  music: media/music.m4a
timeline:
  video:
    - track: V1
      clips:
        - media: clip_a
          duration: 20
        - media: clip_b
          duration: 20
          transition_in:
            type: dissolve
            duration: 1
        - media: clip_c
          duration: 20
    - track: V2
      clips:
        - media: title
          duration: 5
  audio:
    - track: A1
      clips:
        - media: music
          duration: 60
          fade_in: 2
markers:
  - time: 10
    color: blue
    name: beat-1
  - time: 45
    color: red
    name: outro
```

## Decision

**Gate passed → the hero flow ships full-gen** (with a competent model;
`spec_version` pinning + validation + the review step are the guardrails).
The 0.6B control confirms the gate discriminates: weak models cannot emit
valid v0 YAML unaided — exactly the case the template-first mode exists for.

## Caveats (recorded, not hidden)

- Single sample per model at temperature 0. The full-gen call is for the
  specimen class of brief (well-structured prose, explicit timings). Messier
  real-world briefs are the next benchmark, not this one.
- Cut-point metric counts clip starts per track (5 total: 0/480/960 on V1,
  0 on V2, 0 on A1 @24 fps). Transition placement and marker semantics were
  additionally confirmed present in the compiled output.
- Media-path normalisation was applied (see harness header).
