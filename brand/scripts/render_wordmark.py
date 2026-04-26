# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "resvg-py>=0.1",
#     "uharfbuzz>=0.40",
#     "fonttools>=4.50",
#     "defusedxml>=0.7",
# ]
# ///
"""Rasterize brand/images/logo-wordmark.svg to brand/images/wordmark_{dark,light}.png at 960x320.

Same pipeline as render_avatar.py: canonical text SVG -> in-memory path
SVG via uharfbuzz + fontTools -> resvg. Output is JBM Bold geometry,
renderer-agnostic, no font-fallback risk on consumer surfaces.

Usage:
    uv run scripts/render_wordmark.py            # writes both variants
    uv run scripts/render_wordmark.py --only light
    uv run scripts/render_wordmark.py --only dark
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import resvg_py
from svg_text_to_paths import text_to_paths

BRAND = Path(__file__).resolve().parent.parent
IMAGES = BRAND / "images"
SRC = IMAGES / "logo-wordmark.svg"
OUT_DARK = IMAGES / "wordmark_dark.png"
OUT_LIGHT = IMAGES / "wordmark_light.png"
FONTS_DIR = BRAND / "fonts"
WIDTH, HEIGHT = 960, 320  # 4x the 240x80 viewBox


def to_light(svg: str) -> str:
    return (
        svg
        .replace("fill: #0d1117;", "fill: #ffffff;")
        .replace("fill: #e6edf3;", "fill: #1f2328;")
        .replace("fill: #388bfd;", "fill: #1f6feb;")
    )


def render(svg: str, dst: Path, label: str) -> None:
    png = resvg_py.svg_to_bytes(
        svg_string=svg,
        width=WIDTH,
        height=HEIGHT,
        font_dirs=[str(FONTS_DIR)],
    )
    dst.write_bytes(bytes(png))
    print(f"wrote {dst} ({WIDTH}x{HEIGHT}, {label})")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=["dark", "light"])
    args = ap.parse_args()

    if not SRC.exists():
        print(f"missing source: {SRC}", file=sys.stderr)
        return 1
    font = FONTS_DIR / "JetBrainsMono-Bold.ttf"
    if not font.exists():
        print(
            f"missing font: {font}\nrun: uv run scripts/install_fonts.py",
            file=sys.stderr,
        )
        return 1

    svg = text_to_paths(SRC.read_text(), font)

    if args.only != "light":
        render(svg, OUT_DARK, "dark")
    if args.only != "dark":
        render(to_light(svg), OUT_LIGHT, "light")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
