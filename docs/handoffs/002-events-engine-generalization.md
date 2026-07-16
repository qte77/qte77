---
plan: ../plans/002-events-engine-generalization.md
status: not started — build phase 1 (events-core) first
updated: 2026-07-16
---

# Handoff — Events-engine generalization

Onboarding for the next session. Full detail + code/file/source map:
[plan 002](../plans/002-events-engine-generalization.md). Read the plan first (its "Source map" sections
for fo-scraper + sfclarity + estate) — you should not need to re-explore the repos. Tracking issue:
qte77/qte77 **#156**.

## Where things stand

Nothing built yet. This generalizes the **calendar/venue events** domain shared by **fo-scraper-miwi**
(Python/Cloudflare, no-build vanilla JS) and **sfclarity** (React/Vite/Supabase, has the OSM map) into
two NEW repos: **`qte77/events-core`** (Python engine) and **`qte77/events-ui`** (`@qte77/events-ui`
React kit). Distinct from `@qte77/a2ui-agui-kit` (agent events).

Owner decisions already made (this session): generalize the calendar-event engine; standardize the UI on
React/Vite (fo-scraper migrates off vanilla + relaxes its strict CSP). fo-scraper carries the paired
ADRs — `docs/decisions/0007` (D1, PR #85, open) and `0008` (React, PR #86, open) — and a carry-over
`docs/handoffs/012-*`. **This plan + handoff were authored from the fo-scraper session and are UNCOMMITTED
in qte77/qte77** — first, commit them here (`docs(002): …`) and link #156.

## How to handle it (order)

1. **Build `events-core` FIRST (phase 1).** Backend-only, no React, reaches green now, and it delivers
   fo-scraper's durability + the coordinates the map needs, shared with sfclarity immediately. Do NOT
   start the React migration first.
2. **`events-core`** = new `qte77/events-core`, Python, `uv`. Mirror polyfetch's "call from another repo
   via `uv run --directory ../events-core`" contract. Port the models from fo-scraper
   `src/fo_scraper/models.py`; port geocode from sfclarity's offline ops pipeline (OSM Nominatim); two
   store adapters behind one `EventStore` Protocol — **D1** (fo-scraper) + **Supabase** (sfclarity, from
   `useEventsQuery.ts` / `events_enriched`). TDD: models + dedupe (`sha1(source_id|norm(name)|start_date)`)
   + geocode tests red → green.
3. **Wire consumers to `events-core`.** fo-scraper `build_ui_data.py` → `events_core.export.snapshot(D1Store())`
   (keep its `--require-events`/`--require-sitekey` guards + `sources.json`/`config.json` local).
   sfclarity swaps its inline model/geocode for `events-core` + the Supabase adapter.
4. **`events-ui` (phase 2)** — React/Vite, consumes `@qte77/ui-theme`; seed from sfclarity components
   (Map superset) + fo-scraper (filters/Insights/Trip/export superset). Publish to GitHub Packages.
5. **Then** fo-scraper React migration (phase 3, per its ADR-0008), shared map + Ctrl+K (phase 4),
   Ctrl+I Ask-AI (phase 5).

## First actions on resume

- Commit this plan + handoff in qte77/qte77 (`docs(002)…`); link them on #156.
- Create `qte77/events-core` (repo + `pyproject.toml`, `uv`); branch `feat/events-core-models`; port
  `Event`/`Source`/`Provenance` from fo-scraper `src/fo_scraper/models.py` (drop FO-specific scoring;
  `fo_relevance` → optional `relevance`); write model + dedupe tests red, then green.

## Working style

- **Strict TDD, behavior-first.** For `events-core`'s **modules** (models, dedupe, geocode, the
  `EventStore` adapters, export) write the tests FIRST — model the expected/desired behavior red, then
  implement green. TDD the modules, NOT trivial scripts/glue (a one-line CLI wrapper or a `build_ui_data`
  shim needs no unit test — smoke it). Value-add tests only; never chase coverage with trivial tests.
- **Strict lint + type + security ALWAYS**, on every file (ruff/pyright/bandit-equiv for Python; the
  target repo's gate for TS). Non-negotiable regardless of whether a file has unit tests.

## Gotchas

- **Cross-repo hygiene**: delegate content edits to a subagent working INSIDE each target repo; the main
  agent does git plumbing only. Don't Read/edit a sibling's files from an orchestrating session.
- Prefix every git/gh with `env -u GH_TOKEN -u GITHUB_TOKEN` (both vars are invalid, shadow the real
  credential → 403). Commit `--no-gpg-sign`; identity `qte77 <93844790+qte77@users.noreply.github.com>`.
  Plain-text docs, no emoji/glyphs.
- **sfclarity is at `/workspaces/sfsanity/sfclarity`** (different parent, NOT `/workspaces/qte77`), and is
  React/Vite/Supabase — do not assume fo-scraper's stack. fo-scraper's GitHub repo is `qte77/__fo-scraper_miwi`
  (double underscore).
- **Do NOT copy sfclarity's map CSP** (`img-src https:` wildcard) or its disabled attribution. fo-scraper
  scopes tiles (a proxy Function or exact host) and MUST show "(c) OpenStreetMap contributors". The OSM
  map needs coordinates → build `events_core.geocode` first (phase 1).
- fo-scraper CSP is strict `default-src 'self'`; ADR-0008 relaxes it only to the minimum under Vite (keep
  hash/nonce `script-src 'self'`, no `unsafe-eval`).
- GitHub Packages needs `NODE_AUTH_TOKEN`/`NPM_READ_TOKEN` even for public packages — verify tokenless
  via `npm pack` → `npm install <tgz>` (same friction as plan 001's P4/P5).
- Don't conflate with `@qte77/a2ui-agui-kit` — its "events" are AG-UI agent events, a different domain.
