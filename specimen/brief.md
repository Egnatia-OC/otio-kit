# Brief — Specimen 60

A 60-second edit at 24 fps, built from five source files in `media/`.

**Structure:** three video tracks in two layers plus a music bed.

**Bottom video layer (V1), full duration:** three shots of twenty seconds each,
back to back.

- Shot 1 (0:00–0:20): a classic color test pattern (`testsrc`, `clip_a.mp4`),
  with a steady 440 Hz tone in its audio track.
- Shot 2 (0:20–0:40): SMPTE color bars (`smptebars`, `clip_b.mp4`), 554 Hz tone.
- Shot 3 (0:40–1:00): a second color test pattern (`testsrc2`, `clip_c.mp4`),
  659 Hz tone.

Between shot 1 and shot 2 there is a **one-second cross-dissolve** centered on
the 0:20 cut (half a second out of shot 1, half a second into shot 2). No
transition at the 0:40 cut — that one is a hard cut.

**Top video layer (V2):** a full-frame title card for the first five seconds
(0:00–0:05) only. Black background, white text reading "SPECIMEN 60" with a
smaller gray caption beneath it (`title.png`, a still image held for 5 s).
The title sits above shot 1; after 0:05 the top layer is empty and shot 1 is
visible alone.

**Audio:** a single music bed across the whole 60 seconds (`music.m4a`) — a
sustained A-major chord (220 Hz + 277.18 Hz + 329.63 Hz sines, low levels).
The music fades in over the first **two seconds**. The three shots' own tones
play underneath as they appear.

**Markers:** one blue marker named `beat-1` at 0:10 (on shot 1), and one red
marker named `outro` at 0:45 (on shot 3).

Nothing else: no speed changes, no effects on video, no additional tracks,
no gaps. Total duration exactly 60.0 s (1440 frames).
