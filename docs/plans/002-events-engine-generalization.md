---
status: proposed — not started
phase: phase 1 (events-core) is the recommended first build
handoff: ../handoffs/002-events-engine-generalization.md
updated: 2026-07-16
---

# Events-engine generalization (calendar/venue events + React ui-kit)

Cross-repo plan. Extract the duplicated **calendar/venue events** domain shared by two dashboards —
fo-scraper-miwi and sfclarity — into a shared Python engine (`events-core`) and a shared React ui-kit
(`events-ui`), mirroring what plan 001 did for the agent-UI seam. This doc is the **source map** so a
fresh session executes without re-exploring the repos. Onboarding + how-to-run is in the paired
[handoff](../handoffs/002-events-engine-generalization.md). Distinct from `@qte77/a2ui-agui-kit`, whose
"events" are AG-UI *agent/protocol* events — this is real-world **calendar** events.

## Why

Two dashboards render the same real-world-event domain from a duplicated stack:

1. **sfclarity** (React/Vite + Supabase) — already has an interactive **OSM map** and geocoded venues.
2. **fo-scraper-miwi** (no-build vanilla ES modules + Pydantic + Cloudflare Pages) — richer filters,
   Insights, Trip planner, .ics/CSV export, deep-link state; **no coordinates/map yet**.

The event model, geocoding, dedupe, storage, and the List/Calendar/Map views are duplicated (or about
to be). Generalize once — the same move the estate already made for agent UI (plan 001).

## Repo + role map

| Local path | GitHub | Role |
| --- | --- | --- |
| `/workspaces/qte77/qte77` | `qte77/qte77` | Estate hub; governance; publishes `@qte77/ui-theme` (tokens). Tracking issue **#156**. |
| `/workspaces/qte77/fo-scraper-miwi` | `qte77/__fo-scraper_miwi` | FO events dashboard. **events-core seed** (Pydantic models + build) + a **consumer** (migrates to React). |
| `/workspaces/sfsanity/sfclarity` | sfclarity (confirm owner/name) | SF events dashboard. **events-ui superset seed** (React + map) + the **Supabase adapter** source. NOTE: different parent dir (`/workspaces/sfsanity`, not `/workspaces/qte77`). |
| `/workspaces/qte77/events-core` | `qte77/events-core` | NEW. Python events engine (`uv`-consumed like polyfetch). I own it — clean squash-merges. |
| `/workspaces/qte77/events-ui` | `qte77/events-ui` | NEW. React/Vite kit `@qte77/events-ui` (views + OSM map + Ctrl+K palette). Clean squash-merges. |

Estate conventions (apply everywhere): prefix all git/gh with `env -u GH_TOKEN -u GITHUB_TOKEN` (both
vars are invalid and shadow the real credential → 403 on writes); identity
`qte77 <93844790+qte77@users.noreply.github.com>`; commits `--no-gpg-sign`; conventional commits; branch
per topic; squash-merge on green CI then prune; plain-text docs, no emoji/glyphs. **Cross-repo hygiene:**
delegate content edits to a subagent working inside the target repo; the main agent does git plumbing.
The consumer repos may enforce `required_signatures` → per-PR `--admin` merge (bypasses only the
signature gate, never a failing/absent check).

## Owner decisions (2026-07-16)

