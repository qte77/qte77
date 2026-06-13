---
name: qte77
version: 0.1.0
description: >-
  qte77 visual identity — warm, low-fatigue, zero-blue, grounded in color
  science. The brand IS EyeRest (qte77's own theme): the default scheme is the
  flagship warm umber/parchment with an amber accent; Green, BluBlock, and Dusk
  ship as secondary variants. Dual light/dark. Reference tokens, never raw hex.
colors:                        # DEFAULT — EyeRest flagship (warm, amber accent)
  bg: "#ece8d8"
  surface: "#e2dec8"
  border: "#c8c4b0"
  text: "#2c2818"
  text-muted: "#686040"
  accent: "#8a7018"
  accent-on: "#ece8d8"
  dark-bg: "#1c1a14"
  dark-surface: "#242018"
  dark-border: "#383428"
  dark-text: "#d8d0b8"
  dark-text-muted: "#a89878"
  dark-accent: "#c8a858"
  dark-accent-on: "#1c1a14"
data:                          # zero-blue categorical arc (charts, KPI heatmap)
  positive: "#4a6818"          # dark: #8aa860
  caution:  "#787010"          # dark: #c8b868
  negative: "#983828"          # dark: #c08060
  alt:      "#587818"          # dark: #a8b870
typography:
  sans: { fontFamily: "Inter, system-ui, -apple-system, 'Segoe UI', sans-serif", fontSize: "16px", lineHeight: "1.6" }
  mono: { fontFamily: "'JetBrains Mono', ui-monospace, 'SF Mono', monospace", fontSize: "14px", lineHeight: "1.5" }
  h1: { fontFamily: "{typography.sans.fontFamily}", fontSize: "30px", fontWeight: 600, lineHeight: "1.25" }
  h2: { fontFamily: "{typography.sans.fontFamily}", fontSize: "24px", fontWeight: 600, lineHeight: "1.3" }
  h3: { fontFamily: "{typography.sans.fontFamily}", fontSize: "20px", fontWeight: 600, lineHeight: "1.4" }
rounded: { sm: "4px", md: "6px", lg: "12px" }
spacing: { unit: "8px", container: "768px" }
components:
  button-primary: { backgroundColor: "{colors.accent}", textColor: "{colors.accent-on}", rounded: "{rounded.md}", padding: "6px 16px", typography: "{typography.sans}" }
  card: { backgroundColor: "{colors.surface}", textColor: "{colors.text}", rounded: "{rounded.lg}", padding: "16px" }
  code: { backgroundColor: "{colors.surface}", textColor: "{colors.text}", typography: "{typography.mono}", rounded: "{rounded.sm}" }
variants:
  green:                       # forest / yellow-green
    name: EyeRest Green
    colors:
      bg: "#f0f6ee"
      surface: "#e8f0e6"
      border: "#c0d4bc"
      text: "#2a4a2a"
      text-muted: "#4a6a4a"
      accent: "#2a6a2a"
      accent-on: "#f0f6ee"
      dark-bg: "#0c1610"
      dark-surface: "#12201a"
      dark-border: "#2a3e2c"
      dark-text: "#8cb888"
      dark-text-muted: "#7aa878"
      dark-accent: "#3a6a3a"
      dark-accent-on: "#c4e8c0"
  blublock:                    # zero-blue (B<=30), for blue-filter lenses
    name: EyeRest BluBlock
    colors:
      bg: "#f5ecd8"
      surface: "#ede3cc"
      border: "#c8b898"
      text: "#3d2e18"
      text-muted: "#6b5838"
      accent: "#c06010"
      accent-on: "#f5ecd8"
      dark-bg: "#1a1208"
      dark-surface: "#231a0e"
      dark-border: "#3d2e1a"
      dark-text: "#e8d5b0"
      dark-text-muted: "#a08b6d"
      dark-accent: "#e89030"
      dark-accent-on: "#1a1208"
  dusk:                        # plum-gray / sage, earth-tone accents
    name: EyeRest Dusk
    colors:
      bg: "#eaece2"
      surface: "#e0e3d7"
      border: "#c8cac0"
      text: "#2c2622"
      text-muted: "#6a6058"
      accent: "#7a5820"
      accent-on: "#eaece2"
      dark-bg: "#1f1b22"
      dark-surface: "#2a2630"
      dark-border: "#3a343e"
      dark-text: "#d8ccbc"
      dark-text-muted: "#b0a498"
      dark-accent: "#c8a468"
      dark-accent-on: "#1f1b22"
---

# qte77 Design System

## Overview

qte77 looks the way qte77's own product works: **warm, quiet, and zero-blue.**
The brand is the EyeRest palette — color-science-grounded for low visual fatigue
(no blue in any accent, no pure black/white, 5:1–10:1 contrast). The default is
the flagship umber/parchment with an amber accent; three secondary variants
(Green, BluBlock, Dusk) cover preference and blue-filter-lens contexts. Two
schemes always ship (light = default for prose, dark = default for dashboards).
Never hardcode a hex — reference a token so scheme and variant flips re-resolve
every value.

## Colors

Surfaces are warm near-white or near-black; the single amber accent
(`#8a7018` light / `#c8a858` dark) does the pointing. `text-muted` is secondary
metadata only. Zero blue appears in any accent — that is the brand's defining
constraint, not a stylistic preference. The `data` arc (positive/caution/
negative/alt) is the categorical palette for charts and KPI heatmaps; it maps
directly onto good/neutral/bad cell coloring.

## Typography

**Inter** for UI and prose; **JetBrains Mono** for code, tickers, and numeric
tables. Body 16px / 1.6; headings 30 / 24 / 20px at weight 600. Numeric data is
tabular mono. No third typeface. Typography is shared across all variants.

## Layout

Single-column, content-first. Prose max-width 768px; dashboards may go full-bleed
but keep the 8px unit and 768px mobile breakpoint.

## Shapes

Soft, not round: 4px (inputs, chips), 6px (buttons, cells), 12px (cards, panels).
No pills except removable filter chips.

## Components

`button-primary` is accent-filled with `accent-on` text; `card` is a surface
panel at 12px; `code` is mono on the surface tone. Components reference tokens, so
they recolor wholesale when the active variant changes. New components compose
existing tokens — never raw values.

## Do's and Don'ts

- **Do** drive every color from a token so light/dark and variant flips are free.
- **Do** keep one amber accent per variant; let whitespace and weight carry hierarchy.
- **Do** use mono for numeric data and the `data` arc for chart/KPI categories.
- **Don't** ever introduce a blue accent — it breaks the brand's core promise.
- **Don't** mix two variants in one view; pick one, let it resolve wholesale.
- **Don't** add gradients, decorative shadows, a third font, or a hardcoded hex.

## Variants

The page selects variant + scheme (e.g. `data-variant="dusk" data-theme="dark"`);
CSS custom properties resolve from the matching block. All variants are zero-blue.

| Variant | bg light · dark | accent light · dark | Character |
|---|---|---|---|
| **Default** (EyeRest) | `#ece8d8` · `#1c1a14` | `#8a7018` · `#c8a858` | warm umber / parchment |
| Green | `#f0f6ee` · `#0c1610` | `#2a6a2a` · `#3a6a3a` | forest / yellow-green |
| BluBlock | `#f5ecd8` · `#1a1208` | `#c06010` · `#e89030` | zero-blue amber; blue-filter lenses |
| Dusk | `#eaece2` · `#1f1b22` | `#7a5820` · `#c8a468` | plum-gray / sage, earth tones |
