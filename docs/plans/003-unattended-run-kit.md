---
status: in progress — Phase A authored, uncommitted, pending owner review
phase: Phase A (author the contract) done; Phase B (owner review + commit) next
handoff: ../handoffs/003-unattended-run-kit.md
updated: 2026-07-29
---

# Unattended-run kit — the estate contract for hands-off e2e sessions

Codify, once, the contract for **long-running e2e hands-off unattended Claude Code sessions**, distilled
from learnings across prior runs, tasks, and projects in the estate. Contract-only: this repo owns the
rule, guide, templates, and learnings; the runnable mechanism is derived downstream per the
META -> MECHANISM split ([`doc-structure.md`](../doc-structure.md)). Onboarding + loop:
[handoff 003](../handoffs/003-unattended-run-kit.md).

## Why

Run agents hands-off across many repos and each one re-derives the same 80% — the phase shape, the
plan/handoff source map, the verify-on-live-target loop — and re-learns the same footguns (auth 403,
deploy/edge-cache race, session-death data loss, injection blast radius from a broad Bash allowlist).
Several prior projects independently converged on the same architecture, each strongest in a different
dimension. This arc captures the best-of-breed union so a new repo inherits the whole stack instead of
rebuilding it. This is the same generalize-once move the estate already makes for docs and UI.

## Owner decisions (locked, 2026-07-24)

1. **Contract-only in this repo.** Rule + guide + templates + learnings land here; no runnable
   mechanism (sweep / workflow / monitor) is embedded — it is specified and pointed downstream.
2. **Tracked as a numbered arc** (this pair, `003`).
3. **Merge is an owner gate.** The kit prescribes park-for-approval, never agent auto squash-merge. The
   agent that authored this arc does NOT commit, push, or merge — the owner reviews the diff and decides.
4. **No private project names** in any kit artifact (this repo is built in the open) — learnings are
   framed as "prior runs / tasks / projects".

## Source map — what this arc adds (authored 2026-07-24)

| File | Content | Status |
| --- | --- | --- |
| `.claude/rules/unattended-execution.md` | Always-loaded constraints: phase shape, gates, verification, the unattended tax as hard rules | authored, uncommitted |
| `docs/unattended-execution.md` | Depth contract: rationale, phase shape, quality gates, verification loop, context economy, tax table, mechanism spec + downstream pointers | authored, uncommitted |
| `docs/templates/plan.template.md` | Plan skeleton: source map, decide-by-default, phase plan, done-whens, owner-gates, verification | authored, uncommitted |
| `docs/templates/handoff.template.md` | Handoff skeleton: state, order, working style, owner-gates, gotchas | authored, uncommitted |
| `docs/templates/settings.unattended.jsonc` | Harness config: `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` + `SessionStart:compact` re-onboard hook | authored, uncommitted |
| `AGENT_LEARNINGS.md` | One entry linking the codified contract (no footgun duplication — DRY into the rule) | authored, uncommitted |
| `README.md`, `docs/project-workflows.md` | Refs/pointer wiring to the new contract | authored, uncommitted |
| `CHANGELOG.md` | `### Added` entry (Unreleased) for the kit | authored, uncommitted |

## Phase plan (non-blocked A/B/C)

- **Phase A — agent-only (done this session).** Author every artifact above. No git operations.
- **Phase B — one owner sitting.** Owner reviews the diff; decides commit style and merge (the kit's own
  owner gate); approves the two wiring edits (README Refs, project-workflows pointer). Pre-staged: all
  files written, wiring diffs described below.
- **Phase C — rollout (future, agent-runnable once B lands).**
  1. Backfill the rule + settings snippet into estate repos that run hands-off but lack them (targets
     tracked in the arc issue, not named here). Per-repo session or subagent-inside-target-repo; the
     main agent does git plumbing only.
  2. **Mechanize downstream in `claude-code-plugins`** — the survey found strong context/session
     mechanism (`cc-meta`) + a scaffolder (`workspace-setup`) already exist, but the unattended-specific
     mechanism is missing. Build the gap list in
     [`../unattended-execution.md`](../unattended-execution.md#mechanism-derived-downstream): (a) add
     the `unattended-execution` rule + templates + autocompact settings to `workspace-setup`'s deployed
     set (highest leverage; must carry the core-principles reconciliation); (b) a browser-sweep skill +
     run manifest; (c) auto-firing `PreCompact`/`SessionEnd` archiving in `cc-meta`; (d) plan+handoff
     pairing + arc-closure audit; (e) a `git -> gate -> PR -> park` loop skill.
  3. Apply the full kit to the next greenfield-for-unattended build as its first arc.

## Backlog (done-when each)

- [x] Author rule + guide + 3 templates + learnings entry — *done-when:* files exist, project-name-clean.
- [x] Wire README Refs + `project-workflows.md` decision-flow pointer + CHANGELOG entry — *done-when:* all link/record the kit.
- [ ] Owner review + commit/merge decision — *done-when:* owner approves; arc committed per owner style.
- [ ] Rollout backfill (Phase C) — *done-when:* each targeted repo loads the rule; tracked on the issue.

## Owner-gates (the only blockers)

- **Commit / merge** of this arc — owner reviews the diff and decides (agent will not merge).
- **Rollout scope** — which repos get backfilled, and in what order (decide-by-default: all
  hands-off-capable repos, highest-traffic first).

## Verification

Docs arc, so the gate is docs-lint, not a code gate: `markdownlint` (mind MD049 per-file emphasis — these
files are asterisk-emphasis; MD004 per-file bullets — hyphen) + lychee link-check must pass. Confirm no
private project name leaks: grep the kit files for the private-repo set before commit.

## Open questions

- **Autocompact threshold value** — ship the template default at `50` (current) or bump to `~65-70`?
  Prior-run evidence says 50 is aggressive (fires often, risks mid-task) and 65-70 gives more runway.
  Decide-by-default: keep `50` in the template as the estate norm, note the tradeoff, tune per repo.
- Does merge policy stay an owner gate estate-wide, or is auto squash-merge-on-green retained for
  low-risk repos? (current kit default: owner gate everywhere; owner confirms.)

Resolved (2026-07-24): the kit now includes a `PreCompact` archive hook (highest-ROI compaction change)
and names subagent-first discovery as the biggest context lever — see the settings template + guide.

Resolved (2026-07-29): split the force-push footgun after dogfooding exposed it as too blunt — a
downstream scaffold subagent force-pushed its OWN unmerged draft branch (safe) but our rule listed
force-push as universally escalate-only, so it read as a violation. Rule + guide now scope escalation to
**shared/protected** branches; force-push of an own unmerged feature branch with `--force-with-lease` is
routine (aligns with the existing `CONTRIBUTING.template.md` line).

## Refs

- Contract: [`../unattended-execution.md`](../unattended-execution.md);
  rule [`../../.claude/rules/unattended-execution.md`](../../.claude/rules/unattended-execution.md).
- Related rules: `context-management.md`, `compound-learning.md`, `core-principles.md`.
- Related arcs: this repo's `plans/001` (source-map shape precedent).
