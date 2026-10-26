# Discoverability — SEO / GEO / ASO

How qte77-branded UIs get found and parsed, across three audiences. Companion to
[`BASELINE.md`](BASELINE.md) (the theme / a11y / verify baseline); this doc covers the
machine-readability layer.

| Layer | Audience | Goal |
|---|---|---|
| **SEO** | human search engines | rank + rich result (meta, OG, JSON-LD) |
| **GEO** | generative answer engines | be cited in AI answers (`llms.txt`, structured data) |
| **ASO** | autonomous agents | discover / parse / act on the site (semantic + stable hooks) |

None of the three are kit *units* yet, but the ui-kit already lays incidental foundations,
and GEO + ASO overlap enough to share one convention.

## What the ui-kit already contributes

- **a11y baseline** ([`a11y.css`](a11y.css), [`theme-toggle.html`](theme-toggle.html)) — the
  accessibility tree is what most browsing **agents** read, so dynamic `aria-label`,
  `role="status"` / `aria-live`, and semantic markup are ASO foundations for free.
- **stable element ids** — `#theme-toggle`, `#theme-status` give agents predictable hooks.
- **social cards** — favicon / logo + `og:image` +
  [`../scripts/render_og.py`](../scripts/render_og.py) cover the OG sliver of SEO.

## SEO — head partial (shipped)

[`seo.html`](seo.html) (authored template) + [`seo.js`](seo.js) (`renderHead(cfg)` build-time
builder) give portable head parity with the Jekyll sites, framework-free:

- `<title>` + `<meta name="description">` + `<link rel="canonical">`
- Open Graph + Twitter Card (`og:title/description/image/url`, `twitter:card`)
- **JSON-LD** (`schema.org` `WebSite` / `SoftwareSourceCode` / `BreadcrumbList`) — also feeds
  GEO + ASO
- `og:image` wired to a `render_og.py` card (raster; SVG OG is unreliable)

## GEO — answer-engine readiness

- **`llms.txt`** via the org's `gha-llms-txt-action` (a machine-readable map for LLMs).
- Structured data (the same JSON-LD as SEO) + clean semantic HTML + concise summaries.

## ASO — agentic search optimization

Optimizing so autonomous agents can **find, parse, and act**:

- **parse** — semantic HTML + the a11y tree + JSON-LD (shared with SEO / GEO).
- **find** — `llms.txt` + stable URLs + a predictable nav.
- **act (read-only)** — stable selectors / `data-*` hooks (e.g. `#theme-toggle`) so an agent
  can drive controls deterministically.
- **act (interactive)** — agents *driving* the UI is the **AG-UI / A2UI** domain
  (`agenthud-agui-a2ui`), not the static kit; this doc stops at making the surface
  agent-legible.

## Roadmap

**SEO head partial is shipped** — `seo.js` (builder) + `seo.html` (template); meta +
canonical + OG / Twitter + JSON-LD (`BlogPosting`/`WebSite`). Remaining work (the GEO/ASO
machine-readability convention, and later aligning interactive agent-driving with AG-UI / A2UI)
is tracked in **[issue #111](https://github.com/qte77/qte77/issues/111)** alongside the rest
of the ui-kit roadmap, not as a second checklist here.

## See also

- [`BASELINE.md`](BASELINE.md) — theme / a11y / verify baseline (this doc's companion).
- [`DESIGN.md`](../DESIGN.md) — EyeRest tokens (source of truth).
- `gha-llms-txt-action` — GEO `llms.txt`; `agenthud-agui-a2ui` — interactive agent UI.
