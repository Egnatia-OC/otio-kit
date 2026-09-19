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

- Resolve version (Help → About shows the full version, e.g. 21.1.0.0017;
  the title bar shows the major version):
- OS + edition (Windows / macOS / Linux × Free / Studio):

**What you imported** (check one)

- [ ] The H.264 test kit — [specimen-60-h264.zip](https://github.com/Egnatia-OC/otio-kit/releases/download/specimen-60-h264/specimen-60-h264.zip) (Windows / macOS; the README inside has the checklist)
- [ ] The DNxHR specimen — `specimen-60-dnx.otio` (Linux; build recipe: [`specimen/BUILD.md`](../../specimen/BUILD.md))
- [ ] otio-kit emitter output (which command):
- [ ] Your own timeline file (OTIO / FCPXML / EDL)

**Result** (fill in what applies)

- Import: succeeded / failed (exact Import Log message if failed):
- Timing: cuts at expected frame positions (0:00 / 0:20 / 0:40) / drift (describe):
- Transitions intact?
- Markers present? (note: the emitter places markers clip-local; the red
  "outro" marker is expected absent — known emitter limitation)
- Media: clean / relink dialog / video invisible (H.264 on Free Linux is a
  pre-existing gap, not a 21.1 regression)
**Optional:** a screenshot of the timeline + Import Log, or the `.otio` file
itself.
