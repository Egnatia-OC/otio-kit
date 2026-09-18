# otio-kit

![ci](https://github.com/Egnatia-OC/otio-kit/actions/workflows/ci.yml/badge.svg)

Compile timeline briefs into files that import cleanly into **DaVinci Resolve**
— Free or Studio, on Windows, macOS, or Linux. No scripting bridge.

> Not affiliated with or endorsed by Blackmagic Design. "DaVinci Resolve" is a
> trademark of Blackmagic Design Pty Ltd.

## Why

Resolve 21.1 moved Python scripting to Studio. The one interface it left
untouched — on **every** OS and tier — is the **timeline file** (OTIO, FCPXML,
EDL). Every Resolve still imports them: Free or Studio, on Windows, macOS, or
Linux. So the file route works wherever yours runs, and it's the only
automation route left on Free.

`otio-kit` compiles a small YAML brief into a standard OTIO file for that route.

**We test hardest-first** — on the most restricted Resolve there is, **Linux
Free 21.1** (no scripting, no H.264 decode). A cutlist that survives that
gauntlet hits the strictest subset of constraints; the more-permissive targets
(Windows, macOS, Studio) add capability, they don't remove it. The breakage
list and safe-set: [`fidelity-log`](docs/fidelity-log.md),
[`console-status`](docs/console-status.md), [`spec-scope`](docs/spec-scope-v0.md).

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
media from the recipe in [`specimen/BUILD.md`](specimen/BUILD.md) (ffmpeg
synthesis, DNxHR transcode, `make_title.py`); `build_specimen.py` assembles
the timeline only.

This project is not part of the OpenTimelineIO project (which it consumes).

## Support the project

otio-kit is free and stays free. The ongoing cost is the **per-release
re-test cadence** — every new Resolve build gets re-imported and
[`docs/fidelity-log.md`](docs/fidelity-log.md) updated. That's what patronage
funds. No perks, no tiers, nothing to unlock.

- **Patronage** — opens soon; the project is completing its business
  registration and the checkout will appear here.
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

Patronage is processed as a standard purchase (the project is a business, not
a non-profit); nothing here is tax-deductible.

## Licence

AGPL-3.0 — see `LICENSE`. Commercial dual licence: terms on request — open a
GitHub issue labelled `licensing`.
