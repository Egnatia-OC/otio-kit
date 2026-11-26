# Relaunch notes — 2026-11

Repo state at the time of writing: 1 GitHub star, 25 PyPI downloads/month, two
verified import rows (Free 21.1 Linux + Windows), zero posts to any community.
The September work was docs and evidence, not distribution. Nothing has ever
been submitted to Hacker News (`hn.algolia.com` search for `otio-kit`: no hits).

## Why now works

The 21.1 news cycle is over, but the *search intent* is alive:

- `davinciresolveclub.com/davinci-resolve-scripting-api` — published 2026-11-14,
  updated 2026-11-19, 18-minute piece on exactly this problem. Its answer to
  "Free 21.1 + Python" is "buy Studio ($295) or stay on 21.0.4". Its scripting
  matrix has no row for file import.
- `samuelgursky/davinci-resolve-mcp` issue #203 — still receiving build-specific
  reports (2026-11-01 macOS 21.1.2.10).
- Puget Systems' benchmark post: "stay on Free 21.0 or move to Studio".

So the market is being told the only options are *pay* or *don't upgrade*.
otio-kit's claim is a third option that is verifiable, and the discourse has a
hole exactly where it sits. That is the campaign.

Do not re-litigate the 21.1 news. It is two months old and the technical
audience has moved on. Lead with the workaround and the evidence.

## Pre-flight (blockers — none of these are optional)

1. **Landing page root.** `pages/index.html` now exists; before it, the Pages
   root returned 404 and only `/autosubs-alternative.html` resolved. Every post
   needs a destination that answers "what is this, does it work, how do I run
   it" in one screen.
2. **Repo topics + homepage.** Both empty today; discovery on GitHub is dead
   without them.
   ```
   gh repo edit Egnatia-OC/otio-kit \
     --add-topic davinci-resolve,opentimelineio,otio,video-editing,timeline,ffmpeg,python \
     --homepage https://egnatia-oc.github.io/otio-kit/
   ```
3. **A GitHub Release for v0.0.4.** Tags exist (`v0.0.1`…`v0.0.4`) but only the
   `specimen-60-h264` tag has a Release. A launch with no release page reads as
   abandoned.
   ```
   gh release create v0.0.4 --title "v0.0.4" --notes-file CHANGELOG.md
   ```
4. **Record the import.** The one asset the project does not have: 20–40 s of
   the generated OTIO landing in Resolve — media pool populated, timeline with
   the two clips, the dissolve visible, the marker on the ruler. Record on the
   Windows or Linux machine that already produced a PASS row. Without a moving
   picture, a timeline tool is a README. Shot list: brief on the left, `otio-kit
   compile` in a terminal, File → Import → Timeline, the timeline appearing,
   playhead crossing the dissolve.

## Channels, in order of value

| Where | What | Notes |
|---|---|---|
| Show HN | title + first comment below | Tue–Thu, 08:00–10:00 US Eastern. Today is US Thanksgiving — do not post today. Next window: Mon 30 Nov / Tue 1 Dec. |
| r/davinciresolve | practical post, no pitch | Largest pool of Free users; the "buy Studio" objection will appear — answer it in the post body, not in comments. |
| r/editors | workflow angle, shorter | Crosspost 24 h later, rewritten, not copy-pasted. |
| davinci-resolve-mcp issue #203 | a comment, not a link drop | Post the two PASS rows with build numbers and the reproduction kit. This is the highest-intent audience that exists. |
| davinciresolveclub (Jason Miller) | email/pitch | Their guide is now the canonical answer and is missing file import entirely. Offer the evidence, not a favour. |
| Lobsters / r/VideoEditing | after HN | Only if HN produces discussion worth pointing at. |

## Show HN

**Title** (70 chars):

```
Show HN: otio-kit – compile a YAML brief into a Resolve timeline file
```

**Body:**

