"""Golden-file round-trip tests for the otio-kit emitter.

The golden contract: compiling tests/golden/specimen60.yaml produces byte-stable
OTIO whose structure re-reads correctly through opentimelineio — the same
properties that survived the Free 21.1 Linux import (docs/fidelity-log.md).
"""

import json
import pathlib

import pytest
import yaml
from opentimelineio import adapters
from opentimelineio import opentime as ot
from otio_kit.emit_otio import EmitError, emit
from otio_kit.media import MediaMissingError, resolve_media
from otio_kit.spec import SpecError, load_spec

GOLDEN_DIR = pathlib.Path(__file__).parent / "golden"
GOLDEN_YAML = GOLDEN_DIR / "specimen60.yaml"
GOLDEN_OTIO = GOLDEN_DIR / "specimen60.golden.otio"


def _compile(yaml_path: pathlib.Path, out_path: pathlib.Path):
    spec = load_spec(yaml_path)
    media = resolve_media(spec)
    timeline = emit(spec, media)
    adapters.write_to_file(timeline, str(out_path), "otio_json")
    return json.loads(out_path.read_text())


def test_compile_matches_golden(tmp_path):
    out = _compile(GOLDEN_YAML, tmp_path / "out.otio")
    golden = json.loads(GOLDEN_OTIO.read_text())
    assert out == golden, "emitter output drifted from the committed golden file"


def test_roundtrip_structure(tmp_path):
    _compile(GOLDEN_YAML, tmp_path / "out.otio")
    tl = adapters.read_from_file(tmp_path / "out.otio")

    tracks = list(tl.tracks)
    assert [t.kind for t in tracks] == ["Audio", "Video", "Video"]
    assert [t.name for t in tracks] == ["A1", "V1", "V2"]

    fps = 24
    v1 = list(tracks[1])
    assert len(v1) == 4  # 3 clips + 1 transition
    clips = [c for c in v1 if c.schema_name() == "Clip"]
    assert [c.name for c in clips] == [
        "clip_a_dnx.mov", "clip_b_dnx.mov", "clip_c_dnx.mov"
    ]
    for c in clips:
        assert c.source_range.duration == ot.RationalTime(20 * fps, fps)
        assert c.media_reference.target_url.startswith("/")

    trans = [x for x in v1 if x.schema_name() == "Transition"]
    assert len(trans) == 1
    assert trans[0].transition_type == "SMPTE_Dissolve"
    assert trans[0].in_offset == ot.RationalTime(12, fps)
    assert trans[0].out_offset == ot.RationalTime(12, fps)

    # markers: clip-local, on the covering clip
    a_markers = [(m.name, m.color, m.marked_range.start_time) for m in clips[0].markers]
    assert a_markers == [("beat-1", "BLUE", ot.RationalTime(240, fps))]
    assert [(m.name, m.color) for m in clips[2].markers] == [("outro", "RED")]
    assert clips[2].markers[0].marked_range.start_time == ot.RationalTime(120, fps)

    # audio: 60 s music with stock-only fade effect carrying metadata
    a1 = list(tracks[0])
    assert len(a1) == 1 and a1[0].schema_name() == "Clip"
    assert a1[0].source_range.duration == ot.RationalTime(60 * fps, fps)
    fx = a1[0].effects
    assert len(fx) == 1
    assert fx[0].effect_name == "AudioFadeIn"
    assert fx[0].metadata["cutlist"] == {"fade": "AudioFadeIn", "duration": 48}
    # stock schema rule: effect name is not a custom OTIO schema
    assert fx[0].schema_name() == "Effect"

    assert tl.name == "specimen-60"


def test_missing_media_lists_all(tmp_path):
    (tmp_path / "media").mkdir()
    (tmp_path / "media" / "clip_a_dnx.mov").touch()
    bad = {
        "spec_version": 0, "name": "x", "fps": 24,
        "media": {"gone_a": "media/nope_a.mov", "gone_b": "media/nope_b.mov",
                  "ok": "media/clip_a_dnx.mov"},
        "timeline": {"video": [{"track": "V1", "clips": [
            {"media": "gone_a", "duration": 1.0},
            {"media": "gone_b", "duration": 1.0},
            {"media": "ok", "duration": 1.0},
        ]}]},
    }
    p = tmp_path / "bad.yaml"
    p.write_text(yaml.safe_dump(bad))
    with pytest.raises(MediaMissingError) as exc:
        resolve_media(load_spec(p))
    msg = str(exc.value)
    assert "2 media file(s) missing" in msg
    assert "nope_a.mov" in msg and "nope_b.mov" in msg


def test_schema_violation_is_loud(tmp_path):
    bad = {"spec_version": 7, "name": "x", "fps": 24, "media": {},
           "timeline": {"video": []}}
    p = tmp_path / "bad.yaml"
    p.write_text(yaml.safe_dump(bad))
    with pytest.raises(SpecError):
        load_spec(p)


def test_transition_on_first_clip_is_loud(tmp_path):
    bad = {
        "spec_version": 0, "name": "x", "fps": 24,
        "media": {"c": "media/clip_a_dnx.mov"},
        "timeline": {"video": [{"track": "V1", "clips": [
            {"media": "c", "duration": 1.0,
             "transition_in": {"type": "dissolve", "duration": 0.5}},
        ]}]},
    }
    p = tmp_path / "bad.yaml"
    p.write_text(yaml.safe_dump(bad))
    with pytest.raises(SpecError, match="nothing to transition from"):
        load_spec(p)


def test_marker_out_of_range_is_loud():
    spec = load_spec(GOLDEN_YAML)
    spec.markers = [{"time": 999.0, "color": "blue", "name": "void"}]
    media = resolve_media(spec)
    with pytest.raises(EmitError, match="beyond the first video track"):
        emit(spec, media)
