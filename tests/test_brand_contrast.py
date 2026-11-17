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


if __name__ == "__main__":
    unittest.main()
