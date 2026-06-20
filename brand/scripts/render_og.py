#!/usr/bin/env python3
"""render_og.py — UI-branding OG / figure card renderer (cairosvg).

Hand-authored SVG → PNG at 1200×630 (in-content OG / figure cards, EyeRest palette).
This is the UI-branding diagram pipeline (decision D8). It is SEPARATE from repo social
previews (1280×640, GitHub branding) produced by brand/scripts/generate_social.py — same
cairosvg mechanism, different size + palette + purpose; do not merge them.

This renderer is the consolidation target for the org's scattered bash/awk SVG renderers
(qte77/qte77#112).

Usage:
  uv run --with cairosvg python render_og.py images/foo.svg            # -> images/foo.png
  uv run --with cairosvg python render_og.py images/foo.svg out.png

Authoring rules (baked in as a pre-render lint):
  * Canvas 1200×630; use EyeRest tokens (warm, zero-blue) — see brand/DESIGN.md.
  * cairosvg's fallback font lacks → ≈ ² and renders them as tofu in <text>. Use an
    en-dash, '~', and '^2' (or drawn arrow paths) instead.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import cairosvg

OG_WIDTH, OG_HEIGHT = 1200, 630

# glyphs cairosvg renders as tofu inside <text> -> safe replacements (findings/04).
TOFU = {"→": "– (en-dash) or a drawn arrow", "≈": "~", "²": "^2"}


def lint_svg(svg_path: Path) -> list[str]:
    """Warn on tofu-prone glyphs that appear inside <text> elements."""
    text = svg_path.read_text(encoding="utf-8")
    warnings = []
    for chunk in re.findall(r"<text\b[^>]*>(.*?)</text>", text, flags=re.DOTALL):
        for glyph, fix in TOFU.items():
            if glyph in chunk:
                warnings.append(f"tofu risk: {glyph!r} in <text> — use {fix}")
    return warnings


def render(svg_path: Path, png_path: Path) -> None:
    cairosvg.svg2png(
        url=str(svg_path),
        write_to=str(png_path),
        output_width=OG_WIDTH,
        output_height=OG_HEIGHT,
    )


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    svg_path = Path(argv[0])
    png_path = Path(argv[1]) if len(argv) > 1 else svg_path.with_suffix(".png")
    if not svg_path.exists():
        print(f"error: {svg_path} not found", file=sys.stderr)
        return 2

    for w in lint_svg(svg_path):
        print(f"  WARN  {w}", file=sys.stderr)

    render(svg_path, png_path)
    print(f"rendered {svg_path} -> {png_path} ({OG_WIDTH}x{OG_HEIGHT})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
