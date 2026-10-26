# `brand/vscode-theme/` — EyeRest for VS Code

A VS Code color theme extension carrying the EyeRest brand into the editor: the flagship
palette plus all six [`../DESIGN.md`](../DESIGN.md) variants (Green, BluBlock, Dusk, SaaS,
Terracotta, Plum), light and dark — 14 themes from one `contributes.themes` list.

> **Provenance.** Every file here (`package.json`'s `contributes.themes` list and every
> `themes/*-color-theme.json`) is **generated from `../DESIGN.md`**
> (`make -C brand vscode_theme`) — do not hand-edit. Same source of truth as
> `../ui-kit/eyerest.css`, same reason: one palette, no second place for it to drift.

## Scope — UI chrome only (for now)

This themes VS Code's **workbench** colors — editor background/foreground, sidebar, activity
bar, status bar, tabs, panels, inputs, buttons, badges, notifications, and git decorations —
straight from the same `colors` / `data` / `variants` tokens as the web ui-kit.

**Not yet included, and why:** `tokenColors` (syntax highlighting — keywords, strings,
functions, comments, etc.) and the 16-color terminal ANSI ramp both need hues beyond the
current 8-key + 4-data-key token set. Designing those requires the same deliberate,
AA-checked process as the base palette and variants (see `DESIGN.md` "Palette derivation") —
picking them as an afterthought here would be exactly the "eyeballed hex" shortcut that process
exists to avoid. Until that work lands, these themes inherit VS Code's own default TextMate
grammar theme and ANSI colors, which may include blue — a known gap, not a silent one.

## Gallery

[`gallery.html`](gallery.html) shows every variant's swatches and a live editor-chrome mockup,
light and dark, without installing anything — open it locally or view it rendered via
[htmlpreview.github.io](https://htmlpreview.github.io/?https://github.com/qte77/qte77/blob/main/brand/vscode-theme/gallery.html).
Hand-authored (not generated), so re-check it against `DESIGN.md` when a variant changes.

## Install locally (not yet published)

No marketplace listing yet. To try it in VS Code:

1. Symlink (or copy) this folder into your extensions directory, e.g.
   `~/.vscode/extensions/qte77.eyerest-theme`.
2. Reload VS Code, then `Preferences: Color Theme` and pick any `EyeRest …` entry.

Or, for a scratch look without touching your real extensions folder: open this repo in VS
Code, press `F5` to launch an Extension Development Host, and pick a theme there.

## Regenerate

```bash
make -C brand vscode_theme            # write package.json + every themes/*.json
uv run brand/scripts/gen_vscode_theme.py --check   # exit 1 if stale
```

## Contents

| Path | From `DESIGN.md` | What |
|---|---|---|
| `package.json` | `colors` · `variants` | extension manifest + the generated `contributes.themes` list (14 entries) |
| `themes/<variant>-<scheme>-color-theme.json` | `colors` · `data` · `data-dark` · `variants` | one workbench color theme per (variant, scheme) pair |
| `gallery.html` | — | hand-authored showcase page — swatches + editor-chrome mockups, no install needed |

## See also

- [`../DESIGN.md`](../DESIGN.md) — token source of truth, including "Palette derivation" (the
  harmony-rule method Terracotta and Plum were derived with).
- [`../ui-kit/`](../ui-kit/) — the web/Tailwind counterpart, same source, same zero-blue rule.
- [issue #111](https://github.com/qte77/qte77/issues/111) — ui-kit roadmap (syntax
  highlighting / terminal ANSI for this theme would track here too, once scoped).
