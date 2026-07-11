---
status: in-progress
phase: consumer wave (Phases 4/5/7/8) remaining
handoff: ../handoffs/001-estate-ui-engine-unification.md
updated: 2026-07-11
---

# Estate UI + workflow-definition unification

Cross-repo plan. Extract the duplicated A2UI UI seam into shared npm packages and
unify the two workflow engines' definition schema. This doc is the **source map** so
a fresh session executes the remaining work without re-exploring. Onboarding +
how-to-run is in the paired [handoff](../handoffs/001-estate-ui-engine-unification.md).

## Why

Two problems, found by comparing the repos:

1. **UI duplication.** `ldnmxx-hack/ui` is a fork of `agenthud-agui-a2ui/ui`. The A2UI
   seam (`agent/applyA2UIEvent.ts`, `theme/a2uiTheme.ts` byte-identical; `agent/contract.ts`
   ~90%), the presentational trio (`A2UISurface`/`CatalogViewer`/`EventStream`), and the
   EyeRest `@theme` token block (hand-copied from `brand/DESIGN.md`) were duplicated and
   silently drifting. Executes `agenthud-agui-a2ui#211` / its plan 013 Wave 2.
2. **Engine duplication.** `qte77/azure-doc-workflows` (Python) and `ldnmxx-hack/worker`
   (TS Cloudflare Worker) independently converged on "workflow = id + ordered named stages
   defined out-of-code" (YAML vs JSON). Hard language boundary → unify the **definition
   schema**, not the runtime. Relates to `azure-doc-workflows#68` / plan 018.

## Repo + role map

| Local path | GitHub | Role |
| --- | --- | --- |
| `/workspaces/qte77/qte77` | `qte77/qte77` | Estate hub; brand SSOT (`brand/DESIGN.md`); publishes `@qte77/ui-theme` from `brand/ui-kit` |
| `/workspaces/qte77/a2ui-agui-kit` | `qte77/a2ui-agui-kit` | NEW. `@qte77/a2ui-agui-kit` shared bridge (core + React + styles). I own it — clean squash-merges |
| `/workspaces/qte77/protocols` | `qte77/protocols` | NEW. `workflow-definition/v1` JSON Schema + fixtures. Clean squash-merges |
| `/workspaces/qte77/agenthud-agui-a2ui` | `qte77/agenthud-agui-a2ui` | Canonical UI base (superset). Consumer (Phase 4). `required_signatures` → admin merge |
| `/workspaces/qte77/ldnmxx-hack` | `qte77/ldnmxx-hack` | Fork "groundwork" + TS worker. Consumer (Phase 5 ui, Phase 8 worker). Admin merge |
| `/workspaces/qte77/claude-azure-workflows-gui` | `qte77/azure-doc-workflows` | Python doc-workflows engine. Consumer (Phase 7). Admin merge |

Estate conventions (apply everywhere): prefix all git/gh with `env -u GH_TOKEN -u GITHUB_TOKEN`;
identity `qte77 <93844790+qte77@users.noreply.github.com>`; commits `--no-gpg-sign`; conventional
commits; branch per topic; squash-merge on green CI then prune remote+local; plain-text docs, no
emoji/glyphs. The three consumer repos enforce `required_signatures` → their PRs need a per-PR
`--admin` merge (unsigned commits are the estate norm; only the signature gate is bypassed, never
a failing/absent check).

## DONE and published (do not redo)

| Artifact | Version / tag | PR | Notes |
| --- | --- | --- | --- |
| `@qte77/ui-theme` | 0.1.0 → **0.2.0** | qte77/qte77 #149, #150 | Tailwind tokens generated from `brand/DESIGN.md`; 0.2.0 adds `--shadow-card` |
| `@qte77/a2ui-agui-kit` | 0.1.0 → 0.2.0 → **0.3.0** | a2ui-agui-kit #1, #2, #3 | core (#1) → React (#2) → functional-depth styles (#3) |
| `qte77/protocols` `workflow-definition` | tag **`workflow-definition/v1.0.0`** | protocols #1 | schema + 4 valid + 4 invalid fixtures + dual-validator CI |

Published to **GitHub Packages** (npm registry `https://npm.pkg.github.com`, scope `@qte77`).

### Effects history (important context)

