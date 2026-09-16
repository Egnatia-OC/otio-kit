# otio-kit

![ci](https://github.com/Egnatia-OC/otio-kit/actions/workflows/ci.yml/badge.svg)

Compile timeline briefs into files that import cleanly into **DaVinci Resolve
Free** — no scripting bridge, no Studio required.

> Not affiliated with or endorsed by Blackmagic Design. "DaVinci Resolve" is a
> trademark of Blackmagic Design Pty Ltd.

## Why

Resolve 21.1 moved Python scripting to Studio and Linux-Free has never decoded
H.264. What still works everywhere: **timeline files**. `otio-kit` compiles a
small YAML brief into OTIO that imports cleanly — verified first-party on Free
21.1 Linux, with the breakage list and safe-set published in
[`docs/fidelity-log.md`](docs/fidelity-log.md), [`docs/console-status.md`](docs/console-status.md), and
[`docs/spec-scope-v0.md`](docs/spec-scope-v0.md).

## Install

```
pip install otio-kit        # from PyPI (requires Python 3.10+)
```

Or from source:

```
git clone https://github.com/Egnatia-OC/otio-kit && cd otio-kit
uv venv --python 3.12 .venv && uv pip install --python .venv/bin/python -e .
```

## Use

```
otio-kit compile brief.yaml -o timeline.otio
otio-kit validate brief.yaml
```

Missing media fails loudly, listing every absent file in one pass. Never silent.

## Status

Alpha. The emitter covers the v0 safe-set only (see
[`docs/spec-scope-v0.md`](docs/spec-scope-v0.md)); open items and known
issues in [`KNOWN-ISSUES.md`](KNOWN-ISSUES.md). CI: ruff + pytest on Ubuntu
and Windows, Python 3.10/3.12.

The committed media under `tests/golden/media/` are empty stubs: the golden
suite proves emitter *determinism*, not import fidelity — import fidelity is
the Resolve import run documented in
[`docs/fidelity-log.md`](docs/fidelity-log.md). Regenerate the real specimen
media with `specimen/build_specimen.py` (see `specimen/BUILD.md`).

This project is not part of the OpenTimelineIO project (which it consumes).

## Licence

AGPL-3.0 — see `LICENSE`. Commercial dual licence: terms on request — open a
GitHub issue labelled `licensing`.
