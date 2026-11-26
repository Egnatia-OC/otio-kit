# Open channels — no gatekeeper, works today

Ordered by return per minute spent. Every entry here accepts a submission from the
project owner without asking a moderator first. The subreddit is now optional, not
the plan.

| # | Place | Friction | What to send | Why it earns its slot |
|---|---|---|---|---|
| 1 | awesome-davinci-resolve (form or PR) | none — their policy says community submissions are included regardless of stars | the filled-in form text below | durable, curated, linked from a 436-star list; indexed by GitHub and Google |
| 2 | dev.to | free account, no review | the article in `devto-post.md` | Google finds it; set canonical to the site so it does not split SEO |
| 3 | r/opensource | none, self-promo allowed with detail | the short post below | small but genuine OSS audience, tolerant of "I built this" |
| 4 | r/LocalLLaMA | none, needs flair + substance | the local-model post below | big, technical, and the bench numbers are the hook |
| 5 | Mastodon / Bluesky | none | the three short posts | presence and inbound links; low reach, zero cost |
| 6 | Lemmy (c/opensource, c/videoediting) | none | the dev.to link | lenient, federated, long-lived posts |
| 7 | Blackmagic Design forum | account; no ads allowed | the findings post, link last | the audience is exactly right; expect moderation, so lead with measurements |
| 8 | AlternativeTo | free listing | the product blurb | captures "AutoSubs alternative" search |

Skip: Lobsters and Tildes (invite-only), Product Hunt (needs assets you do not have),
LinkedIn, X.

---

## 1. awesome-davinci-resolve — ready to submit

Form: https://docs.google.com/forms/d/e/1FAIpQLSdpbb2pSkkbMkLUFJxnVvlaH-FyO8IMRVxVgL2Lh6okBAqe1Q/viewform

Category: Workflow & Integration Tools

Name: otio-kit

URL: https://github.com/Egnatia-OC/otio-kit

Cost: Free

Developer: Egnatia OC (independent)

Description (one paragraph, fits the form):

> Compiles a short YAML brief into a standard OTIO timeline and imports it into
> Resolve. Built for the case where scripting is not available: the compiler runs
> outside Resolve, needs only Python 3.10+, and writes a text file you can diff and
> commit. Cuts, cross-dissolves, stills on upper tracks and markers; import verified
> on Free 21.1 on Linux and Windows, with the build numbers and method published.
> Effects, grades and Fusion are deliberately out of scope until there is import
> evidence for them.

PR alternative, exact line for the list (insert into "Workflow & Integration Tools",
alphabetical position after "otio"-adjacent entries):

```markdown
- [otio-kit](https://github.com/Egnatia-OC/otio-kit) ![Free](https://img.shields.io/badge/Cost-Free-brightgreen) — Compile a YAML brief into an OTIO timeline that imports cleanly into Resolve. File-based, so no scripting bridge and no Studio licence; cuts, dissolves, stills and markers verified on Free 21.1 Linux and Windows. Compiler runs on any Python 3.10+ machine. AGPL-3.0. *(by Egnatia OC)* `macOS, Windows, Linux` <sub>(⭐ 1 · updated 2026-11)</sub>
```

Their stated inclusion rule makes the star count a non-issue for a submission; do not
apologise for it or mention it in the form.

## 2. dev.to

Paste `devto-post.md`. In the editor sidebar set **Canonical URL** to
`https://egnatia-oc.github.io/otio-kit/otio-import-troubleshooting.html`.
Tags: `python`, `video`, `opensource`, `davinciresolve`.

## 3. r/opensource

Title: `otio-kit: compiling YAML briefs into DaVinci Resolve timelines, because scripting left the free version`

