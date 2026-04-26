# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "resvg-py>=0.1",
#     "uharfbuzz>=0.40",
#     "fonttools>=4.50",
#     "defusedxml>=0.7",
# ]
# ///
"""Rasterize brand/logo-mark.svg to brand/avatar_{dark,light}.png at 920x920.

The canonical SVG keeps its <text> element (font-driven, editable). For
rasterization we derive an in-memory path-only SVG via
scripts/svg_text_to_paths.py — uharfbuzz shapes the text exactly as
browsers do, and fontTools extracts glyph outlines as SVG paths. resvg
then renders those paths predictably; the PNG matches what a browser
would draw.

Light variant is produced by substituting the three fill values to match
the SVG's @media (prefers-color-scheme: light) block, since resvg has
no browser color-scheme context.

GitHub avatars are static — viewer theme does not switch them. We render
both variants so you can pick which one to upload (Settings -> Profile
-> Change avatar; UI-only per docs/gh-endpoints/INDEX row 3).

Usage:
    uv run scripts/render_avatar.py            # writes both variants
    uv run scripts/render_avatar.py --only light
    uv run scripts/render_avatar.py --only dark
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# scripts/ on sys.path so we can import the sibling module.
sys.path.insert(0, str(Path(__file__).resolve().parent))

import resvg_py
from svg_text_to_paths import text_to_paths

BRAND = Path(__file__).resolve().parent.parent
SRC = BRAND / "logo-mark.svg"
OUT_DARK = BRAND / "avatar_dark.png"
OUT_LIGHT = BRAND / "avatar_light.png"
FONTS_DIR = BRAND / "fonts"
SIZE = 920  # 2x of GitHub's 460 minimum, crisp at all display sizes


def to_light(svg: str) -> str:
    """Promote the SVG's @media (prefers-color-scheme: light) values to
    defaults so resvg renders the light variant.
    """
    return (
        svg
        .replace("fill: #0d1117;", "fill: #ffffff;")  # bg
        .replace("fill: #e6edf3;", "fill: #1f2328;")  # fg
        .replace("fill: #388bfd;", "fill: #1f6feb;")  # accent
    )


def render(svg: str, dst: Path, label: str) -> None:
    png = resvg_py.svg_to_bytes(
        svg_string=svg,
        width=SIZE,
        height=SIZE,
        font_dirs=[str(FONTS_DIR)],
    )
    dst.write_bytes(bytes(png))
    print(f"wrote {dst} ({SIZE}x{SIZE}, {label})")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--only",
        choices=["dark", "light"],
        help="render only one variant (default: render both)",
    )
    args = ap.parse_args()

    if not SRC.exists():
        print(f"missing source: {SRC}", file=sys.stderr)
        return 1
    if not FONTS_DIR.exists() or not any(FONTS_DIR.glob("*.ttf")):
        print(
            f"missing fonts: {FONTS_DIR}\n"
            f"run: uv run scripts/install_fonts.py",
            file=sys.stderr,
        )
        return 1

    # Convert canonical text SVG to a path-only derivative for predictable
    # rasterization. uharfbuzz handles shaping the same way browsers do.
    font = FONTS_DIR / "JetBrainsMono-Bold.ttf"
    if not font.exists():
        print(f"missing font: {font}", file=sys.stderr)
        return 1
    svg = text_to_paths(SRC.read_text(), font)

    if args.only != "light":
        render(svg, OUT_DARK, "dark")
    if args.only != "dark":
        render(to_light(svg), OUT_LIGHT, "light")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
