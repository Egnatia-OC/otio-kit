---
name: Fidelity report
about: Report how a timeline file imports into YOUR Resolve — one report = one row in the public fidelity registry
labels: fidelity
---

**The one thing this needs:** what happens when a timeline file imports into
*your* Resolve. One report = one row in the public
[fidelity registry](../../docs/fidelity-registry.md). A clean import is as
valuable as a breakage — the registry is a coverage table, not a bug tracker.

**Environment**

- Resolve version (title bar, or System → System → "Version"):
- OS + edition (Windows / macOS / Linux × Free / Studio):

**What you imported** (check one)

- [ ] The test specimen — `specimen-60-dnx.otio` (media recipe: `specimen/BUILD.md`)
- [ ] otio-kit emitter output (which command):
- [ ] Your own timeline file (OTIO / FCPXML / EDL)

**Result** (fill in what applies)

- Import: succeeded / failed (exact Import Log message if failed):
- Timing: frame-accurate / drift (describe):
- Transitions intact?
- Markers present? (note: the emitter places markers clip-local)
- Media: clean / relink dialog / video invisible (H.264 on Free Linux is a
  pre-existing gap, not a 21.1 regression):

**Optional:** a screenshot of the timeline + Import Log, or the `.otio` file
itself.
