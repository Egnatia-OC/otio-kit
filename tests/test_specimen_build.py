"""Smoke tests: the specimen reproduction recipe works on a clean checkout.

These catch the doc/code divergence class — a `specimen/BUILD.md` that claims
outputs its commands don't actually produce (the §10 finding). Each test runs
the documented build step and asserts the artefact it promises.

The DNxHR transcode step is intentionally NOT run here (~290 MB per 20 s
clip); it is verified manually per BUILD.md §2 and is size-limited by design.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SPECIMEN = Path(__file__).resolve().parent.parent / "specimen"


def _has_pil() -> bool:
    try:
        import PIL  # noqa: F401
        return True
    except ImportError:
        return False


NEEDS_FFMPEG = pytest.mark.skipif(shutil.which("ffmpeg") is None,
                                  reason="ffmpeg not available")
NEEDS_PIL = pytest.mark.skipif(not _has_pil(), reason="pillow not installed")


@NEEDS_FFMPEG
def test_media_synthesis_produces_documented_outputs(tmp_path):
    # The H.264 ffmpeg block from specimen/BUILD.md §1, run on a clean dir.
    cmds = [
        ["-f", "lavfi", "-i", "testsrc=size=1920x1080:rate=24:duration=20",
         "-f", "lavfi", "-i", "sine=frequency=440:duration=20",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
         "-shortest", "clip_a.mp4"],
        ["-f", "lavfi", "-i", "smptebars=size=1920x1080:rate=24:duration=20",
         "-f", "lavfi", "-i", "sine=frequency=554:duration=20",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
         "-shortest", "clip_b.mp4"],
        ["-f", "lavfi", "-i", "testsrc2=size=1920x1080:rate=24:duration=20",
         "-f", "lavfi", "-i", "sine=frequency=659:duration=20",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
         "-shortest", "clip_c.mp4"],
        ["-f", "lavfi", "-i", "aevalsrc='0.30*sin(2*PI*220*t)+0.22*sin(2*PI*277.18*t)+0.12*sin(2*PI*329.63*t)':s=48000:d=60", "-c:a", "aac", "music.m4a"],
    ]
    for args in cmds:
        subprocess.run(["ffmpeg", "-y", *args], cwd=tmp_path, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for name in ("clip_a.mp4", "clip_b.mp4", "clip_c.mp4", "music.m4a"):
        p = tmp_path / name
        assert p.exists() and p.stat().st_size > 0, f"missing {name}"
    # The documented H.264 variant: clip_a must actually be h264.
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=codec_name", "-of", "csv=p=0",
         str(tmp_path / "clip_a.mp4")],
        check=True, capture_output=True, text=True)
    assert "h264" in probe.stdout


@NEEDS_PIL
def test_title_renders(tmp_path):
    out = tmp_path / "title.png"
    subprocess.run([sys.executable, str(SPECIMEN / "make_title.py"), str(out)],
                   check=True)
    assert out.exists() and out.stat().st_size > 0
    from PIL import Image
    with Image.open(out) as im:
        assert im.size == (1920, 1080)


def test_timeline_builds(tmp_path):
    # build_specimen.py writes next to itself; copy it into tmp to keep the
    # working tree clean.
    src = SPECIMEN / "build_specimen.py"
    dst = tmp_path / "build_specimen.py"
    dst.write_text(src.read_text())
    subprocess.run([sys.executable, str(dst)], check=True,
                   stdout=subprocess.DEVNULL)
    otio = tmp_path / "specimen-60.otio"
    assert otio.exists() and otio.stat().st_size > 0
    tracks = json.loads(otio.read_text())["tracks"]["children"]
    assert len(tracks) == 3
    assert {t["kind"] for t in tracks} == {"Audio", "Video"}
    v1 = next(t for t in tracks if t["name"] == "V1")
    assert any(c["OTIO_SCHEMA"].startswith("Transition")
               for c in v1["children"])
