# Task 0.2 — Fidelity log: Resolve Free 21.1 (Linux) import of specimen-60

Machine: Mirai (192.168.1.117), Ubuntu 24.04.4, RTX 3090 (driver 595.84),
DaVinci Resolve **21.1.0.0017 Free**, headless NVIDIA Xorg display 1920×1080.
Specimen: deterministic 60 s / 24 fps / 1920×1080 timeline, 3 tracks, synthetic media
(see `specimen/BUILD.md`). Import tested 2026-09-15 (day 1).

## Result

**Import succeeds and is structurally faithful when media is DNxHR.**
`specimen-60-dnx.otio` (stock schemas + absolute paths + DNxHR media): clean import,
no dialogs, no relink, all seven structural checks pass except one marker
unconfirmed (below). The flagship file-based UX is viable on Free/Linux.

## Checklist results (DNxHR variant)

| Check | Result |
|---|---|
| 60.0 s total, 24 fps, no drift | ✅ confirmed |
| Shots at exact 0:00 / 0:20 / 0:40 | ✅ confirmed (also frame-accurate in the earlier OTIO runs' track layout) |
| 1 s cross-dissolve at 0:20 | ✅ present ("fade over at 20"); exact frame count not yet measured |
| Hard cut at 0:40, no stray transition | ✅ confirmed ("jump at 40") |
| Title on upper layer 0:00–0:05 | ✅ confirmed, 5 s honored |
| Still duration honored (not 1 frame) | ✅ confirmed |
| Music bed 0:00–1:00 + fade | ⚠️ clip present on A1; **audibility untested** (m4a is AAC — see codec matrix) |
| Clip audio tones in sync | ⚠️ untested (tones are PCM inside the DNx clips — should play; verify on next session) |
| Markers: blue @0:10, red @0:45 | ✅ blue confirmed / ⚠️ red not observed — verify pennant on ruler at 45 s; file contains it |
| No relink dialog, no missing media | ✅ confirmed (absolute paths, exact existing locations) |

## Root causes established tonight (each first-party tested)

1. **H.264/H.265 decode does not exist in Free Linux.** mp4 clips import as
   audio-only (container's AAC parsed, H.264 video invisible); DNxHR of the same
   clips plays with full picture. Public record matches: BMD forum — H.264 Linux
   decode is Studio+NVIDIA-only; Free Linux cannot decode *or encode* H.264/H.265
   (forum.blackmagicdesign.com t=125656, t=192600). Windows/Mac Free are NOT
   affected — platform-scoped gap, verify on Windows (offer accepted, pending).
2. **Unknown OTIO schema = fatal import.** The specimen's custom `AudioFadeIn_1`
   effect schema (with top-level `duration`) made the first import fail
   (`Import Log (Fatal) - failed to import OTIO timeline`, no reason given), and
   breaks `opentimelineio`'s own deserializer the same way. Stock `Effect.1` +
   metadata parses and imports. **Emitter rule: stock schemas only; custom
   semantics ride in metadata.**
3. **Video media conform on OTIO import is reel/filename-based, and H.264 clips
   fail it regardless** (3-of-4 / 3-of-3 "clips not yet found" dialogs; audio +
   stills conform by direct URL and land online). With DNxHR media at exact
   absolute paths, conform is silent and complete.
4. **EDL fallback works structurally**: cuts-only CMX_3600 imports, correct
   track/timing/names ("Failed to link … timecode extents do not match" only
   because pool lacked the H.264 media — with DNxHR pool media it should link;
   untested, low priority now that OTIO path is proven).
5. **Resolve Free Linux UI quirks in headless use**: no window manager needed;
   VNC (x11vnc+noVNC) fully drivable; console is Lua-only with a compute-only
   sandbox (no io/os.execute — see `matrix-21.1.md`).

## Environment requirements for Free-Linux operation (discovered)

- VRAM must be free at Resolve launch (GPUDetect aborts under memory pressure).
- `libxcb-cursor0`, `libxcb-xinerama0`, `libxcb-xinput0` + family must be
  installed for the bundled Qt xcb plugin (installer does not check).
- A GPU-backed display (headless NVIDIA Xorg with `UseDisplayDevice None` works;
  xrandr-only virtual monitors and Xvfb-class software GL do not satisfy Resolve).

## Product implications (for /plan; build does not write SPEC)

- Flagship branch: **file-based import UX confirmed on the hardest target**.
  Kill/pivot recommendation: no kill — full UX with the Linux-Free DNxHR rule.
- New product requirement candidate: transcode/proxy preset emission
  (ffmpeg, DNxHR SQ/HQ + PCM), scoped to Linux-Free targets.
- `otio-kit` emitter rule locked: stock schemas only, metadata for custom fields.
- Strike content now includes a complete first-party matrix (`matrix-21.1.md`)
  + this fidelity log + the H.264-Free-Linux story with citations.

## Open items

- [ ] Red marker @0:45 — confirm pennant on ruler (or log as import bug).
- [ ] Audio playback: 440/554/659 Hz tones audible on scrub (PCM in DNx clips);
      music.m4a (AAC) audibility — likely silent on Free Linux per codec record.
- [ ] Dissolve exact frame count (24 f) — measure.
- [ ] Windows-Free control run (user offered a machine): import original
      `specimen-60.otio` (relative paths, H.264) — expect clean + picture;
      would confirm the codec gap as the only platform exception.
- [ ] Control column: Free 20.3/21.0 behavior (per runbook, later).
