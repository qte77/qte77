---
plan: ../plans/001-estate-ui-engine-unification.md
status: shared artifacts DONE; consumer wave (P4/5/7/8) REMAINING
updated: 2026-07-11
---

# Handoff — Estate UI + workflow-definition unification

Onboarding for the next session. Full detail + source map:
[plan 001](../plans/001-estate-ui-engine-unification.md). Read this first, then the plan's
"Source map" and "REMAINING" sections — you should not need to re-explore the repos.

## Where things stand

**Done and published** (7 PRs merged, nothing pending on your side):

- `@qte77/ui-theme` **0.2.0** (Tailwind tokens from `brand/DESIGN.md`, incl. `--shadow-card`)
- `@qte77/a2ui-agui-kit` **0.3.0** (core + `./react` + `./styles.css`, functional depth)
- `qte77/protocols` `workflow-definition` tag **`v1.0.0`**

**Remaining** = the consumer wave: make the four consumer repos use the shared artifacts.

- **P7** azure-doc-workflows adopts the workflow schema (pytest, test-first)
- **P8** ldnmxx worker adopts it (`span`→`name`, vitest, test-first)
- **P4** agenthud consumes the UI packages (`Closes #211`)
- **P5** ldnmxx ui consumes the UI packages

## How to handle it

1. **Order**: do **P7 + P8 first** — they are tokenless (schema vendored over public `curl` via
   `protocols/scripts/sync.sh`) and reach green CI now. Then **P4 + P5** (need the token, see below).
   P5 and P8 both edit the `ldnmxx-hack` clone → run them sequentially, not in parallel.
2. **Test branches**: everything goes on `experiment/*` branches (estate's may-not-merge prefix).
   Open the PR for validation, but **do not merge** — the three consumer repos enforce
   `required_signatures`, so each merge is the user's per-PR `--admin` decision.
3. **Effects are preserved**: consumers pull `@qte77/ui-theme@^0.2.0` + `@qte77/a2ui-agui-kit@^0.3.0`,
   so the card shadow + skeleton shimmer STAY. The only intended visual change is the generating
   chip un-pilling (`999px` → `var(--radius-md)`). Say so in each PR/CHANGELOG; it is not a bug.
4. **TDD**: P7/P8 are genuinely test-first (write the contract-validation tests red, then wire the
   fixture sync + validator dep green). P4/P5 are mechanical (delete duplicated modules, repoint
   imports) verified by build/test/render — each adds only ONE new behavior test (P4 = browser-side
   `detectInjection` at the composer seam; P5 = USAGE chip via `EventStream` `renderExtra`). Delete
   ported tests; never duplicate. Strict lint/typing/sec always.
5. **Delegate content edits** to a subagent working inside each target repo (cross-repo hygiene);
   the main agent does git plumbing (branch/commit/PR). Subagents write files + verify; do not let
   them run git.

## Token constraint (P4/P5 only)

Installing the packages from GitHub Packages needs auth even for public packages. Verify **locally,
tokenless**: `npm pack` each package to a tarball, then in the consumer `npm install <tgz> --no-save`
(keep the published `^` versions in `package.json`) and run the gate. For the draft PR's CI to go
green, the user must add an `NPM_READ_TOKEN` (`read:packages` PAT) secret to `agenthud-agui-a2ui`
and `ldnmxx-hack`. Until then P4/P5 CI is red at install — expected on a test branch.

## First actions on resume

- Reset the stale, empty `experiment/adopt-shared-packages` branch in `agenthud-agui-a2ui`
  (`git checkout main`; delete the branch) before starting P4.
- Start P7: branch `experiment/workflow-definition-contract` off `claude-azure-workflows-gui` main;
  vendor the schema+fixtures via `sync.sh` at tag `workflow-definition/v1.0.0`; write the contract
  tests red; then green.

## Gotchas

- Prefix every git/gh with `env -u GH_TOKEN -u GITHUB_TOKEN` (both vars are invalid and shadow the
  real credential → 403 on writes).
- Commit `--no-gpg-sign`; identity `qte77 <93844790+qte77@users.noreply.github.com>`.
- `--admin` merges bypass ONLY the signature gate, never a failing/absent status check. The auto-mode
  classifier will prompt the user per-PR (the standing allow was intentionally removed).
- Plain-text docs — no emoji/checkmarks/glyphs.
- azure has no typechecker in CI — flag, don't fix.
- Local ephemeral copy of this plan (pre-commit): `~/.claude/plans/tingly-orbiting-scroll.md`. Memory:
  `project_ui_engine_unification.md`.
