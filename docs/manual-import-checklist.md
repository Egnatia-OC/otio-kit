# Manual import checklist (per Resolve version)

Run after every Resolve release you support. One row per run, appended to
`docs/fidelity-log.md`. Specimen: `tests/golden/specimen60.yaml`, compiled with
`otio-kit compile`, media present at the referenced absolute paths.

## Run template

- Resolve version / OS / GPU:
- Date:
- Operator:

## Steps

1. New project, any name.
2. `File → Import → Timeline…` → select the compiled `.otio`.
3. If a "Load OTIO" dialog appears: leave defaults, Ok.
4. Record any error dialog verbatim (or `Import Log (Fatal)` from
   `~/.local/share/DaVinciResolve/logs/ResolveDebug.txt`).
5. Walk the checklist below; mark ✅ / ❌ / ⚠️ with a note.

## Checklist

- [ ] Timeline created, named `specimen-60`, no error dialog
- [ ] Three tracks: A1 (audio), V1 (video), V2 (video)
- [ ] V1 has three clips, 20 s each, boundaries at 0:00 / 0:20 / 0:40
- [ ] Cross-dissolve at 0:20, ~1 s, plays
- [ ] Hard cut at 0:40 — no stray transition
- [ ] Title (title.png) on V2, 0:00–0:05, above clip_a
- [ ] Total timeline duration 60 s
- [ ] Blue marker at 0:10 (on/inside clip_a)
- [ ] Red marker at 0:45 (on/inside clip_c)
- [ ] All video clips online with picture (DNxHR media) — no "Media Offline"
- [ ] No relink dialog appeared
- [ ] Audio: tones audible when scrubbing clips (Linux-Free: AAC will be silent)

## Results so far

| Date | Resolve | OS | Outcome | Notes |
|---|---|---|---|---|
| 2026-09-15 | 21.1.0.0017 Free | Ubuntu 24.04, RTX 3090 | PASS (DNxHR variant) | red-marker observation pending; AAC music silent-expected; see fidelity-log.md |
