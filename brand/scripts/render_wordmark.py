# /// script
# requires-python = ">=3.11"
# dependencies = ["resvg-py>=0.1"]
# ///
"""Rasterize brand/images/logo-wordmark.paths.<font>.svg to brand/images/wordmark_{dark,light}.<font>.png at 608x320.

Reads the path-baked SVG. No font lookup at render time.

Usage:
    uv run scripts/render_wordmark.py                  # font=dejavu (default)
    uv run scripts/render_wordmark.py --font cascadia
    uv run scripts/render_wordmark.py --only light
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import resvg_py

BRAND = Path(__file__).resolve().parent.parent
IMAGES = BRAND / "images"
DEFAULT_FONT = "dejavu"
WIDTH, HEIGHT = 608, 320  # 4x the 152x80 viewBox


def to_light(svg: str) -> str:
    return (
        svg
        .replace("fill: #0d1117;", "fill: #ffffff;")
        .replace("fill: #e6edf3;", "fill: #1f2328;")
        .replace("fill: #388bfd;", "fill: #1f6feb;")
    )


def render(svg: str, dst: Path, label: str) -> None:
    png = resvg_py.svg_to_bytes(svg_string=svg, width=WIDTH, height=HEIGHT)
    dst.write_bytes(bytes(png))
    print(f"wrote {dst} ({WIDTH}x{HEIGHT}, {label})")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--font", default=DEFAULT_FONT,
                    help=f"font key suffix on the source paths SVG (default: {DEFAULT_FONT})")
    ap.add_argument("--only", choices=["dark", "light"])
    args = ap.parse_args()

    src = IMAGES / f"logo-wordmark.paths.{args.font}.svg"
    out_dark = IMAGES / f"wordmark_dark.{args.font}.png"
    out_light = IMAGES / f"wordmark_light.{args.font}.png"

    if not src.exists():
        print(
            f"missing source: {src}\nrun: make -C brand brand_paths",
            file=sys.stderr,
        )
        return 1

    svg = src.read_text()
    if args.only != "light":
        render(svg, out_dark, "dark")
    if args.only != "dark":
        render(to_light(svg), out_light, "light")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
