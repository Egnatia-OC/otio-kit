# Specimen build — reproduction

Deterministic build of the task-0.2 fidelity specimen (no LLM involved).
Everything is regenerable from this file; the checked-in `media/` and
`specimen-60.otio` are the current outputs.

## Environment

```
uv venv --python 3.12 .venv          # from cutlist-p0/
uv pip install --python .venv/bin/python opentimelineio pillow
```

- `opentimelineio` 0.18.1 (PyPI; the OpenTimelineIO Python package — import
  name `opentimelineio`, NOT `otio`; the "pyotio" name in older plan text is
  wrong, fixed here as ground truth)
- `pillow` (title card render)
- `ffmpeg` (media synthesis; a build without `libfreetype` is fine — no
  `drawtext` needed, the title is a PIL-rendered PNG)

## Media (in `specimen/media/`)

```bash
ffmpeg -y -f lavfi -i "testsrc=size=1920x1080:rate=24:duration=20" \
       -f lavfi -i "sine=frequency=440:duration=20" \
       -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest clip_a.mp4
ffmpeg -y -f lavfi -i "smptebars=size=1920x1080:rate=24:duration=20" \
       -f lavfi -i "sine=frequency=554:duration=20" \
       -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest clip_b.mp4
ffmpeg -y -f lavfi -i "testsrc2=size=1920x1080:rate=24:duration=20" \
       -f lavfi -i "sine=frequency=659:duration=20" \
       -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest clip_c.mp4
ffmpeg -y -f lavfi -i "aevalsrc='0.30*sin(2*PI*220*t)+0.22*sin(2*PI*277.18*t)+0.12*sin(2*PI*329.63*t)':s=48000:d=60" \
       -c:a aac music.m4a
# title.png: PIL, black 1920x1080, "SPECIMEN 60" (DejaVu Sans Bold 110, white,
# centered y=480) + caption (DejaVu Sans 40, #cccccc, y=600)
```

## Timeline

`build_specimen.py` (this directory) assembles `specimen-60.otio` with
`opentimelineio`: 3 tracks (A1 music+fade, V1 three clips + 1 s SMPTE_Dissolve
at 0:20, V2 title still 0:00–0:05), markers beat-1@0:10 BLUE / outro@0:45 RED.
One post-step canonicalizes the fade to spec `AudioFadeIn_1` (top-level
`duration`) because the pure-Python build serializes custom effects as generic
`Effect.1`.

Run: `python build_specimen.py` — rewrites `specimen-60.otio` and prints the
track/child structure as a sanity check.

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
