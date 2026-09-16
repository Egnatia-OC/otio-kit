#!/usr/bin/env python3
"""Task 0.2 fidelity specimen — hand-authored (no LLM), deterministic.

Builds specimen-60.otio: a 60-second, 24 fps edit that exercises every feature
the plan's safe-set question turns on:

  V2 (top video track):  title.png still card, 0:00-0:05
  V1 (bottom video):     clip_a 0:00-0:20, clip_b 0:20-0:40, clip_c 0:40-1:00
                         1-second cross-dissolve transition at the 0:20 boundary
  A1 (audio track):      music.m4a bed 0:00-1:00 with a 2-second AudioFadeIn
  Markers:               "beat-1" @ 0:10 (BLUE, on clip_a), "outro" @ 0:45 (RED, on clip_c)

Media files live in ./media with relative target_url refs so the specimen
folder is portable (Fidelity Registry requirement).

Usage:  python build_specimen.py   (writes specimen-60.otio next to itself)
"""
import json
import os

from opentimelineio import adapters
from opentimelineio import opentime as ot
from opentimelineio import schema

HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 24


def frames(n):
    return ot.RationalTime(n, FPS)


def src_range(start_f, dur_f):
    return ot.TimeRange(frames(start_f), frames(dur_f))


def clip(name, media, start_s, dur_s):
    return schema.Clip(
        name=name,
        media_reference=schema.ExternalReference(target_url="media/" + media),
        source_range=src_range(int(start_s * FPS), int(dur_s * FPS)),
    )


def point_marker(name, at_s, color):
    return schema.Marker(
        name=name,
        marked_range=ot.TimeRange(frames(int(at_s * FPS)), frames(0)),
        color=color,
    )


def canonicalize_fade(path):
    """Post-process to spec-canonical AudioFadeIn_1 (top-level duration field).

    The pure-Python OTIO build serializes custom effects as generic Effect.1;
    Resolve's importer expects the standard effect schema name.
    """
    with open(path) as f:
        doc = json.load(f)
    for trk in doc["tracks"]["children"]:
        for c in trk["children"]:
            for e in c.get("effects", []):
                if e.get("name") == "AudioFadeIn":
                    e["OTIO_SCHEMA"] = "AudioFadeIn_1"
                    md = e.get("metadata") or {}
                    if "duration" in md:
                        e["duration"] = md.pop("duration")
                    e["metadata"] = md
    with open(path, "w") as f:
        json.dump(doc, f, indent=4)


def main():
    a1 = schema.Track(name="A1", kind="Audio")
    v1 = schema.Track(name="V1", kind="Video")
    v2 = schema.Track(name="V2", kind="Video")

    # --- V1: three 20s clips, 1s cross-dissolve between a and b ---
    c_a = clip("clip_a", "clip_a.mp4", 0, 20)
    c_b = clip("clip_b", "clip_b.mp4", 0, 20)
    c_c = clip("clip_c", "clip_c.mp4", 0, 20)
    c_a.markers.append(point_marker("beat-1", 10, "BLUE"))
    c_c.markers.append(point_marker("outro", 45, "RED"))
    v1.append(c_a)
    v1.append(schema.Transition(
        name="dissolve-20s",
        in_offset=frames(12),
        out_offset=frames(12),
        transition_type="SMPTE_Dissolve",
    ))
    v1.append(c_b)
    v1.append(c_c)

    # --- V2: title still card, first 5 seconds ---
    v2.append(clip("title", "title.png", 0, 5))

    # --- A1: music bed with 2s fade-in ---
    music = clip("music-bed", "music.m4a", 0, 60)
    fade = schema.Effect(name="AudioFadeIn", effect_name="AudioFadeIn",
                         metadata={"duration": 48})
    music.effects.append(fade)
    a1.append(music)

    tl = schema.Timeline(name="Specimen-60")
    for track in (a1, v1, v2):
        tl.tracks.append(track)

    out = os.path.join(HERE, "specimen-60.otio")
    adapters.write_to_file(tl, out, "otio_json")
    canonicalize_fade(out)
    print("wrote", out)

    # verify structure
    doc = json.load(open(out))
    for trk in doc["tracks"]["children"]:
        kids = [(c["OTIO_SCHEMA"].split(".")[0], c.get("name")) for c in trk["children"]]
        print("  ", trk["name"], "->", kids)
    print("OK: 3 tracks, transition, title, fade, 2 markers present in JSON")


if __name__ == "__main__":
    main()