> Resolve 21.1 moved Python scripting to Studio. On Free the Scripts menu renders
> empty, the external socket refuses connections, and the console that remains is
> a sandboxed Lua REPL (I tested all of it, twice, method in
> docs/console-status.md).
>
> The one interface that did not change is file import. So this compiles a small
> YAML brief into stock OTIO: sequential clips, a cross-dissolve, stills on upper
> tracks, markers, a music bed. `pip install otio-kit`, `otio-kit compile
> brief.yaml -o timeline.otio`, import.
>
> The part I care about is the evidence trail. Every fidelity claim is a row in
> docs/fidelity-registry.md with a build number, an OS, and a reproduction kit —
> two PASS rows so far (Free 21.1.0.0017 on Ubuntu 24.04 and on Windows 10).
> macOS and 21.2 are untested and listed as such. While testing I found that
> custom OTIO effect schemas are fatal to the importer (silent empty timeline, no
> dialog) and that bare relative media URLs misresolve on Linux — both are now
> hard rules in the emitter rather than README footnotes.
>
> Deliberately out of scope in v0: effects, grades, Fusion, speed changes, gaps.
> They have no import evidence, so the spec rejects them instead of guessing.
>
> AGPL-3.0. Happy to answer anything about the import behaviour — the failure
> modes are more interesting than the success.

**First comment** (post immediately after submitting, adds the honest limits):

> Two things I expect to be asked.
>
> 1. "Why not just buy Studio?" Valid — if you need scripting inside Resolve, buy
> it. This is for the other case: the compiler never touches Resolve. It runs on
> any machine with Python 3.10+, the output is a text file you can diff and
> commit, and it works on Free. The two are not in conflict.
> 2. "Why not EDL/FCPXML?" EDL is the fallback and it works for cuts only —
> CMX_3600 cannot carry the dissolve, stills, or markers in one file. OTIO is
> what Resolve documents since 18.6. The failure log with each format is in
> docs/fidelity-log.md.

## r/davinciresolve

**Title:**

```
If 21.1 broke your Resolve automation, the timeline file still works — here's a compiler and the import results
```

**Body:**

> Short version: 21.1 removed Python scripting from Free. I tested every scripting
> surface on Free 21.1.0.0017 (menu, socket, console, macros) and wrote down
> exactly what is dead — summary here, raw method in the repo. File import was
> untouched, so I built the workflow on that instead.
>
> `pip install otio-kit`, write a ~15-line YAML brief, get an OTIO file, File →
> Import → Timeline. Verified frame-accurate cuts on 21.1.0.0017 Free, Linux and
> Windows (independent control run on the Windows box), including a 1 s dissolve,
> a title on V2, and clip markers. No relink dialogs when media is DNxHR at
> absolute paths.
>
> What it does not do: effects, grades, Fusion, speed ramps, gaps. No import
> evidence for those, so the spec refuses them loudly instead of producing a
> timeline that looks right and isn't.
>
> Two gotchas I hit so you don't have to: custom OTIO effect schemas make the
> importer fail with an empty timeline and no dialog, and relative media paths
> misresolve on Linux. Both are handled in the emitter.
>
> macOS is untested and I say so on the site. If you import the specimen kit into
> your build, the fidelity report template takes ~10 minutes and gets you a cited
> row.
>
> [link] [link to AutoSubs comparison page]

## The objection to prepare for

Every thread will contain: *"just pay for Studio."*

Answer once, with the division of labour: Studio buys you scripting **inside**
Resolve. otio-kit is a compiler that runs **outside** it, produces a reviewable
text file, and does not need Resolve installed at all. For a pipeline that
generates cuts from a brief or an LLM, a file is the better interface anyway —
versionable, diffable, revertible. That is not a consolation prize; it is the
argument the README makes and it holds if scripting comes back to Free.

Do not argue about price, licence terms, or Blackmagic's motives. Those threads
go nowhere and the answers are already in `docs/console-status.md`.

## Claims discipline

Safe to say: Free 21.1 Linux PASS, Free 21.1 Windows PASS (independent run),
macOS untested, 21.2 untested, 25 PyPI downloads/month (do not quote download
numbers), alpha, AGPL-3.0.

Never say: "works with any Resolve", "works on macOS", "supports 21.2",
"community-verified", or anything implying Blackmagic endorsement. The trademark
line stays.

## After the launch

- Answer every fidelity report within a day and add the row — the registry is
  the product's credibility, and the launch's only durable output is rows.
- If HN lands: the follow-up post is the 21.2 re-test with a screenshot, not
  another announcement.
- Patronage is still "opens soon" in the README. A launch that funnels people to
  a not-yet-open checkout loses them; either open it before the post or point
  the CTA at the notify list only.