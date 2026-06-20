# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6.0"]
# ///
"""Generate brand/ui-kit/eyerest.css from brand/DESIGN.md.

eyerest.css is the COLOR layer of the EyeRest ui-kit — pure design tokens, no
structural CSS. DESIGN.md (the google-labs-code front matter) is the single
source of truth (decision D5); this renders its ``colors`` / ``data`` /
``data-dark`` / ``variants`` into the cascade so the two never drift.

layout.css and fonts.css are NOT generated — they carry hand-authored structural
CSS (component classes, @font-face, utilities) beyond DESIGN.md's tokens.

Usage:
    uv run scripts/gen_ui_kit.py            # write ui-kit/eyerest.css
    uv run scripts/gen_ui_kit.py --check    # exit 1 if the file is stale
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

BRAND = Path(__file__).resolve().parent.parent
DESIGN_FILE = BRAND / "DESIGN.md"
OUT_FILE = BRAND / "ui-kit" / "eyerest.css"

# A CSS declaration: (custom-property name, value).
Decls = list[tuple[str, str]]

# CSS custom property <- DESIGN.md `colors` key, in cascade order.
BASE: Decls = [
    ("--bg", "bg"),
    ("--surface", "surface"),
    ("--border", "border"),
    ("--text", "text"),
    ("--text-muted", "text-muted"),
    ("--primary", "primary"),
    ("--primary-on", "primary-on"),
]
# CSS custom property <- DESIGN.md `data` / `data-dark` key.
DATA: Decls = [
    ("--data-positive", "positive"),
    ("--data-caution", "caution"),
    ("--data-negative", "negative"),
    ("--data-alt", "alt"),
]
VARIANTS: tuple[str, ...] = ("green", "blublock", "dusk")

HEADER = """\
/*
 * eyerest.css — qte77 UI-branding COLOR tokens (EyeRest design system).
 *
 * GENERATED from ../DESIGN.md by scripts/gen_ui_kit.py — DO NOT HAND-EDIT.
 * Source of truth: brand/DESIGN.md (`colors` / `data` / `data-dark` / `variants`).
 * Regenerate: `make -C brand ui_kit`. Token values are audited by gui-check.py.
 *
 * COLOR only. Pair with layout.css (spacing/shape) and fonts.css (type).
 * Cascade: System = no [data-theme] (prefers-color-scheme); Light/Dark =
 * html[data-theme]; Variant = html[data-variant], combine with data-theme.
 * Zero blue in any accent — the brand's core rule.
 */"""


def load_design() -> dict:
    """Parse the YAML front matter of DESIGN.md (between the first two `---`)."""
    front = DESIGN_FILE.read_text(encoding="utf-8").split("---", 2)[1]
    return yaml.safe_load(front)


def _rule(selector: str, decls: Decls, indent: str = "  ") -> str:
    body = "\n".join(f"{indent}{name}: {value};" for name, value in decls)
    return f"{selector} {{\n{body}\n}}"


def _media_dark(inner: str) -> str:
    nested = "\n".join("  " + line for line in inner.splitlines())
    return f"@media (prefers-color-scheme: dark) {{\n{nested}\n}}"


def _decls(colors: dict, keys: Decls, *, dark: bool) -> Decls:
    prefix = "dark-" if dark else ""
    return [(var, colors[f"{prefix}{key}"]) for var, key in keys]


def css_eyerest(spec: dict) -> str:
    """Render the full eyerest.css cascade from a parsed DESIGN.md spec."""
    colors = spec["colors"]
    data, data_dark = spec.get("data", {}), spec.get("data-dark", {})

    light = [("color-scheme", "light dark"), *_decls(colors, BASE, dark=False)]
    light += [(var, data[key]) for var, key in DATA]
    dark = _decls(colors, BASE, dark=True)
    dark += [(var, data_dark[key]) for var, key in DATA]

    parts = [
        HEADER,
        "/* Default (EyeRest flagship) — light */",
        _rule(":root", light),
        "/* Default — dark (system-dark, then the explicit attribute) */",
        _media_dark(_rule(':root:not([data-theme="light"])', dark)),
        _rule(':root[data-theme="dark"]', dark),
    ]

    for name in VARIANTS:
        variant = spec["variants"][name]
        vlight = _decls(variant["colors"], BASE, dark=False)
        vdark = _decls(variant["colors"], BASE, dark=True)
        sel = f':root[data-variant="{name}"]'
        parts += [
            f'/* Variant: {variant["name"]} */',
            _rule(sel, vlight),
            _media_dark(_rule(f'{sel}:not([data-theme="light"])', vdark)),
            _rule(f'{sel}[data-theme="dark"]', vdark),
        ]

    parts += [
        "/* Base color application */",
        "body { background: var(--bg); color: var(--text); }",
    ]
    return "\n\n".join(parts) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if eyerest.css is stale")
    args = ap.parse_args()

    rendered = css_eyerest(load_design())

    if args.check:
        current = OUT_FILE.read_text(encoding="utf-8") if OUT_FILE.exists() else ""
        if current != rendered:
            print(f"stale: {OUT_FILE} — run `make -C brand ui_kit`", file=sys.stderr)
            return 1
        print(f"ok: {OUT_FILE.name} is in sync with DESIGN.md")
        return 0

    OUT_FILE.write_text(rendered, encoding="utf-8")
    print(f"wrote {OUT_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
