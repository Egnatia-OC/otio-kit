# Spec v0 — scope

Scope frozen 2026-09-15 from the task 0.2 safe-set on **Resolve Free 21.1,
Linux** (see `docs/fidelity-log.md` for the full evidence). Everything v0 emits
is stock OTIO schema; custom semantics travel in `metadata`.

## What v0 covers

| Feature | Spec field | Import behaviour on Free 21.1 Linux |
|---|---|---|
| Timeline name, fps | `name`, `fps` | exact |
| Tracks (video + audio, declared order) | `timeline.video[]`, `timeline.audio[]` | exact |
| Sequential clips with exact durations | `clips[].media`, `clips[].duration` | frame-exact boundaries |
| Cross-dissolve between adjacent clips | `clips[].transition_in` (SMPTE_Dissolve, half-half offsets) | present, plays |
| Still images on upper tracks | media map pointing at images | full duration honored |
| Markers (8 stock colors) | `markers[].time/color/name` | clip-local; blue confirmed on import |
| Media manifest | `media` map, relative to the spec file | compile-time existence check; missing media = loud failure |

**Frame quantization.** Durations are quantized to whole frames per clip
(`round(duration × fps)`); the timeline's length is the sum of the quantized
clips. At fractional fps (23.976, 29.97) the total may differ from the
nominal duration by a few frames — that is the model, not drift to correct.
Durations that round to 0 frames are rejected by the emitter (loud error);
minimum clip is 1 frame, minimum transition 2 frames.

## What v0 deliberately excludes

| Excluded | Why |
|---|---|
| Effects, Fusion comps, grades | Applied natively in Resolve after import; no OTIO fidelity evidence — post-import step, per plan |
| Gaps / offset placement (`start`) | v0 is sequential; safe-set evidence covers back-to-back clips |
| Speed changes, retiming | No import evidence; risk of silent misinterpretation |
| Custom effect schemas | **Fatal** on 21.1 Linux import and in `opentimelineio` itself (`AudioFadeIn_1` case) |
| Bare relative media URLs | Linux conform misresolves them; emitter always writes existing absolute paths |
| AAC-only music audibility | Free Linux cannot decode AAC (record) — ship audio as PCM/WAV-class containers (music.m4a unverified; open item) |
| Audio fade-in (applied in Resolve) | Unverified — the test machine has no audio path (no sound card). The emitter records the *intent* as a stock `Effect` named `AudioFadeIn` with parameters in `metadata.cutlist` for downstream tools; it is **not** an applied fade |

## Versioning rules

- `spec_version: 0` is frozen until a fidelity run on a new Resolve release
  proves a feature safe to add. Additions increment minor, never mutate.
- Every claim in this file cites the fidelity log; no speculation shipped.
