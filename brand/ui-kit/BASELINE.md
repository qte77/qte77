# GUI baseline — findings & actionable roadmap

Consolidated from a review of four qte77 GUIs (qte77.github.io, paperverse,
analyze-stock-kpi, agentic-job-offer-to-application-kit) and how each verified its UI with
`polyfetch-scrape`. **Start at [`README.md`](README.md) to *use* the kit; this doc is the
*why*** — the findings, decisions, and roadmap behind the shared no-build EyeRest theming.

## Two brandings — GitHub vs UI

qte77 runs **two distinct brandings** with different jobs. The `ui-kit/` carries **only UI
branding**. Never pull GitHub-blue into the app; never repaint the GitHub mark in EyeRest.

| | GitHub branding | UI branding |
|---|---|---|
| Purpose | identity inside GitHub's chrome (avatar, README, social cards) | the product GUIs (dashboards, Pages, in-app figures) |
| Source | `brand/images/*`, `brand/scripts/generate_social.py` | `brand/DESIGN.md` → `brand/ui-kit/` |
| Palette | GitHub Primer — blue accent `#388bfd` / `#1f6feb` on `#0d1117` / `#ffffff` | EyeRest — zero-blue, warm umber/parchment, amber primary |
| Cards | repo social previews **1280×640** | in-content OG/figure cards **1200×630** |

The brand mark is deliberately GitHub-blue so it blends into GitHub's UI — that is not an
EyeRest violation, because EyeRest's zero-blue rule governs the app, not the chrome asset.

## The unified UI baseline

The four GUIs already converged on one theme contract; the kit packages it. A qte77-branded
UI is conformant when it:

1. Resolves theme by precedence `?theme=` › `localStorage['qte77-theme']` ›
   `prefers-color-scheme`, restricted to `system | light | dark`.
2. Applies via `html[data-theme="light|dark"]`; for `system`, leaves the attribute unset so
   `prefers-color-scheme` governs.
3. Guards FOUC with an inline `<head>` IIFE that does (1)+(2) before first paint.
4. Cycles `system → light → dark` from one `#theme-toggle` button showing `◐ / ○ / ●`.
5. Is accessible: dynamic `aria-label`/`title`, a `role="status" aria-live="polite"`
   `.sr-only` announce region, a width-sizer (no reflow on cycle), `prefers-reduced-motion`,
   keyboard + Escape.
6. Emits a `themechange` event so charts/canvases recolour on flip.
7. Sources tokens from the generated `eyerest.css` — no per-repo vendored copy.

The reference implementation for the cycler + a11y is `analyze-stock-kpi`; the apply
mechanism + inline guard come from qte77.github.io / paperverse. The kit must stay
**no-build** (plain CSS + ES modules) because `agentic-job-offer-to-application-kit` ships
without a bundler.

## Decisions

| # | Decision | Rationale |
|---|---|---|
| D1 | Apply mechanism = `html[data-theme]` | cleaner `<head>` guard; 3 of 4 already use it |
| D2 | Toggle glyphs = `◐ ○ ●` (System/Light/Dark) | 3 of 4 already use it |
| D3 | a11y reference = `analyze-stock-kpi` | only one with dynamic `aria-label` + `aria-live` + width-sizer |
| D4 | `localStorage` key = `qte77-theme` | standardize the divergent keys |
| D5 | Tokens have one source of truth = `DESIGN.md` | CSS is generated; no second tokens source |
| D6 | Home = `brand/ui-kit/` (next to `DESIGN.md`) | tightest DRY; no new repo, no cross-repo token hop |
| D7 | Favicon **+ site logo** = `brand/images/logo-mark.paths.dejavu.svg` | one path-baked brand asset for both; sourced from brand/images |
| D8 | OG cards split by branding | 1200×630 figure cards (UI) vs 1280×640 repo social (GitHub) |
| D9 | Default CSS split into color / layout / fonts | matches `DESIGN.md` sections; pull only what you need |
| D10 | Fonts: WOFF2 for web, TTF kept for baking | smallest web payload; cairosvg/fonttools need desktop formats |
| D11 | `saas` variant added, de-blued (spruce green, not indigo) | brand is zero-blue by law; ships a cool/flat "SaaS/Linear" look without breaking the core rule (channel-order matches the approved `green`) |
| D12 | `chart-theme.js` reads live CSS custom properties on `themechange` | charts stay correct across any variant/scheme with no per-variant JS palette to drift from `eyerest.css`; consumes the zero-blue `--data-*` arc |
| D13 | `--shadow-card` now emitted into `eyerest.css` too (was Tailwind-only) | the no-build kit needs the elevation token for `.stat-tile`/`.callout` |

