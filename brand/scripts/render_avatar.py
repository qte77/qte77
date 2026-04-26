# /// script
# requires-python = ">=3.11"
# dependencies = ["resvg-py>=0.1"]
# ///
"""Rasterize brand/images/logo-mark.paths.<font>.svg to brand/images/avatar_{dark,light,neutral}.<font>.png at 920x920.

Reads the path-baked SVG (font geometry already converted to <path>
elements). No font lookup needed at render time — geometry is pure
and renders identically across all consumers.

Light variant substitutes the three fill values to match the SVG's
@media (prefers-color-scheme: light) block, since resvg has no browser
color-scheme context.

Neutral variant drops the background rect and recolors glyph + accent
to a single mid-tone gray (#808080), giving a transparent avatar that
reads acceptably on both dark and light GitHub themes (~4:1 contrast
on either) without leaning into the brand-blue palette.

Usage:
    uv run scripts/render_avatar.py                  # font=dejavu (default), all 3 variants
    uv run scripts/render_avatar.py --font cascadia  # use a different bake
    uv run scripts/render_avatar.py --only light
    uv run scripts/render_avatar.py --only neutral
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import resvg_py

BRAND = Path(__file__).resolve().parent.parent
IMAGES = BRAND / "images"
DEFAULT_FONT = "dejavu"
SIZE = 920  # 2x of GitHub's 460 minimum, crisp at all display sizes
NEUTRAL_GRAY = "#808080"


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


def to_neutral(svg: str) -> str:
    """Drop the background rect and recolor fg + accent to a single
    mid-tone gray. Produces a transparent PNG that works on either
    GitHub theme without leaning into the brand-blue palette.
    """
    svg = re.sub(r'\s*<rect class="mark-bg"[^/]*/>\s*', "\n  ", svg)
    return (
        svg
        .replace("fill: #e6edf3;", f"fill: {NEUTRAL_GRAY};")
        .replace("fill: #388bfd;", f"fill: {NEUTRAL_GRAY};")
    )


def render(svg: str, dst: Path, label: str) -> None:
    png = resvg_py.svg_to_bytes(svg_string=svg, width=SIZE, height=SIZE)
    dst.write_bytes(bytes(png))
    print(f"wrote {dst} ({SIZE}x{SIZE}, {label})")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--font", default=DEFAULT_FONT,
                    help=f"font key suffix on the source paths SVG (default: {DEFAULT_FONT})")
    ap.add_argument("--only", choices=["dark", "light", "neutral"])
    args = ap.parse_args()

    src = IMAGES / f"logo-mark.paths.{args.font}.svg"
    out_dark = IMAGES / f"avatar_dark.{args.font}.png"
    out_light = IMAGES / f"avatar_light.{args.font}.png"
    out_neutral = IMAGES / f"avatar_neutral.{args.font}.png"

    if not src.exists():
        print(
            f"missing source: {src}\nrun: make -C brand brand_paths",
            file=sys.stderr,
        )
        return 1

    svg = src.read_text()
    if args.only in (None, "dark"):
        render(svg, out_dark, "dark")
    if args.only in (None, "light"):
        render(to_light(svg), out_light, "light")
    if args.only in (None, "neutral"):
        render(to_neutral(svg), out_neutral, "neutral")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
