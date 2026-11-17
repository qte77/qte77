"""WCAG 2.x contrast helpers shared by the brand generators (stdlib only).

A mark that carries state on its own (focus ring, cursor, active tab, progress
bar) needs 3:1 against its background (WCAG 1.4.11 non-text contrast). `primary`
is the brand's pointing colour, but in some variants it is too faint for that on
the dark background; `link` is the hue-true, text-safe reading of `primary` (see
DESIGN.md "Colors"), so indicators fall back to it there (#214).
"""

from __future__ import annotations

INDICATOR_MIN_RATIO = 3.0


def _channel(value: int) -> float:
    c = value / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _channel(r) + 0.7152 * _channel(g) + 0.0722 * _channel(b)


def contrast_ratio(fg: str, bg: str) -> float:
    """WCAG 2.x contrast ratio of two #rrggbb colours (1.0 to 21.0)."""
    hi, lo = sorted((relative_luminance(fg), relative_luminance(bg)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def indicator_color(primary: str, link: str, bg: str) -> str:
    """Colour for a state indicator: `primary` if it reaches 3:1 on `bg`, else `link`."""
    return primary if contrast_ratio(primary, bg) >= INDICATOR_MIN_RATIO else link
