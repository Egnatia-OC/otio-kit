# otio-kit

![ci](https://github.com/Egnatia-OC/otio-kit/actions/workflows/ci.yml/badge.svg)

Compile timeline briefs into files that import cleanly into **DaVinci Resolve**
— Free or Studio, on Windows, macOS, or Linux. No scripting bridge.

> Not affiliated with or endorsed by Blackmagic Design. "DaVinci Resolve" is a
> trademark of Blackmagic Design Pty Ltd.

## Why

Resolve 21.1 moved Python scripting to Studio. The one interface it left
untouched is the **timeline file**: Resolve documents OTIO, EDL, and
FCPXML import for Free and Studio on the supported platforms. This
project has verified the OTIO import on Free 21.1 Linux (Windows is being
checked; macOS has not been run yet), and file import is the only
automation route I've found that survives 21.1 on Free.

`otio-kit` compiles a small YAML brief into a standard OTIO file.

**Testing starts with the most restricted target: Free 21.1 on Linux**
(no scripting, no H.264 decode). A timeline that
survives that import has hit the strictest subset of constraints. The
import has not yet been run on Windows or macOS; a Windows control run is
next and will be logged. The breakage list and the v0 scope:
[`fidelity-log`](docs/fidelity-log.md),
[`console-status`](docs/console-status.md), [`spec-scope`](docs/spec-scope-v0.md).

**Why a file, not an API call:** even if scripting comes back to Free, the
file approach stands on its own. The output is a text file — diffable,
versionable in git, revertable, and readable before it touches a timeline.
An API call that mutates live NLE state can't give you that.

## Install

```
pip install otio-kit        # from PyPI (requires Python 3.10+)
```

Or from source:

```
git clone https://github.com/Egnatia-OC/otio-kit && cd otio-kit
uv venv --python 3.12
uv pip install -e .
```

**Requirements:** Python 3.10+ (3.10 and 3.12 in CI). Pure Python — three
dependencies (`opentimelineio`, `pyyaml`, `jsonschema`), CPU-only, no GPU,
no display, no network at compile time, and no Resolve installation needed
to compile. The compiler runs anywhere Python 3.10+ runs, on Windows,
macOS, or Linux; importing the output depends on the target Resolve
version and its system requirements (BMD publishes them per version).

## Use

```
otio-kit compile brief.yaml -o timeline.otio
otio-kit validate brief.yaml
```

Missing media fails loudly, listing every absent file in one pass.

## Status

Alpha. The emitter covers the v0 scope only (see
[`docs/spec-scope-v0.md`](docs/spec-scope-v0.md)); open items and known
issues in [`KNOWN-ISSUES.md`](KNOWN-ISSUES.md). CI: ruff + pytest on Ubuntu
and Windows, Python 3.10/3.12.

Import target: any Resolve that imports OTIO (documented in the official
manual since 18.6); the verified row is Free 21.1 Linux. The
[fidelity registry](docs/fidelity-registry.md) tracks the rest.

The committed media under `tests/golden/media/` are empty stubs: the golden
suite proves emitter *determinism*, not import fidelity — import fidelity is
the Resolve import run documented in
[`docs/fidelity-log.md`](docs/fidelity-log.md). Regenerate the real specimen
media from the recipe in [`specimen/BUILD.md`](specimen/BUILD.md) (ffmpeg
synthesis, DNxHR transcode, `make_title.py`); `build_specimen.py` assembles
the timeline only.

This project is not part of the OpenTimelineIO project (which it consumes).

## Support the project

otio-kit is free and stays free. The ongoing cost is the **per-release
re-test cadence** — the project plans to re-test each new Resolve build
and update [`docs/fidelity-log.md`](docs/fidelity-log.md). That's what
patronage is planned to fund. No perks, no tiers, nothing to unlock.

- **Patronage** — opens soon; the project is completing its business
  registration and the checkout will appear here. Patronage is a standard
  purchase (the project is a business, not a non-profit); nothing here is
  tax-deductible.
- **Get notified** — an email list for the flagship launch and per-release
  re-test announcements is being set up; the link lands here. Single-purpose,
  unsubscribe anytime.

Privacy, in one paragraph: we collect one thing — your email address, if you
choose to subscribe to project updates. Subscriptions are handled by
MailerLite, a third-party email service; they send a confirmation email
before you are added, and that confirmation is your consent record; every
email includes an unsubscribe link. We email this list only for major project
milestones (such as when project patronage opens) and never share or sell
the list. Unsubscribe anytime, or email us to be removed manually. Payment
data, if you later support the project, is processed by our payment provider
and never stored by us.

## Licence

AGPL-3.0 — see `LICENSE`. Commercial dual licence: terms on request — open a
GitHub issue labelled `licensing`.
