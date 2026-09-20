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
| 21.1.0.0017 | Linux (Ubuntu 24.04.4) | Free | first-party (this project) | 2026-09-15 | **PASS** — 60 s / 24 fps specimen (DNxHR video + PCM tones, AAC music bed; absolute paths): frame-accurate cuts, 1 s cross-dissolve intact, title + still honored, in-range marker present (clip-local; the second marker is emitted out of its clip's range and is dropped — documented emitter limitation), no relink dialogs. AAC music bed silent (pre-existing Free/Linux codec gap, documented in the log). [Fidelity log](fidelity-log.md) |
| 21.1.0.0017 | Windows 10 Pro 22H2 (GTX 1650) | Free | independent (control run, "Chris") | 2026-09-20/21 | **PASS** — 60 s / 24 fps H.264 kit specimen (stock-`Effect.1` fade; relative `media/` paths): frame-exact cuts 0:00/0:20/0:40, 1 s dissolve intact, title + still honored, in-range marker present, out-of-range marker dropped (matches Linux — limitation is cross-platform), 60 s total, no relink dialog. Media decode: video plays (H.264 decodes on Windows Free), audio audible (the bed is a synthesized sine chord), no offline clips. **2 s fade-in applied** — handle on the music clip, waveform ramps 0:00–0:02: the stock-Effect fade is recognized and applied, not just tolerated. [Report](reports/2026-09-20-windows-0017-partB.md) |

**Count: 2 independent verifications** (2 machines: Linux + Windows, Free 21.1).

## How rows get added

- **First-party:** the specimen is re-imported on each new Resolve build we
  test (21.2, 22.0, …). That per-release re-test cadence is what patronage
  funds.
- **Crowd (you):** import the specimen into *your* Resolve and file a
  [fidelity report](https://github.com/Egnatia-OC/otio-kit/issues/new?template=fidelity-report.md)
  — about 10 minutes. Windows/macOS: [download the H.264 kit](https://github.com/Egnatia-OC/otio-kit/releases/download/specimen-60-h264/specimen-60-h264.zip);
  Linux: build the DNxHR variant per the recipe below. Each report becomes a
  row here, cited to the report and the contributor.

## The specimen

Deterministic 60 s / 24 fps / 1920×1080 timeline, three tracks: cuts at
0:00 / 0:20 / 0:40, a 1 s cross-dissolve, a 5 s title, a music bed, two
markers. Same input → same output, so any row is reproducible.

- **H.264 kit (Windows / macOS):** [specimen-60-h264.zip](https://github.com/Egnatia-OC/otio-kit/releases/download/specimen-60-h264/specimen-60-h264.zip) — ready to import, checklist inside.
- **DNxHR variant (Free Linux, the evidence variant):** build recipe at
  [`specimen/BUILD.md`](../specimen/BUILD.md) (the repo carries 0-byte
  media stubs; the build host keeps the real media).
