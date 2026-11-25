# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6.0"]
# ///
"""Unit tests for brand/scripts/contrast.py — state indicators reach 3:1 (see #214).

Usage:
    uv run tests/test_brand_contrast.py
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys
import unittest

SCRIPTS = pathlib.Path(__file__).resolve().parent.parent / "brand" / "scripts"
sys.path.insert(0, str(SCRIPTS))


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


contrast = _load("contrast")
gen_vscode_theme = _load("gen_vscode_theme")


class ContrastRatioTests(unittest.TestCase):
    def test_extremes_and_identity(self):
        self.assertAlmostEqual(contrast.contrast_ratio("#000000", "#ffffff"), 21.0, places=2)
        self.assertAlmostEqual(contrast.contrast_ratio("#3a6a3a", "#3a6a3a"), 1.0, places=2)

    def test_green_dark_values_from_the_issue(self):
        # #214: dark-primary on dark-bg is 2.90:1, dark-link is 5.26:1
        self.assertAlmostEqual(contrast.contrast_ratio("#3a6a3a", "#0c1610"), 2.90, places=2)
        self.assertAlmostEqual(contrast.contrast_ratio("#539853", "#0c1610"), 5.26, places=2)


class IndicatorColorTests(unittest.TestCase):
    def test_primary_below_3_to_1_falls_back_to_link(self):
        self.assertEqual(contrast.indicator_color("#3a6a3a", "#539853", "#0c1610"), "#539853")

    def test_primary_at_or_above_3_to_1_is_kept(self):
        self.assertEqual(contrast.indicator_color("#c8a858", "#c8a858", "#1a1610"), "#c8a858")

    def test_every_variant_and_scheme_indicator_reaches_3_to_1(self):
        spec = gen_vscode_theme.load_design()
        for key, _name, colors in gen_vscode_theme._profiles(spec):
            for dark in (False, True):
                prefix = "dark-" if dark else ""
                bg = colors[f"{prefix}bg"]
                chosen = contrast.indicator_color(
                    colors[f"{prefix}primary"], colors[f"{prefix}link"], bg
                )
                with self.subTest(variant=key, dark=dark):
                    self.assertGreaterEqual(contrast.contrast_ratio(chosen, bg), 3.0)


def _lab(hex_color: str) -> tuple[float, float, float]:
    r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    r, g, b = (((c + 0.055) / 1.055) ** 2.4 if c > 0.04045 else c / 12.92 for c in (r, g, b))
    x, y, z = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047, 0.2126 * r + 0.7152 * g + 0.0722 * b, (
        0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    f = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    return 116 * f(y) - 16, 500 * (f(x) - f(y)), 200 * (f(y) - f(z))


def _delta_e76(a: str, b: str) -> float:
    return sum((p - q) ** 2 for p, q in zip(_lab(a), _lab(b))) ** 0.5


class DataArcTests(unittest.TestCase):
    """#213: a chart colour must not read as a variant's accent (>= 15 dE76) and must stay visible (3:1)."""

    def test_data_arc_is_distinct_from_every_primary_and_visible(self):
        spec = gen_vscode_theme.load_design()
        for key, _name, colors in gen_vscode_theme._profiles(spec):
            for dark, arc in ((False, spec["data"]), (True, spec["data-dark"])):
                prefix = "dark-" if dark else ""
                for role, hex_color in arc.items():
                    with self.subTest(variant=key, dark=dark, role=role):
                        self.assertGreaterEqual(_delta_e76(hex_color, colors[f"{prefix}primary"]), 15.0)
                        for surface in ("bg", "surface"):
                            self.assertGreaterEqual(
                                contrast.contrast_ratio(hex_color, colors[f"{prefix}{surface}"]), 3.0
                            )


def _delta_e2000(lab1: tuple[float, float, float], lab2: tuple[float, float, float]) -> float:
    """CIEDE2000 (Sharma, Wu, Dalal 2005) between two CIELAB colours; stdlib only."""
    import math

    l1, a1, b1 = lab1
    l2, a2, b2 = lab2
    c_bar = ((math.hypot(a1, b1) + math.hypot(a2, b2)) / 2) ** 7
    g = 0.5 * (1 - math.sqrt(c_bar / (c_bar + 25 ** 7)))
    a1p, a2p = (1 + g) * a1, (1 + g) * a2
    c1, c2 = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1 = math.degrees(math.atan2(b1, a1p)) % 360 if c1 else 0.0
    h2 = math.degrees(math.atan2(b2, a2p)) % 360 if c2 else 0.0
    dl, dc = l2 - l1, c2 - c1
    if c1 * c2 == 0:
        dh = 0.0
    else:
        dh = h2 - h1
        dh -= 360 if dh > 180 else 0
        dh += 360 if dh < -180 else 0
    dhh = 2 * math.sqrt(c1 * c2) * math.sin(math.radians(dh) / 2)
    lp, cp = (l1 + l2) / 2, (c1 + c2) / 2
    if c1 * c2 == 0:
        hp = h1 + h2
    elif abs(h1 - h2) <= 180:
        hp = (h1 + h2) / 2
    else:
        hp = (h1 + h2 + (360 if h1 + h2 < 360 else -360)) / 2
    t = (1 - 0.17 * math.cos(math.radians(hp - 30)) + 0.24 * math.cos(math.radians(2 * hp))
         + 0.32 * math.cos(math.radians(3 * hp + 6)) - 0.20 * math.cos(math.radians(4 * hp - 63)))
    sl = 1 + 0.015 * (lp - 50) ** 2 / math.sqrt(20 + (lp - 50) ** 2)
    sc, sh = 1 + 0.045 * cp, 1 + 0.015 * cp * t
    rc = 2 * math.sqrt(cp ** 7 / (cp ** 7 + 25 ** 7))
    rt = -math.sin(math.radians(60 * math.exp(-(((hp - 275) / 25) ** 2)))) * rc
    return math.sqrt((dl / sl) ** 2 + (dc / sc) ** 2 + (dhh / sh) ** 2 + rt * (dc / sc) * (dhh / sh))


class DeltaE2000Tests(unittest.TestCase):
    def test_matches_sharma_reference_pairs(self):
        # Sharma et al. 2005 test data, pairs 1, 7 and 17 (published to 4 places).
        cases = (
            ((50.0, 2.6772, -79.7751), (50.0, 0.0, -82.7485), 2.0425),
            ((50.0, 2.5, 0.0), (50.0, 0.0, -2.5), 4.3065),
            ((60.2574, -34.0099, 36.2677), (60.4626, -34.1751, 39.4387), 1.2644),
        )
        for lab1, lab2, expected in cases:
            self.assertAlmostEqual(_delta_e2000(lab1, lab2), expected, places=3)


class DataArcSeparationTests(unittest.TestCase):
    """The four arc colours must be told apart from each other, not only from the accents."""

    MIN_DE2000 = 20.0

    def test_every_pair_in_each_scheme_is_clearly_distinguishable(self):
        spec = gen_vscode_theme.load_design()
        for scheme, arc in (("light", spec["data"]), ("dark", spec["data-dark"])):
            roles = sorted(arc)
            for i, a in enumerate(roles):
                for b in roles[i + 1:]:
                    with self.subTest(scheme=scheme, pair=(a, b)):
                        self.assertGreaterEqual(
                            _delta_e2000(_lab(arc[a]), _lab(arc[b])), self.MIN_DE2000
                        )


if __name__ == "__main__":
    unittest.main()
