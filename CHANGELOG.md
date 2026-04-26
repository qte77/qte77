<!-- markdownlint-disable MD024 no-duplicate-heading -->

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**Types of changes**: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`

## [Unreleased]

### Added

- `brand/scripts/upload_social_preview.py`: experimental CLI uploader that targets the undocumented internal endpoint used by the Settings UI; auth via `GH_USER_SESSION` cookie, GitHub provides no public API for this (PR #43)
- `docs/gh-endpoints/`: catalog of GitHub functionality not covered by REST/GraphQL/`gh` CLI; `INDEX.md` lists 7 confirmed gaps with first-party citations, `HOWTO.md` documents the methodology, `social-preview.md` reverse-engineers the upload endpoint (PR #43)
- `brand/images/`: containment subfolder for visual assets — `logo-mark.svg`, `logo-wordmark.svg`, `avatar_dark.png`, `avatar_light.png` (PR #47)
- `brand/.gitignore`: brand-local ignore rules so `brand/` is self-contained (PR #47)
- `brand/Makefile`: `IMAGES`/`FONTS`/`DIST`/`SCRIPTS` path constants; help target expands them at print time (PR #47)
- Tracking issue [#44](https://github.com/qte77/qte77/issues/44): graduate `docs/gh-endpoints/` to a standalone `qte77/gh-endpoints` repo once it has 3+ documented endpoints

### Changed

- Profile `README.md`: wordmark centered horizontally via `<p align="center">`, updated to `brand/images/` paths (PR #47)
- `brand/README.md`, `docs/github-image-theming.md`: live-example paths updated to `brand/images/` (PR #47)
- `brand/scripts/render_avatar.py`: `BRAND` constant + `IMAGES` resolve to subfolder (PR #47)

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
