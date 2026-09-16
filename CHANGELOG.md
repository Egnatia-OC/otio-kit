# Changelog

Format: newest first. Spec semantics are frozen per `spec_version`
(`docs/spec-scope-v0.md`); breaking spec changes bump `spec_version`.

## 0.0.2 (2026-09-16)

- Reject clip durations that round to fewer than 1 frame (loud `EmitError`
  with the minimum, instead of emitting a 0-frame clip)
- Reject transition durations that round to fewer than 2 frames
- Markers exactly on a cut boundary now attach to the clip that *starts*
  there (half-open interval; previously they landed at the end of the
  previous clip)
- Duplicate track names are rejected (previously emitted silently)
- Zero-marker specs no longer hit the video-track guard in `_attach_markers`
- CI runs on the default branch (`master`; the old trigger said `main` and
  never fired) and on Windows as well as Ubuntu (Python 3.10/3.12)
- Golden test is portable: media paths are normalised before comparison
  (previously byte-compared against absolute paths from one machine); the
  POSIX-only `startswith("/")` assertion is replaced with
  `pathlib.Path(...).is_absolute()`
- Specimen committed: `specimen/BUILD.md`, `specimen/brief.md`,
  `specimen/build_specimen.py` (the bench harness now defaults to the
  committed brief); matrix screenshot citation corrected (not preserved,
  re-capture pending)
- Docs: audio fade moved from "covers" to "excluded" (intent metadata, not
  an applied fade); frame-quantization model documented; README states the
  stub-media limitation and CI scope; `KNOWN-ISSUES.md` added

## 0.0.1 (2026-09-16)

- First public release: spec v0 schema + validator, media resolver, OTIO
  emitter (stock schemas only), CLI (`compile` / `validate`), golden
  round-trip tests
