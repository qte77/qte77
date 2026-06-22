<!-- markdownlint-disable MD024 no-duplicate-heading -->

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**Types of changes**: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`

## [Unreleased]

### Added

- `brand/ui-kit/github-links.html` + `assets/images/icons/github-black.svg` / `github-white.svg`: reusable GitHub repo/issues toolbar snippet that swaps GitHub's permitted black/white Octocat (Bootstrap Icons mark, MIT) by theme — dedupes the inlined mark across paperverse + agenthud, paired light/dark like the other monochrome icons; `assets/images/icons/README.md` documents the MIT-code / GitHub-trademark split (PR #131)
- `docs/doc-structure.md` + `docs/templates/README.template.md`: canonical README + document-hierarchy contract for the qte77 estate — value-first order (Hero → Badges → What → How → Why → Refs → License → `<tail>`), badge spec (License → Version → CI; static badges blue, status badges native — paperverse SSOT), front-door/conciseness rule, theme-aware `assets/images/` screenshot rule, `README`/`CONTRIBUTING`/`AGENTS`/`CLAUDE` split. This repo is the source of truth; the docs-governance skills/rules/plugins derive from it. `lychee.toml` excludes `docs/templates` (placeholder links)
- `docs/architecture.md`: mental model, authority chain, GHA pipeline diagrams, and roadmap — extracted from `README.md` so the profile front door stays concise (dogfoods the doc-structure contract)
- `docs/templates/CONTRIBUTING.template.md`: canonical CONTRIBUTING skeleton (`## Documentation hierarchy` + semi-automatic `## Releasing` + commands/conventions/branches) — the SOT the docs-governance plugin's CONTRIBUTING template derives from
- `CONTRIBUTING.md`: `## Documentation hierarchy` statement (one-audience-per-file map); `docs/doc-structure.md`: `## Releasing` canon note — semi-automatic flow for release-bearing repos (human bump PR → `tag-release` → `publish-release`; reusable workflows hosted in `qte77/.github`)
- `brand/ui-kit/seo.js` + `seo.html`: portable SEO head — meta + Open Graph + Twitter Card + JSON-LD (`BlogPosting`/`WebSite`), framework-free parity with the Jekyll sites; the JSON-LD also feeds GEO/ASO (PR #120)
- `brand/ui-kit/README.md` "Self-hosting (no CDN)": advice to vendor fonts + external JS libs (Chart.js / Fuse.js) into the repo and pin exact versions — privacy, reliability/offline, simpler CSP, supply-chain control, GitHub-Pages portability (PR #119)
- `brand/scripts/gen_ui_kit.py` + `make -C brand ui_kit`: generate `brand/ui-kit/eyerest.css` (color tokens) from `DESIGN.md` so the two never drift (decision D5); `--check` flags staleness (PR #118)
- `brand/DESIGN.md`: machine-readable `data-dark` block (was YAML comments only) so the dark data arc is generatable (PR #118)
- WOFF2 web fonts in `brand/scripts/install_fonts.py` (Inter + JetBrains Mono 400/700 from Fontsource); `fonts.css` prefers WOFF2 with TTF fallback (PR #118)
- `brand/ui-kit/`: no-build EyeRest UI kit — `eyerest.css` / `layout.css` / `fonts.css` (generated from `DESIGN.md`), `theme.js` cycler (`◐/○/●`, `html[data-theme]`, `qte77-theme` key, `themechange` event), `a11y.css` + `theme-toggle.html` (dynamic `aria-label`, `aria-live`, width-sizer, `prefers-reduced-motion`), `anti-fouc.html`, `README.md`, optional `ci-verify.example.yml`; `brand/README.md` lists it (PR #113)
- `brand/scripts/render_og.py`: SVG→cairosvg OG/figure renderer (1200×630, EyeRest palette, glyph-safety lint) (PR #113)
- `brand/scripts/gui-check.py`: optional polyfetch-scrape UI verifier, dual-scope (in-project gate + cross-repo token-drift sweep) (PR #113)
- `brand/ui-kit/BASELINE.md`: consolidated GUI-baseline findings (GitHub-vs-UI branding split, decisions D1–D10, portable gotchas) + actionable roadmap (PR #113)
- `brand/ui-kit/README.md` "Favicon & logo": favicon + site logo resolved to `brand/images/logo-mark.paths.dejavu.svg` (decision D7) (PR #114)
- `brand/ui-kit/DISCOVERABILITY.md`: SEO / GEO / ASO (incl. Agentic Search Optimization) machine-readability scope + roadmap, cross-referenced with `BASELINE.md` (PR #115)
- `brand/fonts/LICENSES/`: canonical, committed font-license texts — the single source of truth a consumer vendors a font *and* its license from. `OFL.txt` (SIL OFL 1.1, stacked copyright headers for Inter, JetBrains Mono, Cascadia, Fira, Source Code Pro, IBM Plex Mono), `DejaVu-LICENSE.txt` (Bitstream Vera + Arev), `UbuntuMono-UFL.txt` (Ubuntu Font Licence 1.0), and a `README.md` font→license manifest; `brand/.gitignore` un-ignores `LICENSES/` while font binaries stay ignored
- `brand/social-previews.toml`: expanded from 1 to 12 repo entries covering the main estate (doc-pipeline-engine, paperverse, polyforge-orchestrator, claude-code-plugins, so101-biolab-automation, pseudonymize-text, i3mega-pipettebot, gha-issue-triage, diagramforge, agentic-job-offer-to-application-kit, ai-agents-research)
- `CONTRIBUTING.md`: minimal workflow doc — scope, commands, Conventional Commits, branch naming, CHANGELOG rule, pre-merge checklist
- `.markdownlint.jsonc`: project policy disabling MD013/MD041/MD060, allowing inline HTML
- `lychee.toml`: link-check config with bot-blocking accept codes and exclusion patterns
- `brand/scripts/upload_social_preview.py`: experimental CLI uploader that targets the undocumented internal endpoint used by the Settings UI; auth via `GH_USER_SESSION` cookie, GitHub provides no public API for this (PR #43)
- `docs/gh-endpoints/`: catalog of GitHub functionality not covered by REST/GraphQL/`gh` CLI; `INDEX.md` lists 7 confirmed gaps with first-party citations, `HOWTO.md` documents the methodology, `social-preview.md` reverse-engineers the upload endpoint (PR #43)
- `brand/images/`: containment subfolder for visual assets — `logo-mark.svg`, `logo-wordmark.svg`, `avatar_dark.png`, `avatar_light.png` (PR #47)
- `brand/.gitignore`: brand-local ignore rules so `brand/` is self-contained (PR #47)
- `brand/Makefile`: `IMAGES`/`FONTS`/`DIST`/`SCRIPTS` path constants; help target expands them at print time (PR #47)
- Tracking issue [#44](https://github.com/qte77/qte77/issues/44): graduate `docs/gh-endpoints/` to a standalone `qte77/gh-endpoints` repo once it has 3+ documented endpoints
- `brand/scripts/render_wordmark.py`: rasterizes `logo-wordmark.paths.<font>.svg` to `wordmark_{dark,light}.<font>.png` (960×320) via resvg (PR #55)
- Root `Makefile`: thin delegator forwarding brand targets to `brand/Makefile` (PR #55)
- `brand/images/wordmark_{dark,light}.dejavu.png`: 960×320 rasters for embedding where SVG can't be used (PR #55)

### Changed

- `docs/doc-structure.md`: the doc-hierarchy `CLAUDE.md` row now accepts a **symlink** as a valid pointer form (was `@AGENTS.md` import only) — matches how this repo links `CLAUDE.md` → `AGENTS.md`
- Profile `README.md`: restructured to the value-first doc-structure contract (Hero → Badges → What → How → Why → Refs → License → tail); Mental Model / Authority Chain / Roadmap moved to `docs/architecture.md`; Positioning folded into Why; profile tail kept (Tools · Posts · Profile · Lineage), with Lineage carrying the RAPID/CABIO provenance + repo links
- `brand/ui-kit/eyerest.css`: now generated by `gen_ui_kit.py` (token values unchanged; formatting normalized) (PR #118)
- `brand/ui-kit/{layout,fonts}.css`: headers corrected — hand-authored; only `eyerest.css` is generated (PR #118)
- `brand/ui-kit/` docs streamlined to one-owner-per-topic — `README.md` = usage (front door), `BASELINE.md` = rationale/decisions/roadmap, `DISCOVERABILITY.md` = SEO/GEO/ASO; removed the duplicated verify commands + per-file token re-listing from `BASELINE.md`; added a doc map to `README.md` (PR #117)
- Profile `README.md`: wordmark centered horizontally via `<p align="center">`, updated to `brand/images/` paths (PR #47)
- `brand/README.md`, `docs/github-image-theming.md`: live-example paths updated to `brand/images/` (PR #47)
- `brand/scripts/render_avatar.py`: `BRAND` constant + `IMAGES` resolve to subfolder (PR #47)
- Brand artifact naming: font-suffixed (`*.paths.dejavu.svg`, `*_{dark,light}.dejavu.png`) so multiple bake fonts can coexist; `FONT ?= dejavu` parameterizes the pipeline (PR #55)
- Canonical bake font switched to DejaVu Sans Mono Bold (clean `7` glyph, matches Linux fontconfig fallback for the `.text.svg` font-family chain) (PR #55)
- `brand/images/logo-mark.text.svg`: `q7_` composition centered in 80×80 canvas using DejaVu metrics (PR #55)
- `brand/images/logo-wordmark.text.svg`: underscore aligned to visible glyph edges of `t` (left) and last `7` (right) (PR #55)
- `brand/Makefile` / root `Makefile`: `.SILENT` + `.ONESHELL` for cleaner recipes (PR #55)

### Fixed

- `brand/scripts/install_fonts.py`, `brand/README.md`, `brand/Makefile`: corrected the inaccurate "all fonts are SIL OFL 1.1" claim — the downloader pulls three license families (OFL 1.1, Ubuntu Font Licence 1.0 for Ubuntu Mono, Bitstream Vera + Arev for the canonical DejaVu bake font); docs now list every downloaded font with its actual license and point to `fonts/LICENSES/`
- `brand/scripts/svg_text_to_paths.py`: honor `letter-spacing` attribute when shaping; previously paths SVGs spaced glyphs further apart than the canonical text SVG (PR #55)

### Security

- `brand/ui-kit/seo.js`: escape `<` `>` `&` (and U+2028/U+2029) in the inline JSON-LD `<script>` block, so a config value containing `</script>` can't break out of the script context — prevents XSS in the generated head HTML (PR #121)

## [0.3.0] - 2026-04-26

### Added

- `brand/`: visual identity surface
  - `brand/palette.toml` — GitHub Primer color tokens (light + dark)
  - `brand/logo-mark.svg` (80×80) — `q7_` mark in JetBrains Mono Bold, `font-feature-settings 'onum' 1`, accent-colored underscore raised via `dy="-5"` for terminal-cursor cue
  - `brand/logo-wordmark.svg` (240×80) — `qte77` wordmark with accent underline starting beneath the `t` glyph
  - Both adaptive via inline `@media (prefers-color-scheme: dark)`
  - `brand/avatar_dark.png` / `brand/avatar_light.png` — 920×920 rasters of the mark for GitHub account avatar (UI-only upload)
- `brand/scripts/install_fonts.py`: downloads Inter + JetBrains Mono (OFL) from Fontsource CDN
- `brand/scripts/svg_text_to_paths.py`: converts SVG `<text>` to `<path>` via uharfbuzz + fontTools so renderer-agnostic raster output is pixel-identical
- `brand/scripts/render_avatar.py`: rasterizes `logo-mark.svg` via `text_to_paths` + resvg into both theme variants
- `brand/scripts/generate_social.py`: Pillow-based 1280×640 social preview generator driven by `brand/social-previews.toml`
- `brand/Makefile`: `setup_brand_fonts`, `brand_paths`, `brand_avatar`, `brand_social`, `brand_clean`, `brand` (full refresh), `help`
- `docs/github-image-theming.md`: first-party-sourced comparison of three theme-aware image techniques (`<picture>`, `#gh-*-mode-only` URL fragments, inline `@media` in SVG)
- Profile `README.md`: wordmark inline at the top
- Workspace governance scaffolding: `AGENTS.md`, `AGENT_LEARNINGS.md`, `AGENT_REQUESTS.md`, `.claude/rules/{core-principles,context-management,compound-learning}.md`, `.claude/scripts/statusline.sh` (PR #42)

### Fixed

- `brand/scripts/svg_text_to_paths.py`: parse SVG with `defusedxml.fromstring` instead of stdlib `ElementTree.fromstring` (Bandit B314)
- `brand/scripts/install_fonts.py`: validate `https://` scheme before `urllib.request.urlopen` (Bandit B310)

### Security

- Hardened SVG XML parsing against billion-laughs / external-entity attacks (defusedxml)
- Hardened font download against non-https URL schemes

## [0.2.0] - 2026-04-24

### Changed

- `README.md`: SVGs and Topics audit — synced visual surface with current repo state (PR #37)
- `assets/images/`: archived legacy diagrams retired during audit; `mental-model.svg` and `pipeline-layers.svg` remain as canonical

## [0.1.0] - 2026 (initial profile state)

### Added

- Profile README with bio, mental-model SVG, pipeline-layers SVG, topics, tools, posts, lineage
- `assets/images/mental-model.svg` and `assets/images/pipeline-layers.svg` with inline `@media (prefers-color-scheme: dark)` for adaptive theming
