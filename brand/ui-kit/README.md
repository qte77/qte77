# `brand/ui-kit/` — qte77 default UI theme (EyeRest)

The no-build UI-branding kit, generated from [`../DESIGN.md`](../DESIGN.md) and living next
to it so the CSS sits beside its source of truth. This is the **UI branding** (the product
GUI); `../images/` is the **GitHub branding** (avatar, logo-mark). The two are distinct
systems — never pull GitHub-blue into the app. See [`BASELINE.md`](BASELINE.md) for the full
rationale and decisions.

> **Provenance.** `eyerest.css`, `layout.css`, and `fonts.css` are **generated from
> `../DESIGN.md`** — do not hand-edit. The token source of truth is `DESIGN.md`.

## npm package — `@qte77/ui-theme` (Tailwind v4 apps)

The Vite/React apps consume the theme as an npm package instead of hand-copying
the `@theme` block. `tailwind/tokens.css` is **generated from `../DESIGN.md`**
(same source, `make -C brand ui_kit`) and published to **GitHub Packages** by
`.github/workflows/publish-ui-theme.yml` on a version bump of
[`package.json`](package.json).

```css
/* src/index.css */
@import "tailwindcss";
@import "@qte77/ui-theme/tailwind/tokens.css";
```

This registers the utilities the apps use — `bg-bg`, `bg-surface`, `text-text`,
`text-primary`, `border-border`, `font-sans`, `font-mono`, `rounded-lg` — plus a
runtime `html[data-theme]` / `prefers-color-scheme` scheme swap. Fonts are the
consumer's concern (`@fontsource/*` or self-host); the package only names the
family stacks. It ships **no shadow token** — the surface is flat by mandate
(see `../DESIGN.md` "Motion & effects").

GitHub Packages requires an auth token even to *install* a public package. Add an
`.npmrc` next to your `package.json`:

```ini
@qte77:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=${NODE_AUTH_TOKEN}
```

Locally, export `NODE_AUTH_TOKEN` as a classic PAT (or fine-grained token) with
`read:packages`. In CI, set it from a `NPM_READ_TOKEN` secret (or the job's
`GITHUB_TOKEN` when `permissions: packages: read` is granted).

## Docs in this kit

- **`README.md`** (you are here) — how to adopt & use the kit.
- [`BASELINE.md`](BASELINE.md) — the *why*: branding split, decisions (D1–D10), gotchas, roadmap.
- [`DISCOVERABILITY.md`](DISCOVERABILITY.md) — SEO / GEO / ASO.
- [`../DESIGN.md`](../DESIGN.md) — token source of truth.

## Contents

| File | From `DESIGN.md` | What |
|---|---|---|
| `tailwind/tokens.css` | `colors` · `data` · `typography` · `rounded` | Tailwind v4 `@theme` tokens — the `@qte77/ui-theme` npm package (see above) |
| `eyerest.css` | `colors` · `variants` · `data` | color tokens (default + 3 variants, light/dark, data arc) |
| `layout.css` | `spacing` · `rounded` · `shapes` · `components` | spacing/shape tokens + component bindings |
| `fonts.css` | `typography` | `@font-face` (WOFF2 + TTF fallback) + type tokens |
| `theme.js` | — | no-build cycler: `resolveTheme`/`nextTheme`/`THEME_CYCLE` + `themechange` |
| `a11y.css` | — | `.sr-only`, width-sizer, reduced-motion |
| `theme-toggle.html` | — | toggle markup + `aria-live` status region |
| `github-links.html` | — | toolbar repo + issues links; swaps `../../assets/images/icons/github-{black,white}.svg` by theme |
| `anti-fouc.html` | — | inline `<head>` guard snippet |
| `ci-verify.example.yml` | — | **optional** CI recipe for the polyfetch verify gate |
| `seo.js` / `seo.html` | — | portable SEO head — meta + OG/Twitter + JSON-LD (builder + template) |

## Load order (no-build)

```html
<head>
  <!-- 1. inline guard FIRST, before any stylesheet (paste anti-fouc.html) -->
  <link rel="stylesheet" href="brand/ui-kit/eyerest.css">
  <link rel="stylesheet" href="brand/ui-kit/fonts.css">
  <link rel="stylesheet" href="brand/ui-kit/layout.css">
  <link rel="stylesheet" href="brand/ui-kit/a11y.css">
  <script type="module" src="brand/ui-kit/theme.js"></script>
</head>
```

