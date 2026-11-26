DEV.TO POST

Title:       Resolve Free 21.1 removed Python scripting. Timeline files still work.
Tags:        python, video, opensource, davinciresolve
Canonical:   https://egnatia-oc.github.io/otio-kit/otio-import-troubleshooting.html
Series:      none

Paste everything below the line into the dev.to editor, then set the fields above.

---

DaVinci Resolve 21.1 moved Python scripting to Studio. If you were running a
free-build pipeline, the usual advice is to roll back to 21.0.4 or buy a licence.
Both are valid. There is a third option that got lost in the release-notes
discussion, and it is the one I ended up building on: **timeline files**.

Resolve still imports OTIO, EDL and FCPXML on the free edition. File import is not
scripting, so the change did not touch it. That means a tool can generate a timeline
outside Resolve and hand it over as a file — no Python inside the app, no socket, no
licence.

## What actually broke

I tested the scripting surfaces on Free 21.1.0.0017 on Ubuntu 24.04, the day after
release. The short version:

- The Scripts menu renders four submenus, all empty. `.py` files in the documented
  path never appear. No error is shown.
- The console opens and runs Lua, with the `resolve` object injected. There is no
  Python option on Free, and the sandbox strips `io` and `os.execute`.
- The external scripting socket at `127.0.0.1:1211` refuses connections whether
  Resolve is running or not.
- The documented Fusion macro trigger path is gone from the 21.1 UI.

Community reports differ on the Lua details across builds, so I link those next to
my rows rather than merging them. What is consistent: the Python routes are closed.

## The workaround, concretely

I wrote a small compiler that takes a YAML brief and writes an OTIO timeline. It
does not import anything into Resolve and does not need Resolve installed.

```yaml
spec_version: 0
name: specimen-60
fps: 24
media:
  clip_a: media/clip_a_dnx.mov
  clip_b: media/clip_b_dnx.mov
  title:  media/title.png
timeline:
  video:
    - track: V1
      clips:
        - media: clip_a
          duration: 20.0
        - media: clip_b
          duration: 20.0
          transition_in: {type: dissolve, duration: 1.0}
    - track: V2
      clips:
        - media: title
          duration: 5.0
markers:
  - {time: 10.0, color: blue, name: beat-1}
```

```
$ otio-kit compile brief.yaml -o timeline.otio
compiled 'specimen-60': 5 clips, 3 tracks -> timeline.otio
```

Then File > Import > Timeline in Resolve.

On the free build the import produced frame-accurate cuts, a one second
cross-dissolve, a five second title on the upper track, and the marker on the right
clip. No relink dialogs, no offline media. A second run on Windows by a different
person gave the same result with a different codec. Both rows carry the build number
and the reproduction kit in a public registry. macOS and anything newer than 21.1
are untested and labelled as such — a row only gets added after someone has actually
run the import on that build.

## Two failures that cost me an afternoon

Both are worth knowing even if you never use my tool, because neither one produces
an error message you can act on.

**A custom OTIO effect schema is fatal.** An effect named `AudioFadeIn_1` instead of
the stock `Effect.1` made the import return an empty timeline with no dialog. The
same file also fails OpenTimelineIO's own deserializer, so you can diagnose it
outside Resolve: list the distinct `OTIO_SCHEMA` values in the file and check they
are all stock.

**Relative media paths misresolve on Linux.** The conform step is filename and reel
based, not just path based, so a clip can be on disk and still import offline. Write
absolute paths to media that exists at import time.

## What it deliberately does not do

Effects, grades, Fusion comps, speed changes, gaps. There is no import evidence for
any of them, so the compiler rejects them with an error instead of emitting
something that looks right and is not. A tool that silently produces a plausible
wrong timeline is worse than one that refuses.

The project is 308 lines of Python with a larger test file, AGPL-3.0, and the
evidence trail is deliberately bigger than the code: a fidelity log, a per-build
registry, and the console matrix above.

If you import a generated OTIO into a build I have not tested, a report is more
useful than a star — there is a ten minute template in the repo.

- Repo: https://github.com/Egnatia-OC/otio-kit
- Project page: https://egnatia-oc.github.io/otio-kit/
- Import failures, written up: https://egnatia-oc.github.io/otio-kit/otio-import-troubleshooting.html

Not affiliated with Blackmagic Design.