An early "flat design" instruction was **misread** as "make it flat"; it meant "don't lose the
effects". Corrected 2026-07-11 (qte77/qte77 #150 + a2ui-agui-kit #3, `Closes #148`): the brand now
sanctions subtle **functional depth** — a warm zero-blue `--shadow-card` elevation + a loading
shimmer, each `prefers-reduced-motion`-guarded; decorative gloss stays discouraged; the
generating chip stays non-pill. `brand/DESIGN.md` "Motion & effects" documents this with examples.
**So the consumer migrations PRESERVE the shadow + shimmer** — the only intended visual delta is the
generating chip un-pilling (`999px` → `var(--radius-md)`).

## Source map — what the packages contain and where it came from

### `@qte77/a2ui-agui-kit` (v0.3.0) exports: `.`, `./react`, `./styles.css`

| Package file | Extracted from |
| --- | --- |
| `src/contract.ts` | agenthud `ui/src/agent/contract.ts` (the SUPERSET — `DataModelUpdateMessageSchema`, `TreeChoiceSchema.action`) |
| `src/applyA2UIEvent.ts` | agenthud `ui/src/agent/applyA2UIEvent.ts` (render-injection seam; unknown events pass through as log entries) |
| `src/events.ts` | AG-UI event vocab + `EventLogEntry`/`AgentEvent`/`appendLogEntry` (single-sourced here) |
| `src/guard.ts` | ldnmxx `shared/guard.ts` (`detectInjection` + PATTERNS) |
| `src/renderTool.ts` | ldnmxx `shared/renderTool.ts` (dep-free `RENDER_UI_TOOL` + `isSelfContainedBatch`; card builders left behind) |
| `src/providers.ts` | ldnmxx `worker/src/agent/{providers,model}.ts` — runtime-agnostic subset only: `Provider`/`ToolSpec`/`CallArgs`/`ToolCallResult`/`runChain`. Cloudflare/OpenRouter/fetch specifics DROPPED |
| `src/prompt.ts` | agenthud `ui/src/agent/prompts.ts` SYSTEM_PROMPT (superset) + ldnmxx `shared/prompt.ts` A2UI rules (subset) → `buildSystemPrompt(options)` |
| `src/react/a2uiTheme.ts` | agenthud `ui/src/theme/a2uiTheme.ts` |
| `src/react/A2UISurface.tsx` | agenthud `ui/src/A2UISurface.tsx` — decoupled from its actionBridge singleton → takes an `onAction?: (name) => void` prop |
| `src/react/CatalogViewer.tsx` | agenthud `ui/src/CatalogViewer.tsx` |
| `src/react/EventStream.tsx` | agenthud `ui/src/EventStream.tsx` — gains optional `renderExtra?: (entry) => ReactNode` (so ldnmxx keeps its USAGE chip without forking) |
| `styles/a2ui.css` | agenthud `ui/src/index.css` — the `.a2ui-surface .qte-*` rules + motion/skeleton/busy; functional depth (`box-shadow: var(--shadow-card)`, gradient shimmer, non-pill chip) |

Toolchain: strict tsc (`exactOptionalPropertyTypes`), eslint (`typescript-eslint` + `sonarjs` +
`react-hooks`), vitest (node project for core, jsdom for react), stylelint (`color-no-hex` only —
functional depth allowed). CI: gitleaks + semgrep (`p/typescript --error`) + typecheck/lint/stylelint/
test/build + CodeQL + publish-on-version-bump. 46 tests. Peers: `zod`, and optional `react` /
`@a2ui/react` / `@qte77/ui-theme`.

### `@qte77/ui-theme` (v0.2.0)

`brand/ui-kit/tailwind/tokens.css` GENERATED from `brand/DESIGN.md` by `brand/scripts/gen_ui_kit.py`
(`--check` gates staleness; `make -C brand ui_kit` regenerates). Ships a Tailwind v4 `@theme` block:
`--color-*`, `--font-*`, `--radius-*`, `--shadow-card` (light) + dark scheme-swap blocks. DESIGN.md
front matter has the `elevation` block that produces `--shadow-card`. `eyerest.css` stays color-only
(no-build sites). Publish workflow: `.github/workflows/publish-ui-theme.yml`.

### `qte77/protocols` `workflow-definition/v1`