Place the `theme-toggle.html` markup in your toolbar; recolour charts on flip via
`document.addEventListener('themechange', e => chart.update())`. The optional
`github-links.html` adds repo + issues links the same way — vendor
`assets/images/icons/github-black.svg` + `github-white.svg` and point its
`background-image` `url()`s at the local copies.

## Fonts: WOFF2 for the web, TTF for baking

`fonts.css` serves WOFF2 (with a TTF fallback) from `../fonts/`. The brand-baking pipeline
(`../scripts/`) keeps the TTF/OTF because fonttools / cairosvg need desktop formats.
`install_fonts.py` should emit both.

## Self-hosting (no CDN)

Vendor everything the GUI needs — fonts (above) and any external JS libs (Chart.js, Fuse.js,
…) — into the repo and serve it from your own origin. Don't hotlink a CDN.

**Why:** no third-party requests (privacy), works offline / survives CDN outages, a simpler
Content-Security-Policy, supply-chain control, and clean GitHub-Pages portability.

**How:**

- **Fonts** → `../fonts/` via `install_fonts.py` + `fonts.css` (see above).
- **Libs** → a committed `vendor/` dir (e.g. `ui/public/vendor/chart.umd.min.js`); load via a
  plain `<script>` tag — no bundler needed. **Pin the exact version** in the file/commit;
  never track `@latest`.

## Favicon & logo

Both come from `brand/images/` (single source) — the same path-baked mark (resolves D7):

- **Favicon + site logo** = `brand/images/logo-mark.paths.dejavu.svg` (path-baked square
  mark; renders identically, no font dependency).
- These are **GitHub-native brand** assets used on UI surfaces for identity — only the
  *theme* (colors/fonts) is EyeRest.

Vendor the file into your site's `assets/` (same as fonts — a deployed site can't reference
another repo at runtime), then:

```html
<link rel="icon" type="image/svg+xml" href="/assets/logo-mark.svg">
<img class="site-logo" src="/assets/logo-mark.svg" alt="qte77">
```

For **`og:image`** use a raster (e.g. `brand/images/avatar_neutral.dejavu.png` or a
`render_og.py` card) — many platforms don't render SVG OG images.

## SEO

Portable SEO `<head>` parity with the Jekyll sites, framework-free (for the no-build / Vite
GUIs). Two options:

- **Author** [`seo.html`](seo.html) — copy into your `<head>`, fill the `{{PLACEHOLDERS}}`;
  meta lives in the served HTML (best for crawlers, no JS needed).
- **Generate** with [`seo.js`](seo.js) — `renderHead(cfg)` emits the same tags at build time
  and keeps the JSON-LD in sync (`BlogPosting` for posts, `WebSite` otherwise).

`og:image` should be a raster (a `render_og.py` card or `brand/images/avatar_*.png`). The
JSON-LD also feeds GEO / ASO — see [`DISCOVERABILITY.md`](DISCOVERABILITY.md).

## Verify with polyfetch — optional, recommended

Check the rendered UI headlessly with the shared
[`qte77/polyfetch-scrape`](https://github.com/qte77/polyfetch-scrape) stack — **check** that
the EyeRest branding actually rendered (tokens, theme cycle, a11y, fonts, favicon) and
**fetch** that URLs/assets return 200. Recommended before deploy; **not** a required gate.

```bash
# one-time browser install (shared, no per-repo dependency)
uv run --directory ../polyfetch-scrape patchright install chromium

# single-repo / in-project (point at your local/staging URL)
uv run --directory ../polyfetch-scrape python ../qte77/brand/scripts/gui-check.py \
  --url http://localhost:8137

# cross-repo / multi-project drift sweep (audit live tokens vs DESIGN.md)
uv run --directory ../polyfetch-scrape python ../qte77/brand/scripts/gui-check.py \
  --urls urls.txt
```

`--directory` points at wherever the `polyfetch-scrape` checkout lives. See
[`ci-verify.example.yml`](ci-verify.example.yml) to wire it into CI if/when you want it.
