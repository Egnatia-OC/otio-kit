# Fidelity registry

The public answer to: **does a timeline file import correctly into *that*
Resolve build?** One row per (Resolve version × OS × edition), with a
reproduction path for every claim.

This is a living, versioned record. It starts at **1 independent
verification** — ours — and grows one row per report. The count below is
always the actual count; no "community-verified" claim is made until there
are multiple independent rows.

## Rows

| Resolve | OS | Edition | Source | Date | Result |
|---|---|---|---|---|---|
| 21.1.0.0017 | Linux (Ubuntu 24.04.4) | Free | first-party (us) | 2026-09-15 | **PASS** — 60 s / 24 fps specimen, DNxHR media: frame-accurate cuts, 1 s cross-dissolve intact, title + still honored, markers present (clip-local), no relink dialogs. AAC music bed silent (pre-existing Free/Linux codec gap, documented in the log). [Fidelity log](fidelity-log.md) |

**Count: 1 independent verification** (1 machine, Linux Free 21.1).

## How rows get added

- **First-party:** the specimen is re-imported on each new Resolve build we
  test (21.2, 22.0, …). That per-release re-test cadence is what patronage
  funds.
- **Crowd (you):** import the same specimen into *your* Resolve and file a
  [fidelity report](https://github.com/Egnatia-OC/otio-kit/issues/new?template=fidelity-report.md)
  — a 2-minute contribution. Each report becomes a row here, cited to the
  report and the contributor.

## The specimen

Deterministic 60 s / 24 fps / 1920×1080 timeline, three tracks: cuts at
0:00 / 0:20 / 0:40, a 1 s cross-dissolve, a 5 s title, a music bed, two
markers. Same input → same output, so any row is reproducible. Media recipe:
[`specimen/BUILD.md`](../specimen/BUILD.md).
