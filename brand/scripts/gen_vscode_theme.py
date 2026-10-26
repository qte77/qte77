# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6.0"]
# ///
"""Generate the qte77 EyeRest VS Code color theme(s) from brand/DESIGN.md.

Workbench (UI chrome) colors only — editor/sidebar/statusbar/tabs/panels/inputs/
buttons/badges/git-decorations — generated straight from the same `colors` /
`data` / `variants` tokens as eyerest.css (single source of truth, decision D5),
so the editor matches the brand with zero extra palette to design or maintain.

Syntax highlighting (`tokenColors`) and the 16-color terminal ANSI ramp are a
tracked follow-up, not included here: both need new hues beyond the current
8-key + 4-data-key token set, designed and AA-checked the same deliberate way
the base palette and variants are (see DESIGN.md "Palette derivation"). Until
then this theme inherits VS Code's own default syntax colors, which may include
blue — a known, documented gap (see brand/vscode-theme/README.md).

One theme file per (variant, scheme) pair: the flagship ("eyerest") plus every
`variants` key in DESIGN.md, light and dark. package.json's `contributes.themes`
list is generated in lockstep so it can never drift out of sync with the files.

Usage:
    uv run scripts/gen_vscode_theme.py            # write every theme + package.json
    uv run scripts/gen_vscode_theme.py --check    # exit 1 if anything is stale
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

BRAND = Path(__file__).resolve().parent.parent
DESIGN_FILE = BRAND / "DESIGN.md"
OUT_DIR = BRAND / "vscode-theme"
THEMES_DIR = OUT_DIR / "themes"
PACKAGE_FILE = OUT_DIR / "package.json"

SCHEMES: tuple[str, ...] = ("light", "dark")


def load_design() -> dict:
    """Parse the YAML front matter of DESIGN.md (between the first two `---`)."""
    front = DESIGN_FILE.read_text(encoding="utf-8").split("---", 2)[1]
    return yaml.safe_load(front)


def _profiles(spec: dict) -> list[tuple[str, str, dict]]:
    """(key, display name, colors dict) for the flagship + every variant."""
    profiles = [("eyerest", "EyeRest", spec["colors"])]
    for key, variant in spec["variants"].items():
        profiles.append((key, variant["name"], variant["colors"]))
    return profiles


def _c(colors: dict, key: str, *, dark: bool) -> str:
    return colors[f'{"dark-" if dark else ""}{key}']


def workbench_colors(colors: dict, data: dict, *, dark: bool) -> dict[str, str]:
    """Map DESIGN.md tokens onto VS Code workbench (UI chrome) color keys."""
    bg = _c(colors, "bg", dark=dark)
    surface = _c(colors, "surface", dark=dark)
    border = _c(colors, "border", dark=dark)
    text = _c(colors, "text", dark=dark)
    text_muted = _c(colors, "text-muted", dark=dark)
    primary = _c(colors, "primary", dark=dark)
    primary_on = _c(colors, "primary-on", dark=dark)
    link = _c(colors, "link", dark=dark)
    positive, caution, negative, alt = data["positive"], data["caution"], data["negative"], data["alt"]

    return {
        "editor.background": bg,
        "editor.foreground": text,
        "editorLineNumber.foreground": text_muted,
        "editorLineNumber.activeForeground": text,
        "editorCursor.foreground": primary,
        "editor.selectionBackground": border,
        "editor.lineHighlightBackground": surface,
        "editorIndentGuide.background1": border,
        "editorWhitespace.foreground": border,
        "editorError.foreground": negative,
        "editorWarning.foreground": caution,
        "editorInfo.foreground": primary,
        "activityBar.background": surface,
        "activityBar.foreground": text,
        "activityBar.border": border,
        "activityBarBadge.background": primary,
        "activityBarBadge.foreground": primary_on,
        "sideBar.background": surface,
        "sideBar.foreground": text,
        "sideBar.border": border,
        "sideBarTitle.foreground": text,
        "sideBarSectionHeader.background": surface,
        "sideBarSectionHeader.foreground": text_muted,
        "statusBar.background": bg,
        "statusBar.foreground": text_muted,
        "statusBar.border": border,
        "titleBar.activeBackground": bg,
        "titleBar.activeForeground": text,
        "titleBar.inactiveBackground": bg,
        "titleBar.inactiveForeground": text_muted,
        "titleBar.border": border,
        "tab.activeBackground": bg,
        "tab.activeForeground": text,
        "tab.inactiveBackground": surface,
        "tab.inactiveForeground": text_muted,
        "tab.border": border,
        "tab.activeBorderTop": primary,
        "editorGroupHeader.tabsBackground": surface,
        "editorGroupHeader.tabsBorder": border,
        "editorGroup.border": border,
        "panel.background": surface,
        "panel.border": border,
        "panelTitle.activeForeground": text,
        "panelTitle.activeBorder": primary,
        "panelTitle.inactiveForeground": text_muted,
        "input.background": bg,
        "input.foreground": text,
        "input.border": border,
        "input.placeholderForeground": text_muted,
        "inputOption.activeBorder": primary,
        "dropdown.background": surface,
        "dropdown.foreground": text,
        "dropdown.border": border,
        "focusBorder": primary,
        "widget.border": border,
        "editorWidget.background": surface,
        "editorWidget.foreground": text,
        "editorWidget.border": border,
        "button.background": primary,
        "button.foreground": primary_on,
        "button.secondaryBackground": surface,
        "button.secondaryForeground": text,
        "badge.background": primary,
        "badge.foreground": primary_on,
        "textLink.foreground": link,
        "textLink.activeForeground": link,
        "textPreformat.foreground": primary,
        "list.activeSelectionBackground": border,
        "list.activeSelectionForeground": text,
        "list.hoverBackground": surface,
        "list.inactiveSelectionBackground": surface,
        "list.highlightForeground": primary,
        "scrollbarSlider.background": border,
        "scrollbarSlider.hoverBackground": border,
        "scrollbar.shadow": border,
        "terminal.background": bg,
        "terminal.foreground": text,
        "progressBar.background": primary,
        "notificationCenterHeader.background": surface,
        "notifications.background": surface,
        "notifications.foreground": text,
        "notifications.border": border,
        "gitDecoration.addedResourceForeground": positive,
        "gitDecoration.modifiedResourceForeground": caution,
        "gitDecoration.deletedResourceForeground": negative,
        "gitDecoration.untrackedResourceForeground": alt,
        "gitDecoration.ignoredResourceForeground": text_muted,
        "gitDecoration.conflictingResourceForeground": negative,
    }


def theme_json(display_name: str, colors: dict, data: dict, *, dark: bool) -> str:
    doc = {
        "name": display_name,
        "type": "dark" if dark else "light",
        "colors": workbench_colors(colors, data, dark=dark),
    }
    return json.dumps(doc, indent=2) + "\n"


PACKAGE_META = {
    "name": "qte77-eyerest-theme",
    "displayName": "EyeRest (qte77)",
    "description": (
        "qte77's zero-blue, low-fatigue EyeRest color theme for VS Code — the "
        "flagship palette plus every brand variant, light and dark. UI chrome "
        "only for now; syntax highlighting is a tracked follow-up. Generated "
        "from brand/DESIGN.md."
    ),
    "version": "0.1.0",
    "publisher": "qte77",
    "license": "Apache-2.0",
    "engines": {"vscode": "^1.90.0"},
    "categories": ["Themes"],
    "repository": {
        "type": "git",
        "url": "https://github.com/qte77/qte77",
        "directory": "brand/vscode-theme",
    },
}


def package_json(spec: dict) -> str:
    themes = []
    for key, name, _ in _profiles(spec):
        for scheme in SCHEMES:
            dark = scheme == "dark"
            themes.append(
                {
                    "label": f"{name} {'Dark' if dark else 'Light'}",
                    "uiTheme": "vs-dark" if dark else "vs",
                    "path": f"./themes/{key}-{scheme}-color-theme.json",
                }
            )
    doc = dict(PACKAGE_META)
    doc["contributes"] = {"themes": themes}
    return json.dumps(doc, indent=2) + "\n"


def _emit(out: Path, rendered: str, *, check: bool) -> int:
    if check:
        current = out.read_text(encoding="utf-8") if out.exists() else ""
        if current != rendered:
            print(f"stale: {out} — run `make -C brand vscode_theme`", file=sys.stderr)
            return 1
        return 0
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(rendered, encoding="utf-8")
    print(f"wrote {out}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="exit 1 if any generated file is stale")
    args = ap.parse_args()

    spec = load_design()
    data_by_scheme = {"light": spec.get("data", {}), "dark": spec.get("data-dark", {})}

    outputs: list[tuple[Path, str]] = [(PACKAGE_FILE, package_json(spec))]
    for key, name, colors in _profiles(spec):
        for scheme in SCHEMES:
            dark = scheme == "dark"
            display = f"{name} {'Dark' if dark else 'Light'}"
            out = THEMES_DIR / f"{key}-{scheme}-color-theme.json"
            outputs.append((out, theme_json(display, colors, data_by_scheme[scheme], dark=dark)))

    results = [_emit(out, rendered, check=args.check) for out, rendered in outputs]
    if args.check and max(results) == 0:
        print(f"ok: {len(outputs)} vscode-theme files are in sync with DESIGN.md")
    return max(results)


if __name__ == "__main__":
    raise SystemExit(main())