1. Generalize the **calendar/venue events engine** as a new shared concern (distinct from `a2ui-agui-kit`).
2. Standardize the UI on **React/Vite**; **fo-scraper migrates off no-build vanilla JS** and relaxes its
   strict `default-src 'self'` CSP to the minimum the toolchain needs (hash/nonce `script-src 'self'`,
   map tiles via a proxy or scoped `img-src`; NOT sfclarity's `img-src https:` wildcard). Recorded in
   fo-scraper `docs/decisions/0008-react-ui-kit-supersedes-no-build-strict-csp.md`.

## Proposed repos

- **`qte77/events-core`** (Python) — models, dedupe, OSM geocode, storage adapters (D1 + Supabase),
  snapshot export. Consumed via `uv run --directory ../events-core` (polyfetch precedent).
- **`qte77/events-ui`** (React/Vite npm `@qte77/events-ui`, GitHub Packages) — the dashboard components.
  Consumes `@qte77/ui-theme`.

## Source map — fo-scraper (events-core seed + React consumer)

Base: `/workspaces/qte77/fo-scraper-miwi`.

| File | Symbols / content | Role in this plan |
| --- | --- | --- |
| `src/fo_scraper/models.py` | `Event` (name, source_id, organizer, start_date, end_date, city, country, region, venue, format[in_person/virtual/hybrid], audience, topics[], registration_url, source_url, price_hint, `fo_relevance` float, scraped_at, notes); `Source`; `Provenance` (verified, validated_date, first_party_urls) — `extra="forbid"` | → `events_core.models`. `fo_relevance` becomes optional generic `relevance`. |
| `scripts/build_ui_data.py` | `main(argv)` argparse (positional out_dir, results_dir, `--require-events`/`--require-sitekey`), `build_events`, `build_sources`, `latest_results`, `_has_events` | → `events_core.ingest`/`export`. Guards + config.json stay fo-scraper. |
| `config/sources.json` | 23 sources + `_meta` | STAYS fo-scraper (registry data). |
| `ui/src/app.js` | state, `render()` (dispatches `viewchange`), `bindControls`, `initFiltersPane`, `initScrollNav`, `applyDrill`, `renderChips` | → replaced by `events-ui` React shell. |
| `ui/src/dashboard.js` | `renderList`, `filterEvents`, `activeFilters`, `formatBucket`, `parseDate` | → `events-ui` List/Tiles + filter logic (shareable to events-core as pure fns). |
| `ui/src/calendar.js` | `renderCalendar` | → `events-ui` Calendar. |
| `ui/src/insights.js` | `renderInsights` (Chart.js, drill via `insights-drill` event) | → `events-ui` Insights. |
| `ui/src/trips.js` | `renderTrips` | → `events-ui` Trip. |
| `ui/src/data.js` | `fetchJSON`, `loadWithFallback(real, demo)` | → `events-ui` data loader (or `/api/events`). |
| `ui/src/urlstate.js` | `restoreState`, `persistState`, `PARAM_KEYS` (view/region/organizer/format/upcoming/groupby/search/window) | → `events-ui` deep-link state. |
| `ui/src/modal.js` | event modal + `travelLinks` (Getting-there deep links) | → `events-ui` modal. |
| `ui/src/ics.js`, `ui/src/csv.js` | `icsForMany`/`veventFor`, `downloadCsv` | → `events-ui` export. |
| `ui/src/stars.js`, `ui/src/scrollnav.js`, `ui/src/provenance.js`, `ui/src/format.js` | watchlist; toolbar scroll-nav (↑/↓ + Jump-to, shipped PR #77/#84); provenance popover; formatting | → `events-ui` components. |
| `ui/assets/linear.css` | Linear-style theme + component CSS | → reconcile with `@qte77/ui-theme` tokens. |
| `ui/app/index.html` | strict CSP `<meta>` (`default-src 'self'; img-src 'self' data:`), toolbar structure | CSP changes under ADR-0008. |
| `functions/app/_middleware.js`, `functions/claim.js`, `functions/request_access.js`, `functions/_lib/{session,store,ratelimit}.js` | per-user invite gate (KV `ACCESS_REQUESTS`), gates ONLY `/app/*` | STAYS fo-scraper (ADR-0006). A `/api/*` route is NOT gated by this. |
| `docs/decisions/0006` / `0007` / `0008` | gate / D1 (PR #85) / React (PR #86) | 0007 D1 → `events_core.store.d1`; 0008 = the React decision. |
| `tests/test_ui_data.py` | require-events/keep-existing/harvest-write cases (PR #84) | model/dedupe/geocode tests → events-core; glue tests stay. |

Open PRs: **#84** (011 durable data + guards, merged+deployed), **#85** (ADR-0007 D1, open), **#86**
(ADR-0008 + carry-over handoff, open).

## Source map — sfclarity (events-ui superset seed + Supabase adapter + geocode)

Base: `/workspaces/sfsanity/sfclarity/frontend` (React/Vite; `package.json`: `pigeon-maps ^0.22.1`, `vite ^7`).

| File | Symbols / content | Role in this plan |
| --- | --- | --- |
| `src/components/map/MapView.tsx` | `pigeon-maps` `Map`+`Overlay`; `lightTiles` = `tile.openstreetmap.org/{z}/{x}/{y}.png`, `darkTiles` = `basemaps.cartocdn.com/dark_all/...`; `attribution={false}` (policy gap — re-enable) | → `events-ui` Map. pigeon-maps core (Web-Mercator + `<img>` tile grid) is portable. |
| `src/components/map/EntityMarker.tsx` | lone pin vs numbered density pill | → `events-ui` marker. |
| `src/lib/mapPins.ts` | `pinKey`, `dedupePins`, `eventsAtPin`, `densityTier` (pure, zero-dep) | → `events_core.dedupe` (server) + `events-ui` (client density). |
| `src/components/a2ui/VenueMap.tsx` | sizing wrapper (`height='60vh'`) | → `events-ui`. |
| `src/components/views/EventsView.tsx` | expand/collapse map (`?map=0` URL-synced, `aria-expanded`, mount/unmount); pin-click → list filter (banner) | → `events-ui` expandable-map UX (the pattern fo-scraper wants). |
| `src/hooks/useEventsQuery.ts` | `parseCoords("lat,lng")`; `.from('events_enriched').select(...).eq('published', true)`; `EventItem.coords?: [number,number]` | → `events_core.store.supabase` + coord parsing. |
| `src/contexts/ThemeContext.tsx` | `[data-theme]` drives light/dark tiles | → `events-ui` theme wiring. |
| `public/_headers` | CSP `img-src 'self' data: https:` (wildcard) | DO NOT copy — fo-scraper scopes tiles (proxy or exact host). |
| Supabase `events_enriched` (table) + offline `ops` geocode pipeline (service-role, `coordinates` "lat,lng") | server-side geocode | → `events_core.geocode` (OSM Nominatim) + `events_core.store.supabase`. |

## Source map — estate (coupling + tokens)

| Artifact | Where | Use here |
| --- | --- | --- |
| `@qte77/ui-theme` (v0.2.0) | qte77/qte77 `brand/ui-kit` from `brand/DESIGN.md` (Tailwind v4 `@theme`) | `events-ui` consumes for tokens. |
| `@qte77/a2ui-agui-kit` (v0.3.0) | `/workspaces/qte77/a2ui-agui-kit` | Reference for the React package shape; possibly reuse primitives. NOT the same "events". |
| `qte77/protocols` | `scripts/sync.sh` pinned-tag curl vendoring | Precedent for a shared **types** artifact if `events-core` model types are shared to `events-ui` as JSON Schema. |
| Coupling mechanisms | — | GitHub Packages npm (`.npmrc` + `NODE_AUTH_TOKEN`/`NPM_READ_TOKEN`) for `events-ui`; `uv run --directory ../events-core` for Python; pinned-tag curl for schema. No submodules. |

## events-core — extraction scope (phase 1 build spec)

Move → `events-core` (generic): the `Event`/`Source`/`Provenance` models; `ingest.load(harvest) -> list[Event]`;
`dedupe.key` (canonical `event_key = sha1(source_id|norm(name)|start_date)`); `geocode.enrich` (OSM
Nominatim, cached, ODbL attribution → `latitude`/`longitude`); `store.d1` + `store.supabase` adapters;
`export.snapshot(store) -> list[dict]` (upcoming-first, `exclude_none`).

Store interface (the D1/Supabase seam):

```python
class EventStore(Protocol):
    def upsert(self, events: Iterable[Event]) -> int: ...
    def all(self, *, upcoming: bool = False) -> list[Event]: ...
    def export_snapshot(self) -> list[dict]: ...   # feeds build_ui_data / the deploy
```

STAYS app-specific: `config/sources.json` registry data; `fo_relevance` scoring semantics; the invite
gate; deploy policy (`config.json` sitekey, `wrangler.jsonc`, Makefile guards); branding + demo data;
the FO scraping pipeline (writes into events-core via `ingest` but is domain code).

fo-scraper consumption (phase 1, pre-React): `build_ui_data.py` shrinks to
`events_core.export.snapshot(D1Store())` → writes `events.json` (keeps the deploy guards +
`sources.json`/`config.json` local).

## events-ui — component inventory (phase 2)

Seed from sfclarity (superset for Map) + fo-scraper (superset for filters/Insights/Trip/export):
List, Tiles, Calendar, **Map** (expandable, pins→filter, OSM tiles + attribution), Insights (Chart.js),
Trip, filters + chips + deep-link state, .ics/CSV export, event modal + travel links, watchlist,
**Ctrl+K command palette** (new — pure client), later **Ctrl+I Ask-AI** (per-app `/api/ask` RAG proxy).

## Phasing

0. **Ratify** — this plan + issue #156 + fo-scraper ADR-0008 (PR #86); re-scope fo-scraper ADR-0007 (D1)
   as the `events-core` D1 adapter.
1. **`events-core`** — package skeleton + models + dedupe + geocode + D1 adapter + Supabase adapter +
   snapshot export; fo-scraper `build_ui_data` consumes it. **Recommended first build** — backend-only,
   no React, delivers fo-scraper durability + the coords the map needs, shared with sfclarity now.
2. **`events-ui`** — seed from sfclarity; publish `@qte77/events-ui`.
3. **fo-scraper React migration** — Vite build consuming `events-ui`; preserve the invite gate + the
   patchright e2e gates (`make ui_check`/`ui_matrix`, borrow `../polyfetch-scrape` venv).
4. **Shared features** — OSM map (rides coords) + Ctrl+K palette into `events-ui`.
5. **Ctrl+I Ask-AI** — per-app gated `/api/ask` RAG proxy (LLM server-side, browser stays same-origin).

## OSM map / CSP notes (for phase 4)

fo-scraper's CSP is `img-src 'self' data:` — external tiles violate it. Options: (a) a **tile-proxy Pages
Function** (`/tiles/:z/:x/:y` → cache in Cache API/R2 → OSM), browser stays `'self'`; or (b) scoped
`img-src tile.openstreetmap.org`. Either way ADD visible "(c) OpenStreetMap contributors" attribution
(sfclarity disabled it). Coordinates are a hard prerequisite → `events_core.geocode` (phase 1).

## Open questions

- One Python `events-core`, or split ingest/store from a shared **types** artifact for `events-ui` (TS
  via `protocols`-style JSON Schema, so the model isn't defined twice)?
- Dedupe key for undated / cross-source duplicates.
- `relevance` in core (nullable) vs each app's domain layer (recommend: nullable generic field in core).
- Geocode cache location (repo file vs store table vs R2), shared across apps.
- How tight fo-scraper's CSP stays under Vite (hash/nonce vs unsafe-inline; no unsafe-eval).
- Greenlight `events-core` (phase 1) alone first vs the whole program.

## Refs

- Tracking issue: qte77/qte77 #156.
- Estate: plan 001 (agent-UI unification); `a2ui-agui-kit`; `protocols`; `@qte77/ui-theme`.
- fo-scraper: `docs/decisions/0007` (D1, PR #85), `0008` (React, PR #86); PR #84 (011 durability); the
  carry-over `docs/handoffs/012-qte77-events-generalization-tracking-issue.md`.
- sfclarity: `frontend/src/components/map/*`, `lib/mapPins.ts`, `hooks/useEventsQuery.ts`.
