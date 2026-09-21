---
plan: ../plans/004-productization-research.md
status: not started — Stage 0 (plan) written, research fan-out not yet launched
updated: 2026-08-03
---

# Handoff — Productization research (market, competition, ICP, USP)

Onboarding for the next session. Full detail + `file:line` source map:
[plan 004](../plans/004-productization-research.md). **Read the plan's source map first — you should
not need to re-explore the orchestrators or the goal rails.** Tracking issue: none yet (owner-gated,
backlog #9).

## State at handoff (2026-08-03)

- **Branch / sync:** `main`, dirty — arc 003 files still uncommitted (`.claude/rules/unattended-execution.md`,
  `docs/unattended-execution.md`, `docs/templates/*`, `docs/{plans,handoffs}/003-*`) plus this 004 pair.
  Nothing pushed for this arc.
- **Prod:** n/a — docs/research arc, no deploy surface.
- **Shipped this arc:** nothing yet. Stage 0 (this plan + handoff) is the only artifact.
- **Resume point:** launch the Phase A research fan-out (plan backlog #1–#4) as a dynamic workflow.
- **Owner action that unblocks the rest:** none blocks Phase A. The first hard gate is #11 (BRD
  go/no-go + outreach authorization) after the BRD lands.

## The one thing to understand before doing anything

`docs/operating-model.md` ran a **commercial** adversarial distillation in 2026-06 and almost
everything fell (`:69-77`). It then **voided** the moat/TAM/"reinventable" cuts on the explicit
grounds that the estate is a *showcase, not a product* (`:88-90`). **This arc reverses that voiding.**

Consequences you must not lose:

1. The **only** commercially-surviving artifact was the narrow *eval-before-work forcing function*
   (`:60-65`) — **not** the traceability spine, which is an explicit `DISCARD` at `:71`. Scope P2 to
   the forcing function; do not quietly re-inflate it to the full spine.
2. That survivor is rated "incentive barrier, **thin**, ~12–18 months" from 2026-06-28. The window is
   the urgency argument *and* the biggest risk. State it dated, never vague.
3. `goals.json:6` is **empty**. The eval-gate has run zero closed KR cycles against a required ≥3
   (`:127-136`). The BRD may argue the opportunity; it may **not** claim proven traction.

## How to handle the plan (order)

1. **Run Phase A research first** (backlog #1–#4) — comparables, ICP/JTBD, competitive matrix, then
   the adversarial verify. Do **not** start writing the BRD before the verify pass completes;
   an unsourced BRD is worse than none.
2. **Then #5** — re-run the `operating-model.md:69-77` "What fell" table under the commercial frame,
   using the research evidence. This is the arc's intellectual core; everything downstream depends on
   whether those rows still fall.
3. **Then #6–#8** — positioning, pricing, BRD. Single-threaded in the main session; synthesis needs
   one coherent voice and does not parallelize.
4. **Then #9–#10** — pre-stage the tracking issue, `goals.json` entries, and interview guide, so the
   owner checkpoint is an approval, not a work session.
5. **Park at #11.** Do NOT open issues, commit `goals.json`, or contact anyone before the owner sitting.
6. **Phase C (#12–#14)** only after go.

**Do NOT start with the PRD/FRD.** Writing requirements before the market research is exactly the
yak-shave `operating-model.md:79-80` names as the single most likely failure mode ("the cure is the
disease").

## First actions on resume

- `git checkout -b docs/004-productization-research`
- Launch the research workflow: three lanes (comparables ×7, ICP/JTBD ×4, category+competition ×2),
  each agent returning a fixed schema with a mandatory `sources: []` field; then an adversarial verify
  stage that drops any claim without a source URL. Target 12–15 agents (medium size guideline).
- Write findings to `docs/plans/004-productization-research-findings.md` — **structured findings only,
  never raw search dumps** (`.claude/rules/context-management.md`).

## Working style

- **Sources or it did not happen.** Every market/pricing/ICP claim carries a URL or moves to an
  explicit assumptions list. Incorrect info is the worst degradation mode; market research is where
  models confabulate most. This replaces "RED first" as this arc's quality gate — there is no code.
- **Assert nothing about the named companies from priors** — especially monaco.com, whose GTM
  archetype is unverified.
- **Docs gate before pushing:** `markdownlint $(git ls-files '*.md')` and `lychee $(git ls-files '*.md')`,
  whole, not à la carte. Gate the lint with `if … then … else exit 1`, never `set -e`
  (`AGENT_LEARNINGS.md` — `set -e` did not abort here and shipped violating commits twice).
- **Match the target file's emphasis char** before editing (MD049 is per-file).
- **Merge is an owner gate** — park the green PR; never auto squash-merge.

## Owner-gates (pre-staged; batch into one sitting)

| Gate | Pre-staged in Phase A | Owner flips |
| --- | --- | --- |
| Tracking issue | Issue body drafted | `gh issue create` approval |
| BRD go/no-go | BRD + kill-criteria | Proceed to PRD/FRD, or kill |
| Customer-discovery outreach | 8–12 question interview guide | Authorize contacting real people |
| `goals.json` commit | Goal/KR JSON written, uncommitted | Approve — goals are human-authored (`CLAUDE.md` task-tracking authority) |

## Gotchas (the unattended tax + arc-specific traps)

- Prefix every `git`/`gh` with `env -u GH_TOKEN -u GITHUB_TOKEN`; commit `--no-gpg-sign` and `-F <file>`
  (never `-m` — backticks/`$()` get shell-substituted). Full list:
  [unattended tax](../unattended-execution.md).
- **Cross-repo:** the orchestrators are sibling repos. Do **not** `Read` their files from a qte77
  session for content work — the implicit `CLAUDE.md` cascade fires on `Read`. The plan's source map
  already carries what you need; if more is required, delegate to a subagent inside the target repo.
- **Do not create a second tracking system.** BRD/PRD/FRD plugs into the existing rails at
  `docs/goals.md:41-55` step 1. GitHub Issues stay the SOT; `contributions.json` and the tracker are
  derived (`CLAUDE.md` task-tracking authority).
- **`AGENT_LEARNINGS.md` has a stale-by-frame entry** — "Calibrate adversarial / moat red-teams to the
  actual purpose" says moat cuts are void because this is a showcase. Backlog #14 amends it. Until
  then, a future session reading that entry will wrongly discard the commercial cuts again.
- **Findings + this arc's scaffolding are ephemeral.** Do not let `004-*-findings.md` become a
  permanent doc.

## At arc close (mine, then prune)

This handoff, its plan, the findings, and the arc's memory are **ephemeral working state**. When the
arc ships: **mine** them — the frame-flip learning into `AGENT_LEARNINGS.md`, the re-armed verdict into
`docs/operating-model.md`, the BRD/PRD/FRD into durable product docs (or delete them if the go/no-go is
"no") — migrate any remainder to `005`, then **prune** this scaffolding.
