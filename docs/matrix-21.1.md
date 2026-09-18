# Task 0.1 — Console-scripting verification matrix (Free 21.1, first-party)

Machine: Mirai (192.168.1.117), Ubuntu 24.04.4, Ryzen 5 7600X, RTX 3090 (24 GB),
DaVinci Resolve **21.1.0.0017 Free**. Tested 2026-09-14/15 (day 0-1 of the news cycle).
Method: live GUI session on a headless NVIDIA Xorg display (`:5`, 1920×1080,
`UseDisplayDevice None`), driven over VNC. Evidence screenshots captured
2026-09-15 (`t1-menu.xwd`, `t2-console.xwd`) but not preserved (host `/tmp`
cleared); re-capture pending — see `KNOWN-ISSUES.md`.

Environment notes (setup findings, not matrix rows):
- 21.1 Free installs and runs on Ubuntu 24.04 despite official Rocky-8.6-only list (R10 evidence).
- Resolve requires: VRAM free at launch (crashes at GPUDetect under memory pressure),
  `libxcb-cursor0`, `libxcb-xinerama0`, `libxcb-xinput0` (+family) for its bundled Qt xcb
  plugin — the installer checks none of these.
- No monitor attached → falls over unless a GPU-backed virtual display exists.

| Test | Result | Evidence |
|---|---|---|
| T1 — Scripts-menu user Python script | **SILENTLY DEAD (menu layer).** Workspace → Scripts menu renders **4 submenus, all empty**. `t1_scripts_menu.py` + `t4_os_execute.py` verified present in `~/.local/share/DaVinciResolve/Fusion/Scripts/Utility/` (documented path). Nothing appears; nothing runs. | File listing on record; screenshot captured 09-15 but not preserved (see header), re-capture scheduled |
| T2 — Console exists + executes | **ALIVE (Lua only).** Console opens (F6 / Workspace → Console). Executes Lua; `resolve` global injected; `resolve:GetProjectManager():GetCurrentProject()` returns a live project object (user observed object dump: "App: resolve 127.0.0.1 UUID: …"). **No Lua/Python language selector exists on Free** — Python console gated to Studio. Console sandbox strips `io` (nil), `os.execute` (nil), `bmd.writefile` (nil); surviving `os` keys: `tmpname, getenv, clock, date, time, difftime`. **Console can compute + query the API but cannot write files or spawn processes.** | User-executed probes (this session); screenshot captured 09-15 but not preserved (see header), re-capture scheduled |
| T3 — runpy from file (via console) | **UNTESTABLE — no Python console on Free.** Python toggle absent (see T2). | T2 |
| T4 — os.execute / subprocess in-app | **DEAD (both paths).** Menu path dead via T1. Console path: `os.execute` is nil (sandbox). | T2 probes |
| T5 — Lua macro (Fusion) | **TRIGGER PATH ABSENT.** Fusion page menu shows no Tools → Macros browser (21.1 UI: a "Macro Editor" entry exists; the documented `t5_macro` trigger path does not). Macro in `~/.local/share/DaVinciResolve/Fusion/Scripts/Macros/` unreachable via any observed menu path. Runbook's lowest-confidence test — recorded as observed, not chased. | User session report 2026-09-15 |
| T6 — External scripting socket | **DEAD both states.** Closed baseline: 127.0.0.1:1211 refused (`t6-socket-closed.txt`). Running state (Resolve up): still refused — `ConnectionRefusedError [Errno 111]` at 01:44 local. `DaVinciResolveScript` ships in-app only (`/opt/resolve/Developer/Scripting/`, `/opt/resolve/ResolvePython/lib/modules/`); not importable from system Python (expected). | Probe output on record |
## One-paragraph summary (strike-ready)

On DaVinci Resolve **21.1 Free**, first-party tested the day after release: the Scripts
menu renders but loads zero user scripts from the documented path; the external
scripting socket (127.0.0.1:1211) is refused whether Resolve is running or not; and the
console — which still exists — is **Lua-only** (no Python selector), sandboxed with no
`io`, no `os.execute`, no filesystem writes. In-app automation on Free is reduced to
read/compute API queries through a Lua REPL. Python scripting is now a Studio feature,
and the migration path Free users had (external socket, scripts menu, Python console)
is closed in the same release. What still works on Free: timeline **files** — OTIO/EDL
import/export via the UI — which is exactly the integration surface that matters.
