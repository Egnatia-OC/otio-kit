#!/usr/bin/env python3
"""Render the specimen title still card (title.png).

Reproduces the exact 5-second title card used in the task-0.2 fidelity
specimen:

  - 1920x1080 solid black
  - "SPECIMEN 60"  — DejaVu Sans Bold 110, white, centred, baseline y=480
  - "task 0.2 fidelity specimen - 24 fps - 60 s" — DejaVu Sans 40, #cccccc, y=600

Usage:
  python make_title.py [output.png]      # default: title.png next to this file

Requires: pillow        (pip install pillow)
Font:     DejaVu Sans — the script searches common system locations and
          falls back to PIL's built-in font if none is found (the card is a
          conformed still; exact glyph metrics are not load-bearing).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

W, H = 1920, 1080
TITLE = "SPECIMEN 60"
SUBTITLE = "task 0.2 fidelity specimen - 24 fps - 60 s"
TITLE_Y, SUBTITLE_Y = 480, 600
TITLE_FILL = (255, 255, 255)
SUBTITLE_FILL = (0xCC, 0xCC, 0xCC)

_FONT_CANDIDATES = {
    "DejaVuSans-Bold.ttf": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
        os.path.expanduser("~/.local/share/fonts/DejaVuSans-Bold.ttf"),
        "C:/Windows/Fonts/DejaVuSans-Bold.ttf",
    ],
    "DejaVuSans.ttf": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans.ttf",
        os.path.expanduser("~/.local/share/fonts/DejaVuSans.ttf"),
        "C:/Windows/Fonts/DejaVuSans.ttf",
    ],
}


def _load_font(fname: str, size: int):
    from PIL import ImageFont
    for path in _FONT_CANDIDATES[fname]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    try:
        return ImageFont.load_default(size=size)  # Pillow >= 9.2
    except TypeError:
        return ImageFont.load_default()


def render(out_path: str) -> None:
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(img)
    jobs = [
        (TITLE, _load_font("DejaVuSans-Bold.ttf", 110), TITLE_Y, TITLE_FILL),
        (SUBTITLE, _load_font("DejaVuSans.ttf", 40), SUBTITLE_Y, SUBTITLE_FILL),
    ]
    for text, font, y, fill in jobs:
        bbox = d.textbbox((0, 0), text, font=font)
        left = (W - (bbox[2] - bbox[0])) // 2 - bbox[0]
        d.text((left, y), text, font=font, fill=fill)
    img.save(out_path)


def main() -> None:
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "title.png")
    render(out)
    print(f"OK: wrote {out} ({W}x{H})")


if __name__ == "__main__":
    main()