`schemas/workflow-definition/v1/workflow-definition.schema.json` (draft 2020-12). Envelope:
required `id` + non-empty ordered `stages[].name`; engine-specific keys documented in `$defs` and
allowed (`additionalProperties: true`); `system` = string or `{lang: string}` (#167); `output` =
`oneOf` [python `{outputs, required_sections}` | ts `{render.mode}}`]. Fixtures under
`fixtures/workflow-definition/v1/{valid,invalid}/`. Vendor into a consumer with `scripts/sync.sh`
(curls a pinned tag over public raw URLs — no token). CI validates every fixture with BOTH `ajv`
and `check-jsonschema`.

## REMAINING — consumer wave (Phases 4/5/7/8)

All on `experiment/*` **test branches** (may-not-merge). PRs open for validation; **merge waits for
the user** (protected repos). Consume `@qte77/ui-theme@^0.2.0` + `@qte77/a2ui-agui-kit@^0.3.0`
(effects preserved). Suggested order: **7 + 8 first** (tokenless, test-first), then **4 + 5** (need
`NPM_READ_TOKEN` for green CI). Phases 5 and 8 share the `ldnmxx-hack` clone → run sequentially there.

### TDD framing (honest, per "modules not scripts")

- **P7 (azure) + P8 (ldnmxx worker) = genuinely test-first.** Contract-conformance is load-bearing:
  write the failing tests FIRST — every shipped config validates against the vendored schema, every
  `invalid/*` fixture is rejected — then wire the fixture-sync + validator dep to green. FIRST RED
  RISK: confirm ALL shipped configs actually validate (schema is envelope-permissive, so they
  should).
- **P4 (agenthud) + P5 (ldnmxx ui) = mostly mechanical** (delete duplicated modules/CSS, repoint
  imports) — verified by typecheck/lint/test/build + a render/E2E smoke, NOT new unit tests. Each
  adds ONE new behavior test only. Ported tests are DELETED (the package owns them) — never
  duplicated.

### Phase 4 — agenthud (`experiment/adopt-shared-packages`)

- DELETE: `ui/src/agent/{contract,applyA2UIEvent}.ts`, `ui/src/theme/a2uiTheme.ts`,
  `ui/src/{A2UISurface,CatalogViewer,EventStream}.tsx`; the `@theme` token block in `ui/src/index.css`
  (→ `@import "@qte77/ui-theme/tailwind/tokens.css"`); the `.a2ui-surface .qte-*` + motion/skeleton/
  busy CSS in `ui/src/index.css` (→ `@import "@qte77/a2ui-agui-kit/styles.css"`). KEEP app-specific
  CSS (brand-mark, gh-icon, `#theme-toggle`, `.sr-only`).
- KEEP local: `ui/src/agent/{liveAgent,useLiveAgent,actionBridge,assets,prompts,conversation,transcript,fallback}.ts`, `recordings/`, `DashboardShell`, Demo/Live dashboards.
- MODIFY: `ui/package.json` (+ `@qte77/ui-theme@^0.2.0`, `@qte77/a2ui-agui-kit@^0.3.0`); import sites
  (`useLiveAgent.ts`, `liveAgent.ts`, `LiveDashboard.tsx`, `Transcript.tsx`; `prompts.ts` shrinks);
  wire `A2UISurface`'s `onAction` to the actionBridge; NEW `ui/.npmrc`.
- Adopt `detectInjection` browser-side at the composer submit seam. NEW behavior test: flagged input
  → refusal/stub path.
- Docs: CHANGELOG; `docs/plans|handoffs/015` pair; `docs/README` index; `.github/CONTRIBUTING.md`
  (.npmrc/token); AGENTS.md pointer. Separate tiny branch (out of scope here): fix
  `worker/README.md:61` keyless "Deferred" → shipped + document TURNSTILE_SECRET/OPENROUTER_KEY/
  OPENROUTER_FREE_MODELS.
- Issues: PR `Closes #211`; comment #165 (BYOK model list now in the pkg).
- Gate: full CI green (needs `NPM_READ_TOKEN`). PR/CHANGELOG note: effects preserved, only the chip
  un-pills.

### Phase 5 — ldnmxx UI (`experiment/adopt-shared-packages`)

- DELETE: `ui/src/agent/{applyA2UIEvent,contract}.ts`, `ui/src/theme/a2uiTheme.ts`,
  `shared/guard.ts`, the tool schema + `isSelfContainedBatch` from `shared/renderTool.ts` (card
  builders stay); the `@theme` block in `ui/src/index.css`.
- KEEP local: `shared/{prompt,incorporate,assessTool,searchTool}.ts` (grant-domain), `useAgentSSE.ts`,
  the USAGE chip (now rendered via `EventStream`'s `renderExtra`).
- MODIFY: `ui/package.json`, `worker/src/worker.ts` (import `detectInjection` from the package),
  `.npmrc` in `ui/` + `worker/`.
- NEW behavior test: USAGE chip renders via `renderExtra` (`ui/tests/`).
- Docs: CHANGELOG; `docs/plans|handoffs/009` pair; `docs/design.md` (theme now from `@qte77/ui-theme`,
  DESIGN.md still SSOT); `docs/architecture.md`; AGENTS.md "Reuse" line. Open small issue "worker/
  lacks eslint config". Comment #5.
- Gate: gitleaks + semgrep + ui lint/typecheck/test/build + worker typecheck/test green.

### Phase 7 — azure adopts contract (`experiment/workflow-definition-contract`)

- NEW `tests/contract/test_workflow_schema.py` + vendored fixtures (make target running
  `protocols/scripts/sync.sh` at tag `workflow-definition/v1.0.0`); dev-dep `jsonschema` (or
  `check-jsonschema`). `src/doc_workflows/models/config.py` gets `model_config =
  ConfigDict(extra="forbid")` ONLY if all `workflows/*.yaml` stay green, else defer to #26 WS3.
- TDD (red first): every shipped `workflows/*.yaml` validates against the vendored schema; every
  valid fixture parses via `Workflow.model_validate`; invalid fixtures rejected; round-trip
  `from_yaml(...).model_dump()` re-validates. Do NOT touch `core/runner.py` (plan 018's job).
- Docs: **scriv fragment** in `changelog.d/` (required pre-merge; not a direct CHANGELOG edit);
  `docs/plans|handoffs/019` pair (note the no-typechecker gap); MADR ADR beside
  `docs/decisions/0004-workflow-runtime.md`; CONTRIBUTING fixture-sync command. Passing fix: add
  `DOC_WF_REQUIRE_PRINCIPAL_HEADER` + `DOC_WF_MAX_UPLOAD_FILES` (`core/settings.py:53-56`) to the
  CONTRIBUTING config table + `.env.example`.
- Issues: comment #68 (schema-only, does NOT block plan 018) / #26 WS3 / #167.
- Gate: ruff E/F/I/S + format + pytest + pip-audit green.

### Phase 8 — ldnmxx worker adopts contract (`experiment/workflow-definition-contract`)

- `usecases/*.json`: rename `span` → `name`. `worker/src/usecases.ts`: `StageDef.span` → `name`,
  align `assertUsecaseDef` with the schema core (keep the assert-guard style — bundle-size-sensitive,
  trusted build-time JSON; no zod). `worker/src/worker.ts`: span refs. Vendored
  `worker/test/fixtures/contract/`.
- TDD (red first, `worker/test/usecases.contract.test.ts`): every `usecases/*.json` validates against
  the schema (ajv devDep, test-only); invalid fixtures rejected by `assertUsecaseDef`; the rename is
  covered by existing usecase tests going red-then-green.
- Docs: CHANGELOG; `usecases/README.md` + `docs/usecase-workflows.md` rewritten against the contract
  (document USAGE as a B-local SSE extension); `docs/plans|handoffs/010` pair.
- Gate: worker typecheck/test + gitleaks/semgrep green; demo smoke `/run?usecase=founders-copilot`.

## Token constraint (Phases 4/5 only)

Installing the packages from GitHub Packages needs auth even for public packages. Local verification
is **tokenless via tarballs**: `npm pack` each package, then in the consumer
`npm install <tgz> --no-save` (package.json still declares the published `^` versions) and run the
gate. For the draft PR's own CI to go green, each consumer repo needs an `NPM_READ_TOKEN`
(`read:packages` PAT) secret — user action; until then P4/P5 CI is red at install (expected on a test
branch). Phases 7/8 are tokenless.

## Verification (per phase)

1. P4: agenthud `npm run typecheck && lint && test && build` green; replay demo + live BYOK smoke;
   bundle diff sane; render shows shadow + shimmer (effects preserved), chip non-pill.
2. P5: ldnmxx `make test` green; `/run?usecase=founders-copilot` renders cards + USAGE chip.
3. P7/P8: `pytest tests/contract` green in azure; `vitest worker/test/usecases.contract.test.ts`
   green in ldnmxx — the SAME contract passing in both languages.

## Risks

| Risk | Mitigation |
| --- | --- |
| `@a2ui/react` pre-1.0 drift breaks both consumers | Peer range `>=0.10.1 <0.11`; upgrade via one a2ui-agui-kit PR first |
| GitHub Packages token friction (P4/P5) | `.npmrc.example` + CONTRIBUTING recipe; `NPM_READ_TOKEN` PAT; tokenless local verify via tarballs; can mirror to npmjs later |
| Schema breaks azure YAML / fights plan 018 | Envelope-permissive schema; "every shipped YAML validates" red test; strictness deferred to #26 WS3; never touch `runner.py` |
| ldnmxx may freeze post-hackathon | Its phases are self-contained; plan docs carry the exact diff |
