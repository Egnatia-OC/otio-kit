# Console scripting on DaVinci Resolve Free 21.1 (Linux): first-party test results

**Tested 2026-09-14/15 — the day after the 21.1 release.** One machine, one
operator, every claim in this document reproduced by us, on our hardware, with
the exact build (`21.1.0.0017 Free`, Ubuntu 24.04, RTX 3090). Method and raw
evidence: [`fidelity-log.md`](fidelity-log.md), [`matrix-21.1.md`](matrix-21.1.md).

Not affiliated with or endorsed by Blackmagic Design.

## The matrix

| # | Surface | Result on Free 21.1 (Linux) |
|---|---|---|
| T1 | Scripts menu (user Python scripts) | **Dead.** The menu renders — four submenus, all empty. Scripts placed in the documented `Fusion/Scripts/Utility/` path never appear. |
| T2 | In-app console | **Alive — Lua only.** Executes code; the `resolve` global is injected; the API answers. No Python selector exists on Free. |
| T2b | Console sandbox | **Compute-only.** `io` stripped, `os.execute` nil, no file writes via `bmd.writefile`. Surviving `os` keys: `tmpname, getenv, clock, date, time, difftime`. |
| T3 | Running Python from file via console | **Untestable** — no Python console on Free. |
| T4 | `os.execute` / subprocess | **Dead** — menu path dead (T1); console path stripped (T2b). |
| T5 | Lua macros (Fusion) | **Trigger path absent** — the documented Tools → Macros browser is gone from the 21.1 Fusion UI. |
| T6 | External scripting socket (127.0.0.1:1211) | **Dead both states** — connection refused with Resolve running and closed. The `DaVinciResolveScript` module ships in-app only. |

## What this means

The official 21.1 release notes moved Python scripting to Studio. Community
discussion assumed the old escape hatches survived on Free. They do not — and we
can say that from measurement, not memo-reading:

- the **menu** loads nothing,
- the **socket** refuses connections,
- the **console** that remains is a Lua REPL whose sandbox cannot touch the
  filesystem or spawn a process. It can query the API. That is all.

Every automation surface Free users had — scripts menu, external socket,
Python console — is closed in the same release that moved Python to Studio.

## What still works: files

Timeline **import** survives intact, and it is faithful. Our 60-second
three-track specimen (cuts, cross-dissolve, title still, markers, audio fade)
imports cleanly on Free 21.1 Linux when media is a Free-decodable codec — with
two sharp edges every tool built on files must respect:

1. **Linux-Free decodes no H.264/H.265** (and never has; Studio+NVIDIA decodes
   it). Media must ship as DNxHR-class or the picture simply never appears —
   clips import as audio-only. Windows/macOS Free are not affected.
2. **Unknown OTIO schemas crash the importer** (fatal, no message). Stock
   schemas only; custom semantics ride in `metadata`.

Both established first-party; details and citations in the fidelity log.

## For tool builders

If your product drives Resolve through any scripting surface on Free, it died
this week. If it emits files, it lives — and the fidelity requirements are now
measured, public, and version-pinned. We will re-run this matrix on every
Resolve release; the results land in the Fidelity Registry.

## References

- Official 21.1 release notes: [Blackmagic Design forum, 21.1 thread](https://forum.blackmagicdesign.com/viewtopic.php?f=21&t=239823)
- H.264 on Linux Free/Studio: [BMD forum t=125656](https://forum.blackmagicdesign.com/viewtopic.php?f=21&t=125656), [BMD forum t=192600](https://forum.blackmagicdesign.com/viewtopic.php?t=192600&p=1001985)
- Our full test matrix: [`matrix-21.1.md`](matrix-21.1.md) · fidelity log: [`fidelity-log.md`](fidelity-log.md)
