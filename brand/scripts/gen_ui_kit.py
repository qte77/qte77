# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6.0"]
# ///
"""Generate the EyeRest ui-kit CSS from brand/DESIGN.md.

Two generated outputs, both from DESIGN.md (the single source of truth, decision
D5) so they never drift:

- ``ui-kit/eyerest.css`` — the no-build COLOR layer: plain ``--bg`` / ``--surface``
  custom properties for the Jekyll/static sites (default + 3 variants, light/dark).
- ``ui-kit/tailwind/tokens.css`` — the same tokens shaped as a Tailwind v4
  ``@theme`` block (``--color-*`` / ``--font-*`` / ``--radius-*``), published as the
  ``@qte77/ui-theme`` npm package and consumed by the Vite/React apps
  (agenthud-agui-a2ui, ldnmxx-hack) that used to hand-copy this block.

layout.css and fonts.css are NOT generated — they carry hand-authored structural
CSS (component classes, @font-face, utilities) beyond DESIGN.md's tokens.

Usage:
    uv run scripts/gen_ui_kit.py            # write both generated files
    uv run scripts/gen_ui_kit.py --check    # exit 1 if either file is stale
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

BRAND = Path(__file__).resolve().parent.parent
DESIGN_FILE = BRAND / "DESIGN.md"
OUT_FILE = BRAND / "ui-kit" / "eyerest.css"
OUT_TAILWIND = BRAND / "ui-kit" / "tailwind" / "tokens.css"

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


TW_HEADER = """\
/*
 * tokens.css — qte77 UI theme as Tailwind v4 design tokens (@qte77/ui-theme).
 *
 * GENERATED from DESIGN.md by scripts/gen_ui_kit.py — DO NOT HAND-EDIT.
 * Source of truth: brand/DESIGN.md (`colors` / `data` / `data-dark` /
 * `typography` / `rounded` / `elevation`). Regenerate: `make -C brand ui_kit`.
 *
 * Consume from a Tailwind v4 app:
 *     @import "tailwindcss";
 *     @import "@qte77/ui-theme/tailwind/tokens.css";
 * The @theme block registers utilities (bg-bg, text-primary, border-border,
 * font-sans, rounded-lg, …); the :root overrides swap the scheme at runtime via
 * html[data-theme] or prefers-color-scheme. Fonts are the consumer's concern
 * (self-host or @fontsource) — this file only names the family stacks.
 * Includes --shadow-card: functional elevation, warm/zero-blue (DESIGN.md
 * "Motion & effects"); the dark value swaps via the runtime scheme blocks.
 * Zero blue in any accent — the brand's core rule.
 */"""


def _tw_color_decls(colors: dict, data: dict, *, dark: bool) -> Decls:
    """Tailwind --color-* declarations for a scheme (base palette + data arc)."""
    base = [(f"--color-{key}", colors[f'{"dark-" if dark else ""}{key}']) for _, key in BASE]
    arc = [(f"--color-data-{key}", data[key]) for _, key in DATA]
    return base + arc


def css_tailwind(spec: dict) -> str:
    """Render tokens.css: the DESIGN.md tokens as a Tailwind v4 @theme cascade."""
    colors = spec["colors"]
    typ, rounded, elevation = spec["typography"], spec["rounded"], spec.get("elevation", {})

    theme = _tw_color_decls(colors, spec.get("data", {}), dark=False)
    theme += [
        ("--font-sans", typ["sans"]["fontFamily"]),
        ("--font-mono", typ["mono"]["fontFamily"]),
        ("--radius-sm", rounded["sm"]),
        ("--radius-md", rounded["md"]),
        ("--radius-lg", rounded["lg"]),
    ]
    dark = _tw_color_decls(colors, spec.get("data-dark", {}), dark=True)
    # Functional elevation (DESIGN.md `elevation`): --shadow-card, light in @theme +
    # its dark value in the scheme-swap blocks so var(--shadow-card) re-resolves.
    if elevation:
        theme.append(("--shadow-card", elevation["shadow-card"]))
        dark.append(("--shadow-card", elevation["dark-shadow-card"]))

    parts = [
        TW_HEADER,
        _rule("@theme", theme),
        "/* Runtime scheme swap: system-dark (no explicit light), then the attribute. */",
        _media_dark(_rule(':root:not([data-theme="light"])', dark)),
        _rule(':root[data-theme="dark"]', dark),
        _rule(":root", [("color-scheme", "light dark")]),
    ]
    return "\n\n".join(parts) + "\n"


def _emit(out: Path, rendered: str, *, check: bool) -> int:
    """Write `rendered` to `out`, or (check mode) report whether it is stale."""
    if check:
        current = out.read_text(encoding="utf-8") if out.exists() else ""
        if current != rendered:
            print(f"stale: {out} — run `make -C brand ui_kit`", file=sys.stderr)
            return 1
        print(f"ok: {out.name} is in sync with DESIGN.md")
        return 0
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(rendered, encoding="utf-8")
    print(f"wrote {out}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if either generated file is stale")
    args = ap.parse_args()

    spec = load_design()
    outputs = [(OUT_FILE, css_eyerest(spec)), (OUT_TAILWIND, css_tailwind(spec))]
    # Emit both before returning so --check reports every stale file, not just the first.
    return max(_emit(out, rendered, check=args.check) for out, rendered in outputs)


if __name__ == "__main__":
    raise SystemExit(main())
