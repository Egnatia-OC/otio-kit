"""OTIO emitter: spec -> .otio.

Locked rules from the Free 21.1 Linux fidelity log (docs/fidelity-log.md):

1. STOCK SCHEMAS ONLY. The importer fatals on unknown schemas (our custom
   AudioFadeIn_1 killed it). Custom semantics ride in Effect/metadata.
2. target_url is an EXISTING ABSOLUTE PATH. Bare relative URLs misresolve in
   the Linux importer's media conform.
3. Markers attach to the first-video-track clip covering their time, with
   clip-local marked_range (the specimen's track-time value exceeded the
   carrying clip on outro@45s and Resolve dropped it).
"""

import pathlib

from opentimelineio import adapters, schema
from opentimelineio import opentime as ot

MARKER_COLORS = {
    "blue": schema.MarkerColor.BLUE,
    "red": schema.MarkerColor.RED,
    "green": schema.MarkerColor.GREEN,
    "yellow": schema.MarkerColor.YELLOW,
    "pink": schema.MarkerColor.PINK,
    "purple": schema.MarkerColor.PURPLE,
    "cyan": schema.MarkerColor.CYAN,
    "white": schema.MarkerColor.WHITE,
}


class EmitError(ValueError):
    """Emitter semantic failure. Message is user-facing."""


def _rt(seconds: float, fps: float) -> ot.RationalTime:
    return ot.RationalTime(round(seconds * fps), fps)


def emit(spec, media: dict[str, str]) -> schema.Timeline:
    """Build a Timeline from a validated Spec and resolved media paths."""
    fps = spec.fps
    timeline = schema.Timeline(name=spec.name)
    names = [t["track"] for t in spec.timeline.get("audio", [])] + [
        t["track"] for t in spec.timeline.get("video", [])]
    dupes = sorted({n for n in names if names.count(n) > 1})
    if dupes:
        raise EmitError(
            f"duplicate track name(s): {', '.join(dupes)} — "
            "track names must be unique"
        )


    # Track order mirrors the proven-known-good specimen: audio first, then
    # video in declared order.
    for audio_track in spec.timeline.get("audio", []):
        track = schema.Track(name=audio_track["track"], kind="Audio")
        for clip_spec in audio_track["clips"]:
            clip = _make_clip(clip_spec, media, fps)
            fade = clip_spec.get("fade_in", 0)
            if fade > 0:
                # Stock Effect only; semantics in metadata (fidelity rule 1).
                clip.effects.append(
                    schema.Effect(
                        name="AudioFadeIn",
                        effect_name="AudioFadeIn",
                        metadata={"cutlist": {"fade": "AudioFadeIn",
                                              "duration": round(fade * fps)}},
                    )
                )
            track.append(clip)
        timeline.tracks.append(track)

    for video_track in spec.timeline.get("video", []):
        track = schema.Track(name=video_track["track"], kind="Video")
        for i, clip_spec in enumerate(video_track["clips"]):
            if i > 0:
                tr = clip_spec.get("transition_in")
                if tr:
                    frames = round(tr["duration"] * fps)
                    if frames < 2:
                        raise EmitError(
                            f"transition duration {tr['duration']}s rounds to "
                            f"{frames} frame(s) at {fps} fps; minimum is 2 frames"
                        )
                    half = frames // 2
                    track.append(
                        schema.Transition(
                            name=f"{tr['type']}_{i}",
                            in_offset=ot.RationalTime(half, fps),
                            out_offset=ot.RationalTime(frames - half, fps),
                            transition_type="SMPTE_Dissolve",
                        )
                    )
            track.append(_make_clip(clip_spec, media, fps))
        timeline.tracks.append(track)

    _attach_markers(timeline, spec.markers, fps)
    return timeline


def _attach_markers(timeline: schema.Timeline, marker_specs: list, fps: float) -> None:
    """Attach markers to the first-video-track clip covering each time.

    marked_range is clip-local (valid inside the carrying clip). Track order
    mirrors the proven specimen layout: Resolve imports clip-level markers.
    """
    if not marker_specs:
        return

    video_tracks = [t for t in timeline.tracks
                    if isinstance(t, schema.Track) and t.kind == "Video"]
    if not video_tracks:
        raise EmitError("markers require at least one video track")
    clips = [c for c in video_tracks[0] if isinstance(c, schema.Clip)]
    if not clips:
        raise EmitError("markers require at least one clip on the first video track")

    for marker_spec in marker_specs:
        target = _rt(marker_spec["time"], fps)
        track_time = ot.RationalTime(0, fps)
        placed = False
        for clip in clips:
            clip_len = clip.source_range.duration
            clip_end = track_time + clip_len
            if track_time <= target < clip_end:
                clip_local = clip.source_range.start_time + (target - track_time)
                clip.markers.append(
                    schema.Marker(
                        name=marker_spec.get("name", ""),
                        marked_range=ot.TimeRange(clip_local, ot.RationalTime(0, fps)),
                        color=MARKER_COLORS[marker_spec["color"]],
                    )
                )
                placed = True
                break
            track_time = clip_end
        if not placed:
            raise EmitError(
                f"marker at {marker_spec['time']}s lies beyond the first video track"
            )


def _make_clip(clip_spec: dict, media: dict[str, str], fps: float) -> schema.Clip:
    target = media[clip_spec["media"]]
    frames = round(clip_spec["duration"] * fps)
    if frames < 1:
        raise EmitError(
            f"clip '{pathlib.Path(target).name}' duration "
            f"{clip_spec['duration']}s rounds to {frames} frame(s) at "
            f"{fps} fps; minimum is {1.0 / fps:.4f}s (1 frame)"
        )
    return schema.Clip(
        name=pathlib.Path(target).name,
        media_reference=schema.ExternalReference(target_url=target),
        source_range=ot.TimeRange(
            ot.RationalTime(0, fps), ot.RationalTime(frames, fps)
        ),
    )


def write_otio(timeline: schema.Timeline, out_path: str | pathlib.Path) -> pathlib.Path:
    out = pathlib.Path(out_path)
    adapters.write_to_file(timeline, str(out), "otio_json")
    return out