## Tokens & CSS

`DESIGN.md` is the single source of truth (D5); the CSS is **generated** from it and split
into color / layout / fonts (D9) — see [`README.md`](README.md) for the per-file contents.
Everything references tokens, never a raw hex; `--primary` is the deepened `#7a6010` /
`#c8a858` (WCAG AA on `--primary-on`).

## Verify with polyfetch — optional

The recommended (not required) way to catch branding/render defects **before users**:
[`../scripts/gui-check.py`](../scripts/gui-check.py) drives the shared `polyfetch-scrape`
stack to **check** the rendered UI (tokens, theme cycle, a11y, fonts, favicon, WebGL) and
**fetch** that URLs/assets return 200. It is **dual-scope** — *in-project* (your local/
staging URL) and *cross-repo* (sweep deployed URLs, audit live tokens vs `DESIGN.md` for
drift).

Commands + the opt-in CI recipe live in [`README.md`](README.md) ("Verify with polyfetch").

`gui-check.py` verifies **conformance** — the static contract (tokens, theme cycle, a11y,
fonts, favicon, WebGL context). **Behaviour** verification — does a control actually *do*
something over time (pause stops the idle motion, a toggle re-weights, a view snaps) — is the
complementary, currently ad-hoc half, driven the same way but comparing **frames** (see the
animation + Pillow gotchas below).

## Portable gotchas

| Gotcha | Fix |
|---|---|
| cairosvg tofu on `→ ≈ ²` in SVG `<text>` | use en-dash, `~`, `^2` / drawn arrows |
| `WebGPURenderer` ignores `gl_PointSize` | use the classic `WebGLRenderer` for `THREE.Points` |
| headless WebGL blank | launch with `--enable-unsafe-swiftshader --ignore-gpu-blocklist` |
| nested `sync_playwright()` throws | run polyfetch's `attempt()` outside your own context |
| `fetch()` won't JS-render a 200 page | drive Patchright directly to execute JS |
| idle animation (auto-rotate, transitions) confounds frame comparison | pause/disable it first, then compare; else every frame differs and the diff is meaningless |
| frame-diffing screenshots needs Pillow (absent from polyfetch's env) | add `--with pillow` to the `uv run`; compare via `ImageChops`/`ImageStat` mean-diff |

## Actionable items

- [ ] Add a `make ui-kit` target that **generates** `eyerest.css` / `layout.css` /
      `fonts.css` from `DESIGN.md` (keep them in sync; today they are faithful hand-renders).
- [ ] Update `scripts/install_fonts.py` to emit **WOFF2** (web) alongside TTF (baking).
- [x] Favicon (D7) — resolved: favicon + site logo = `brand/images/logo-mark.paths.dejavu.svg` (see README).
- [ ] Promote `scripts/gui-check.py` to `repo-baseline/tools/` for the cross-repo drift
      sweep (the org-wide baseline/drift home); keep the brand copy or symlink.
- [ ] Wire the existing GUIs onto the kit (start with `analyze-stock-kpi`, the reference).
- [x] Update issues #111 (shared ui-kit) and #112 (SVG/diagram pipeline) — done.
- [ ] Discoverability (SEO / GEO / ASO) — see [`DISCOVERABILITY.md`](DISCOVERABILITY.md) for the SEO head partial + GEO/ASO convention items.
- [ ] (optional) Adopt `ci-verify.example.yml` in projects that want the gate in CI.

## Discoverability (SEO / GEO / ASO)

How the sites get found and parsed by humans, answer engines, and autonomous agents — and
what the kit contributes — is a separate concern. See
[`DISCOVERABILITY.md`](DISCOVERABILITY.md).

## References

- `DESIGN.md` — EyeRest tokens (source of truth).
- `scripts/gui-check.py` — the polyfetch verify gate · `scripts/render_og.py` — OG/figure
  pipeline (1200×630).
- Issues #111 (shared ui-kit) · #112 (SVG/diagram pipeline consolidation).
