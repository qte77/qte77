---
name: qte77
version: 0.1.0
description: >-
  qte77 visual identity — warm, low-fatigue, zero-blue, grounded in color
  science. The brand IS EyeRest (qte77's own theme): the default scheme is the
  flagship warm umber/parchment with an amber accent; Green, BluBlock, Dusk, and
  SaaS ship as secondary variants. Dual light/dark. Reference tokens, never raw hex.
colors:                        # DEFAULT — EyeRest flagship (warm, amber primary)
  bg: "#ece8d8"
  surface: "#e2dec8"
  border: "#c8c4b0"
  text: "#2c2818"
  text-muted: "#686040"
  primary: "#7a6010"           # deepened from EyeRest #8a7018 to clear WCAG AA on primary-on text
  primary-on: "#ece8d8"
  link: "#755c0f"               # primary set AS TEXT — primary is 4.4:1 as small text here; link clears 4.7-5.2:1
  dark-bg: "#1c1a14"
  dark-surface: "#242018"
  dark-border: "#383428"
  dark-text: "#d8d0b8"
  dark-text-muted: "#a89878"
  dark-primary: "#c8a858"
  dark-primary-on: "#1c1a14"
  dark-link: "#c8a858"          # aliases dark-primary — already clears AA as text (7.1-7.6:1)
data:                          # zero-blue categorical arc (charts, KPI heatmap)
  positive: "#4a6818"          # dark: #8aa860
  caution:  "#787010"          # dark: #c8b868
  negative: "#983828"          # dark: #c08060
  alt:      "#587818"          # dark: #a8b870
data-dark:                     # dark scheme of the data arc (machine-readable; read by gen_ui_kit.py)
  positive: "#8aa860"
  caution:  "#c8b868"
  negative: "#c08060"
  alt:      "#a8b870"
typography:
  sans: { fontFamily: "Inter, system-ui, -apple-system, 'Segoe UI', sans-serif", fontSize: "16px", lineHeight: "1.6" }
  mono: { fontFamily: "'JetBrains Mono', ui-monospace, 'SF Mono', monospace", fontSize: "14px", lineHeight: "1.5" }
  eyebrow: { fontFamily: "{typography.sans.fontFamily}", fontSize: "12px", fontWeight: 600, lineHeight: "1.4", letterSpacing: "0.06em" }
  caption: { fontFamily: "{typography.sans.fontFamily}", fontSize: "13px", fontWeight: 400, lineHeight: "1.5" }
  body-small: { fontFamily: "{typography.sans.fontFamily}", fontSize: "14px", fontWeight: 400, lineHeight: "1.5" }
  h3: { fontFamily: "{typography.sans.fontFamily}", fontSize: "20px", fontWeight: 600, lineHeight: "1.4" }
  h2: { fontFamily: "{typography.sans.fontFamily}", fontSize: "24px", fontWeight: 600, lineHeight: "1.3" }
  h1: { fontFamily: "{typography.sans.fontFamily}", fontSize: "30px", fontWeight: 600, lineHeight: "1.25" }
  display: { fontFamily: "{typography.sans.fontFamily}", fontSize: "40px", fontWeight: 600, lineHeight: "1.15", letterSpacing: "-0.01em" }
  mono-label: { fontFamily: "{typography.mono.fontFamily}", fontSize: "13px", fontWeight: 500, lineHeight: "1.4", letterSpacing: "0.02em" }
rounded: { sm: "4px", md: "6px", lg: "12px", full: "9999px" }  # full: removable filter chips ONLY
spacing:
  unit: "8px"                  # base rhythm — every gap is a multiple of this
  container: "768px"           # prose max-width / mobile breakpoint (container-prose)
  scale-px: [4, 8, 12, 16, 24, 32, 48, 64, 96]   # space-1|2|3|4|6|8|12|16|24 — 4px half-steps below 16, 8px multiples of unit above
  rule-height: "3px"           # Index Rule bar thickness — fixed, never scales
  rule-width-sm: "24px"        # Index Rule, inline form
  rule-width-lg: "48px"        # Index Rule, card/section top-edge form
elevation:                     # functional depth — warm, zero-blue, low-opacity (card/skeleton/chip)
  shadow-card: "0 1px 2px rgba(28, 26, 20, 0.06), 0 4px 12px rgba(28, 26, 20, 0.08)"
  dark-shadow-card: "0 1px 2px rgba(0, 0, 0, 0.5), 0 8px 20px rgba(0, 0, 0, 0.55)"
components:
  button-primary: { backgroundColor: "{colors.primary}", textColor: "{colors.primary-on}", rounded: "{rounded.md}", padding: "6px 16px", typography: "{typography.sans}" }
  card: { backgroundColor: "{colors.surface}", textColor: "{colors.text}", rounded: "{rounded.lg}", padding: "16px" }
  code: { backgroundColor: "{colors.surface}", textColor: "{colors.text}", typography: "{typography.mono}", rounded: "{rounded.sm}" }
  page: { backgroundColor: "{colors.bg}", textColor: "{colors.text}" }
  input: { backgroundColor: "{colors.surface}", textColor: "{colors.text}", rounded: "{rounded.sm}", padding: "6px 12px" }
  caption: { textColor: "{colors.text-muted}", typography: "{typography.sans}" }
  divider: { backgroundColor: "{colors.border}", height: "1px" }
  stat-tile: { backgroundColor: "{colors.surface}", textColor: "{colors.text}", rounded: "{rounded.lg}", padding: "16px", elevation: "{elevation.shadow-card}" }
  callout: { backgroundColor: "{colors.surface}", textColor: "{colors.text}", borderColor: "{colors.border}", rounded: "{rounded.md}", padding: "12px 16px" }
variants:
  green:                       # forest / yellow-green
    name: EyeRest Green
    colors:
      bg: "#f0f6ee"
      surface: "#e8f0e6"
      border: "#c0d4bc"
      text: "#2a4a2a"
      text-muted: "#4a6a4a"
      primary: "#2a6a2a"
      primary-on: "#f0f6ee"
      link: "#2a6a2a"            # aliases primary — already clears AA as text in light (5.7-6.0:1)
      dark-bg: "#0c1610"
      dark-surface: "#12201a"
      dark-border: "#2a3e2c"
      dark-text: "#8cb888"
      dark-text-muted: "#7aa878"
      dark-primary: "#3a6a3a"
      dark-primary-on: "#c4e8c0"
      dark-link: "#539853"       # primary alone is only 2.6-2.9:1 as text in dark; retuned to 4.6-5.3:1
  blublock:                    # zero-blue (B<=30), for blue-filter lenses
    name: EyeRest BluBlock
    colors:
      bg: "#f5ecd8"
      surface: "#ede3cc"
      border: "#c8b898"
      text: "#3d2e18"
      text-muted: "#6b5838"
      primary: "#c06010"
      primary-on: "#f5ecd8"
      link: "#964b0c"            # primary alone is only 3.3-3.6:1 as text in light; deepened to 4.7-5.4:1
      dark-bg: "#1a1208"
      dark-surface: "#231a0e"
      dark-border: "#3d2e1a"
      dark-text: "#e8d5b0"
      dark-text-muted: "#a08b6d"
      dark-primary: "#e89030"
      dark-primary-on: "#1a1208"
      dark-link: "#e89030"       # aliases dark-primary — already clears AA as text (6.9-7.5:1)
  dusk:                        # plum-gray / sage, earth-tone accents
    name: EyeRest Dusk
    colors:
      bg: "#eaece2"
      surface: "#e0e3d7"
      border: "#c8cac0"
      text: "#2c2622"
      text-muted: "#6a6058"
      primary: "#7a5820"
      primary-on: "#eaece2"
      link: "#7a5820"            # aliases primary — already clears AA as text (5.0-5.4:1)
      dark-bg: "#1f1b22"
      dark-surface: "#2a2630"
      dark-border: "#3a343e"
      dark-text: "#d8ccbc"
      dark-text-muted: "#b0a498"
      dark-primary: "#c8a468"
      dark-primary-on: "#1f1b22"
      dark-link: "#c8a468"       # aliases dark-primary — already clears AA as text (6.3-7.2:1)
  saas:                        # de-blued "SaaS/Linear" — cool spruce green (zero-blue), flat/modern
    name: EyeRest SaaS
    colors:
      bg: "#f4f6f4"
      surface: "#e9ece9"
      border: "#ccd2cc"
      text: "#1a201c"
      text-muted: "#5a635c"
      primary: "#1f6e4c"
      primary-on: "#eef1ec"
      link: "#1f6e4c"            # aliases primary — already clears AA as text (5.2-5.7:1)
      dark-bg: "#0f1512"
      dark-surface: "#161d19"
      dark-border: "#28322c"
      dark-text: "#e6ece8"
      dark-text-muted: "#9aa8a0"
      dark-primary: "#4fae82"
      dark-primary-on: "#14201a"
      dark-link: "#4fae82"       # aliases dark-primary — already clears AA as text (6.3-6.8:1)
---

# qte77 Design System

## Overview

qte77 looks the way qte77's own product works: **warm, quiet, and zero-blue.**
The brand is the EyeRest palette — color-science-grounded for low visual fatigue
(no blue in any accent, no pure black/white, 5:1–10:1 contrast). The default is
the flagship umber/parchment with an amber accent; four secondary variants
(Green, BluBlock, Dusk, SaaS) cover preference, blue-filter-lens, and de-blued
dashboard contexts. Two schemes always ship (light = default for prose, dark =
default for dashboards). Never hardcode a hex — reference a token so scheme and
variant flips re-resolve every value.

## Colors

Surfaces are warm near-white or near-black; the single amber `primary`
(`#7a6010` light / `#c8a858` dark) does the pointing. `text-muted` is secondary
metadata only. Zero blue appears in any accent — that is the brand's defining
constraint, not a stylistic preference. The `data` arc (positive/caution/
negative/alt) is the categorical palette for charts and KPI heatmaps; it maps
directly onto good/neutral/bad cell coloring.

`primary` has two jobs that need two different values. As a **fill** (buttons,
icons, large/bold elements, the Index Rule) the swatch is correct everywhere.
As **text** (an inline link, a small primary-colored label) it falls short of
4.5:1 in three of five variant/theme combinations — `link` is a hue-true,
text-safe reading of `primary`, aliased straight to it wherever that already
clears AA and re-tuned only where it doesn't (see Accessibility). **Use
`link`, never `primary`, for any primary-colored text.**

## Typography

**Inter** for UI and prose; **JetBrains Mono** for code, tickers, and numeric
tables. The scale runs `eyebrow` (12px, uppercase labels) → `caption` (13px) →
`body-small` (14px) → `body`/`sans` (16px, the floor of running text) → `h3`
(20px) → `h2` (24px) → `h1` (30px) → `display` (40px, cover/hero moments
only — spend it once per surface). `mono-label` (13px, tabular) carries KPI
values and sensor readouts. Numeric data is always tabular mono, never
proportional sans. No third typeface. Typography is shared across all variants.

## Layout

Single-column, content-first. Prose max-width 768px; dashboards may go full-bleed
but keep the 8px unit and 768px mobile breakpoint.

## Shapes

Soft, not round: 4px (inputs, chips), 6px (buttons, cells), 12px (cards, panels).
No pills except removable filter chips.

## The Index Rule

qte77's one recurring geometric signature: a `primary`-filled bar, `rule-height`
(3px) thick, always capsule-ended (corner radius = half its own height — never a
separate radius token). Two fixed lengths only — `rule-width-sm` (24px, inline
beside a heading or `eyebrow` label) and `rule-width-lg` (48px, flush against a
card's or section's top edge). No third length, no responsive scaling: the same
rule at the same size everywhere is what makes it read as qte77's mark rather
than a random underline.

Use it to open a section, underline an `eyebrow` label, or as a card's top edge
in place of a primary-colored left border (a pattern this brand avoids as an
AI-generated-UI cliché — `border`-tone left rules, like `.callout`'s, are
unaffected). Never as a progress indicator, a divider between unrelated
content, or more than once in a composition.

## Components

`button-primary` is primary-filled with `primary-on` text; `card` is a surface
panel at 12px; `code` is mono on the surface tone. Components reference tokens, so
they recolor wholesale when the active variant changes. New components compose
existing tokens — never raw values.

## Motion & effects

Depth is **functional, not decorative**. The brand allows a small, warm, zero-blue
elevation shadow and quiet motion where they help the reader parse the interface;
anything ornamental stays out. Everything here collapses under
`prefers-reduced-motion`.

**Allowed** — subtle and purposeful:

- **Elevation shadow** (`--shadow-card`): lifts a card/panel so it reads as a
  distinct surface. Use on raised surfaces (cards, the loading skeleton, the
  "working" chip); pair it with the `border` + `surface` tone step, don't replace
  it. *Example: an A2UI card uses `box-shadow: var(--shadow-card)`.*
- **Loading shimmer**: a token-driven gradient sweeping a skeleton placeholder
  while content streams — signals "in progress". *Example: a `--color-border` →
  `--color-surface` `linear-gradient` animating `background-position`.*
- **Functional motion**: a brief entrance on a newly-mounted block, a low-contrast
  "working" pulse. *Example: `qte-enter` 220ms on a new card only.*

**Discouraged** — decorative, high-fatigue: heavy or high-contrast shadows, glow,
gloss, and non-functional gradients used as surface fills. Depth should be barely
noticed, never the point.

**Still banned** (see Shapes / Colors / Typography): pill radii except a removable
filter chip; any blue accent; pure black/white; a hardcoded hex; a third typeface.

`--shadow-card` is a real brand token — its light/dark values live in the
`elevation` front matter and ship in `@qte77/ui-theme`
(`ui-kit/tailwind/tokens.css`), so every surface draws the same depth and a scheme
flip re-resolves it.

## Accessibility

Every `text` / `text-muted` / `primary-on` pairing clears WCAG AA (4.5:1 body
text, 3:1 large/bold text and UI components) against its stated ground, in
every theme and variant, with three flagged exceptions — real, shipping
values, not silently adjusted:

- **`border`** is ~1.2–1.7:1 against `bg`/`surface` across every variant — a
  quiet one-tone-step divider by design, not a 3:1 boundary. Pair it with
  `shadow-card` or a surface step where a control's edge must be perceivable
  at 3:1.
- **`primary-on` on a BluBlock `primary` fill** is 3.6:1 in light theme —
  clears the 3:1 large/bold floor, not 4.5:1. Keep BluBlock `button-primary`
  labels at `body` weight 600+ or `h3`+ size.
- **`data-caution` / `data-alt`, light theme only** are 3.8:1 as small text on
  `surface` (4.2:1 on `bg`) — `surface` is the binding case: fine for a chart
  fill, dot, or icon (3:1 floor), but a KPI delta or axis label needs bold or
  16px+/weight 600 to clear AA there. Both are 7.5–8.7:1 in dark theme,
  unrestricted.

`data-negative` is never the only signal — pair it with a label or icon.

## Do's and Don'ts

- **Do** drive every color from a token so light/dark and variant flips are free.
- **Do** keep one amber primary per variant; let whitespace and weight carry hierarchy.
- **Do** use mono for numeric data and the `data` arc for chart/KPI categories.
- **Do** use `--shadow-card` for subtle elevation; keep motion functional, subtle,
  and `prefers-reduced-motion`-guarded (see Motion & effects).
- **Do** use `link` (never `primary`) for any primary-colored text — inline
  links, small primary-colored labels. `primary` itself is for fills, icons,
  and large/bold elements only (see Colors, Accessibility).
- **Don't** ever introduce a blue accent — it breaks the brand's core promise.
- **Don't** mix two variants in one view; pick one, let it resolve wholesale.
- **Don't** add decorative gloss, glow, non-functional gradients, heavy shadows,
  pills (except a removable filter chip), a third font, or a hardcoded hex.

## Variants

The page selects variant + scheme (e.g. `data-variant="dusk" data-theme="dark"`);
CSS custom properties resolve from the matching block. All variants are zero-blue.

| Variant | bg light · dark | primary light · dark | Character |
|---|---|---|---|
| **Default** (EyeRest) | `#ece8d8` · `#1c1a14` | `#7a6010` · `#c8a858` | warm umber / parchment |
| Green | `#f0f6ee` · `#0c1610` | `#2a6a2a` · `#3a6a3a` | forest / yellow-green |
| BluBlock | `#f5ecd8` · `#1a1208` | `#c06010` · `#e89030` | zero-blue amber; blue-filter lenses |
| Dusk | `#eaece2` · `#1f1b22` | `#7a5820` · `#c8a468` | plum-gray / sage, earth tones |
| SaaS | `#f4f6f4` · `#0f1512` | `#1f6e4c` · `#4fae82` | de-blued flat/modern spruce |
