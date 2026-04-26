# /// script
# requires-python = ">=3.11"
# dependencies = ["uharfbuzz>=0.40", "fonttools>=4.50", "defusedxml>=0.7"]
# ///
"""Replace <text> elements in an SVG with equivalent <path> elements.

Why: SVG renderers disagree on text shaping and OpenType feature handling.
By converting text into geometry up-front, every renderer (browsers, resvg,
cairosvg, librsvg) produces pixel-identical output. The canonical SVG keeps
its <text> element for editing; this script produces a derived path-only
SVG suitable for rasterization.

Implementation:
- uharfbuzz shapes the text exactly as browsers do (HarfBuzz is what
  Chromium and Firefox use), applying font-feature-settings.
- fontTools extracts glyph outlines as SVG path data.
- Output is the original SVG with each <text> element replaced by a
  <g> of <path> elements, preserving class attributes for styling.

Usage as module:
    new_svg = text_to_paths(svg_string, font_path)

Usage as CLI (stdin -> stdout):
    cat brand/images/logo-mark.svg | uv run scripts/svg_text_to_paths.py \\
        --font brand/fonts/JetBrainsMono-Bold.ttf > out.svg
"""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# defusedxml hardens stdlib XML parsers against billion-laughs / external-entity
# attacks. We only feed our own canonical SVGs through this code, but the
# hardening is free.
from defusedxml.ElementTree import fromstring as safe_fromstring

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)


def _parse_features(attr: str | None) -> dict[str, int]:
    """Parse e.g. \"'onum' 1\" -> {'onum': 1}."""
    if not attr:
        return {}
    return {tag: int(val) for tag, val in re.findall(r"'(\w+)'\s+(\d)", attr)}


def _shape(hb_font: hb.Font, text: str, features: dict[str, int]) -> tuple:
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(hb_font, buf, features)
    return buf.glyph_infos, buf.glyph_positions


def _glyph_path(glyph_set, ttfont: TTFont, gid: int) -> str:
    name = ttfont.getGlyphName(gid)
    pen = SVGPathPen(glyph_set)
    glyph_set[name].draw(pen)
    return pen.getCommands()


def _convert_text_element(text_el: ET.Element, hb_font: hb.Font, ttfont: TTFont) -> ET.Element:
    glyph_set = ttfont.getGlyphSet()
    upem = ttfont["head"].unitsPerEm

    x = float(text_el.get("x", 0))
    y = float(text_el.get("y", 0))
    font_size = float(text_el.get("font-size", 16))
    anchor = text_el.get("text-anchor", "start")
    features = _parse_features(text_el.get("font-feature-settings"))
    scale = font_size / upem

    # First pass: shape every tspan, collect glyph data + total advance
    runs: list[tuple[float, float, list[tuple[int, float, float]]]] = []
    total_advance = 0.0
    cursor_x = 0.0
    cursor_y = 0.0  # relative to baseline y

    for tspan in text_el.findall(f"{{{SVG_NS}}}tspan"):
        cls = tspan.get("class", "")
        dy = float(tspan.get("dy", 0))
        cursor_y += dy
        text = tspan.text or ""
        infos, positions = _shape(hb_font, text, features)
        glyphs: list[tuple[int, float, float]] = []
        for info, pos in zip(infos, positions):
            gx = cursor_x + pos.x_offset * scale
            gy = cursor_y - pos.y_offset * scale
            glyphs.append((info.codepoint, gx, gy))
            cursor_x += pos.x_advance * scale
        run_advance = cursor_x  # cumulative
        runs.append((run_advance, cls, glyphs))
        total_advance = cursor_x

    # Compute anchor offset
    if anchor == "middle":
        offset_x = x - total_advance / 2
    elif anchor == "end":
        offset_x = x - total_advance
    else:
        offset_x = x

    # Build replacement <g>
    g = ET.Element(f"{{{SVG_NS}}}g")
    for _, cls, glyphs in runs:
        for gid, gx, gy in glyphs:
            d = _glyph_path(glyph_set, ttfont, gid)
            if not d:
                continue
            attrs = {
                "d": d,
                "transform": (
                    f"translate({offset_x + gx:.4f},{y + gy:.4f}) "
                    f"scale({scale:.6f},{-scale:.6f})"
                ),
            }
            if cls:
                attrs["class"] = cls
            ET.SubElement(g, f"{{{SVG_NS}}}path", attrs)
    return g


def text_to_paths(svg_string: str, font_path: Path) -> str:
    """Return a new SVG with all <text> elements replaced by <path> equivalents."""
    blob = hb.Blob.from_file_path(str(font_path))
    face = hb.Face(blob)
    hb_font = hb.Font(face)
    ttfont = TTFont(str(font_path))

    root = safe_fromstring(svg_string)
    # Find all text elements (one or more)
    for parent in root.iter():
        for i, child in enumerate(list(parent)):
            if child.tag == f"{{{SVG_NS}}}text":
                replacement = _convert_text_element(child, hb_font, ttfont)
                parent.remove(child)
                parent.insert(i, replacement)
    return ET.tostring(root, encoding="unicode")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--font", required=True, type=Path, help="path to .ttf/.otf")
    args = ap.parse_args()
    if not args.font.exists():
        print(f"font not found: {args.font}", file=sys.stderr)
        return 1
    svg = sys.stdin.read()
    sys.stdout.write(text_to_paths(svg, args.font))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
