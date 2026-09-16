# Specimen build — reproduction

Deterministic build of the task-0.2 fidelity specimen (no LLM involved).

This directory is the **recipe**, not the artefacts. `build_specimen.py`
assembles the OTIO timeline and `make_title.py` renders the title still; the
media and the timeline are *generated on demand* and are **not checked in**
(the repo carries 0-byte stubs under `tests/golden/media/` for the golden test
only). Run the steps below on a clean checkout to regenerate everything.

## Two variants — and which one is the evidence

The fidelity log's acceptance rests on the **DNxHR** variant, because H.264
does not decode on Resolve Free Linux:

| variant | media | Free-Linux import | role |
|---|---|---|---|
| `specimen-60.otio` (default, relative `media/` paths) | H.264/AAC `.mp4` | audio-only, no picture | demonstrates the codec gap |
| `specimen-60-dnx.otio` | DNxHR SQ + PCM `.mov` | clean, full picture | the load-bearing evidence |

`build_specimen.py` writes the H.264 variant. The DNxHR variant is the same
timeline re-pointed at the DNxHR media (absolute paths on the build host); the
import result is in `docs/fidelity-log.md`.

## Environment

```
uv venv --python 3.12
uv pip install opentimelineio pillow
```

- `opentimelineio` 0.18.x (PyPI; the OpenTimelineIO Python package — import
  name `opentimelineio`, **not** `otio`; the "pyotio" name in older plan text
  is wrong)
- `pillow` (title-card render — `make_title.py`)
- `ffmpeg` (media synthesis; no `libfreetype` needed — the title is a
  PIL-rendered PNG, not `drawtext`)

The `uv venv` + `uv pip install` pair is cross-platform: uv finds the `.venv`
it just created, so there is no hard-coded interpreter path. Run the scripts
below with `uv run python …`.

## 1. Media (into `media/`)

```bash
mkdir -p media
ffmpeg -y -f lavfi -i "testsrc=size=1920x1080:rate=24:duration=20" \
       -f lavfi -i "sine=frequency=440:duration=20" \
       -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest media/clip_a.mp4
ffmpeg -y -f lavfi -i "smptebars=size=1920x1080:rate=24:duration=20" \
       -f lavfi -i "sine=frequency=554:duration=20" \
       -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest media/clip_b.mp4
ffmpeg -y -f lavfi -i "testsrc2=size=1920x1080:rate=24:duration=20" \
       -f lavfi -i "sine=frequency=659:duration=20" \
       -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest media/clip_c.mp4
ffmpeg -y -f lavfi -i "aevalsrc='0.30*sin(2*PI*220*t)+0.22*sin(2*PI*277.18*t)+0.12*sin(2*PI*329.63*t)':s=48000:d=60" \
       -c:a aac media/music.m4a
uv run python make_title.py media/title.png
```

These are the **H.264** variant's media — the codec that FAILS on Free Linux
(imports audio-only).

## 2. DNxHR transcode (the evidence variant)

Free Linux cannot decode H.264, so the passing evidence uses DNxHR SQ.
Verified codec: `dnxhd`, profile **DNXHR SQ**, 1920×1080, yuv422p, 24 fps,
PCM s16le 44.1 kHz mono. Transcode each clip — DNxHR is ~290 MB per 20 s
clip, which is why the `.mov` files are not checked in:

```bash
for c in a b c; do
  ffmpeg -y -i media/clip_$c.mp4 \
         -c:v dnxhd -profile:v 2 -c:a pcm_s16le -ar 44100 -ac 1 \
         media/clip_${c}_dnx.mov
done
```

`-profile:v 2` is **DNXHR SQ** in ffmpeg's `dnxhd` encoder (verified:
profiles 1–5 are DNXHR LB / SQ / HQ / HQX / 444 12-bit; 0 is a DNxHD variant).
Confirm with `ffprobe -v error -select_streams v:0
-show_entries stream=profile media/clip_a_dnx.mov` → `DNXHR SQ`.

## 3. Timeline

`build_specimen.py` assembles `specimen-60.otio` (the H.264 variant, relative
`media/` paths): 3 tracks — A1 music+fade, V1 three clips + a 1 s
SMPTE_Dissolve at 0:20, V2 title still 0:00–0:05 — markers beat-1@0:10 BLUE /
outro@0:45 RED. One post-step canonicalizes the fade to spec `AudioFadeIn_1`
(top-level `duration`), because the pure-Python build serializes custom effects
as generic `Effect.1`.

```
uv run python build_specimen.py
```

writes `specimen-60.otio` next to itself and prints the track/child structure
as a sanity check.

## Contents checklist (what the fidelity log must verify on import)

- [ ] 60.0 s total, 24 fps, no frame-rate drift
- [ ] three shots at exact 0:00/0:20/0:40 boundaries (±0 frames)
- [ ] 1 s cross-dissolve at 0:20 present (type + duration)
- [ ] hard cut at 0:40 (no stray transition)
- [ ] title card on upper layer 0:00–0:05, correct text, above shot 1
- [ ] still-image duration honored (5 s, not 1 frame)
- [ ] music bed 0:00–1:00, 2 s fade-in audible/visible
- [ ] clip audio tones in sync with video (440/554/659 Hz)
- [ ] markers beat-1 @ 0:10 (blue) and outro @ 0:45 (red)
- [ ] no relink dialog, no missing media (relative `media/` paths)
