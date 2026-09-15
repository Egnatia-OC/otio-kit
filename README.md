# otio-kit

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
pip install otio-kit        # from PyPI (v0.0.1, day-10 release)
```

Until then, from source:

```
git clone <this repo> && cd otio-kit
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
[`docs/spec-scope-v0.md`](docs/spec-scope-v0.md)). Releases are tagged from
day one; breaking spec changes bump `spec_version`.

## Licence

AGPL-3.0 — see `LICENSE`. Commercial licensing available at first request
(contact via the repository).