> DaVinci Resolve 21.1 moved Python scripting to Studio. On the free build, the
> Scripts menu loads nothing, the socket refuses connections, and the console is
> Lua-only and sandboxed. I tested all of it and published the matrix, then built
> around the one surface that did not change: file import.
>
> otio-kit compiles a short YAML brief into a standard OTIO timeline. Cuts,
> cross-dissolves, stills on upper tracks, markers, an audio bed. The compiler is
> 308 lines of Python, needs no Resolve install, and the output is a text file you
> can diff and commit. Import is verified on Free 21.1 on Linux and Windows, with
> build numbers and reproduction steps in a public registry. macOS is untested and
> labelled as such.
>
> The interesting part is the failure log: a custom OTIO effect schema makes the
> importer return an empty timeline with no error, and relative media paths
> misresolve on Linux. Both are now hard rules in the emitter.
>
> AGPL-3.0. Source and evidence: https://github.com/Egnatia-OC/otio-kit
> Write-up: https://egnatia-oc.github.io/otio-kit/
>
> Happy to answer anything about the import behaviour, and a report from a build I
> have not tested is genuinely more useful than a star.

## 4. r/LocalLLaMA

Title: `Compiling prose briefs into video timelines with a local model: harness, numbers, and where it fails`

> Not a video tool post exactly. I needed to turn a written edit brief into a
> structured timeline, and measured whether models can do it: brief + JSON schema in,
> YAML spec out, compiled to a timeline file, diffed against a hand-made golden.
>
> Result on a 60 s / 3-track specimen, temperature 0, single sample: qwen3.8:27b
> local hit 5/5 cut points within ±2 frames, structure exact, 30 s wall, $0. Four
> cloud models matched it for $0.0009–0.0038 per brief. qwen3:0.6b failed the gate
> (invalid YAML), which is the point of the control.
>
> Files and harness: https://github.com/Egnatia-OC/otio-kit/tree/master/bench
> Full table: https://github.com/Egnatia-OC/otio-kit/blob/master/docs/llm-baseline.md
>
> Caveats I would insist on if someone else posted this: one sample per model, a
> well-structured brief, and a mandatory human review step. Real briefs are messier,
> and schema repair is the next engineering item. The target app is DaVinci Resolve,
> which is why the output is OTIO and not a render.

## 5. Mastodon / Bluesky

Three variants, same day, slightly different wording. Hashtags only on Mastodon.

> DaVinci Resolve 21.1 moved Python scripting to Studio. Before you roll back to
> 21.0 or buy a licence: timeline files still import on Free. I tested every
> scripting surface, wrote down what is dead, and built a small compiler that turns
> a YAML brief into an OTIO timeline. Verified on Free 21.1, Linux and Windows.
> https://egnatia-oc.github.io/otio-kit/

> Imported a generated OTIO timeline into Resolve Free 21.1 today. Cuts land on the
> right frames, the dissolve holds, markers survive. No scripting, no Studio licence.
> 308 lines of Python and a public evidence log: https://github.com/Egnatia-OC/otio-kit

> Two things that silently break OTIO import into Resolve and cost me an afternoon:
> a custom effect schema (empty timeline, no error dialog) and relative media paths
> on Linux. Wrote both up: https://egnatia-oc.github.io/otio-kit/otio-import-troubleshooting.html

## 7. Blackmagic forum

Post in the Resolve forum's scripting/automation area. Lead with measurements, put
the link at the very bottom, expect the post to be read as a report rather than an
announcement. Do not mention a product name in the title.

> Title: Scripting surfaces on Free 21.1, measured: menu, socket, console, macros
>
> Body: the four findings, the method (build 21.1.0.0017, Ubuntu 24.04), and one
> sentence at the bottom: "I put the full matrix and a file-import workaround in a
> public log if anyone needs it: <link>". If it gets trimmed, the measurements are
> still in the thread.

## 8. AlternativeTo

Create a listing for otio-kit, then add it as an alternative to AutoSubs and to
"DaVinci Resolve Studio" (for the automation use case). Description: the same
paragraph used in the awesome form.

---

## Sequence

Day 1: awesome form, dev.to article, Mastodon + Bluesky.
Day 2: r/opensource, Lemmy.
Day 3: r/LocalLLaMA (separate angle, needs its own numbers, do not crosspost the same text).
Day 5+: Blackmagic forum, AlternativeTo.

Between each: check whether the previous one produced a question. Questions are the
signal to write the next post; silence is the signal to change the angle, not to
repeat it.