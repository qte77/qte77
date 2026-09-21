---
plan: ../plans/003-unattended-run-kit.md
status: in progress — Phase A authored + uncommitted; owner review is the next gate
updated: 2026-07-24
---

# Handoff — Unattended-run kit

Onboarding for the next session. Full detail + source map:
[plan 003](../plans/003-unattended-run-kit.md). Read the plan first. Tracking issue: <open one; link here>.

## State at handoff (2026-07-24)

- **Branch / sync:** authored on the working tree, **uncommitted**. No git operations were run (merge is
  an owner gate; the authoring agent does not commit/push/merge).
- **Shipped this arc:** nothing merged yet — Phase A is the authored contract, pending owner review.
- **Resume point:** owner reviews the diff (Phase B), then the two wiring edits land + arc is committed.
- **Owner action that unblocks the rest:** approve + commit this arc; decide rollout scope (Phase C).

## What was authored (Phase A)

The contract-only kit, all project-name-clean:

- `.claude/rules/unattended-execution.md` — always-loaded constraints.
- `docs/unattended-execution.md` — the depth contract (rationale + mechanism spec + the unattended tax).
- `docs/templates/plan.template.md`, `handoff.template.md`, `settings.unattended.jsonc` — copyables.
- `AGENT_LEARNINGS.md` — one linking entry (footguns live in the rule, not duplicated).

## How to handle it (order)

1. **Owner review the diff.** This is the kit's own owner gate — do not auto-merge.
2. **Land the two wiring edits** (still pending): a README `## Refs` line and a
   `docs/project-workflows.md` decision-flow pointer to the guide. Both are additive, single-line.
3. **Commit per owner's chosen style** (`docs(003): add unattended-run kit`). If the repo enforces
   `required_signatures`, per-PR `--admin` bypasses ONLY the signature gate.
4. **Phase C rollout** (agent-runnable after commit): backfill the rule + settings snippet into
   hands-off-capable repos (targets on the issue, not named here); point the `workspace-setup`-class
   skill at this contract; apply the full kit to the next build's first arc.

## Working style

- Docs arc: the gate is `markdownlint` + lychee link-check, not a code gate. These files are
  **asterisk-emphasis** (MD049 is per-file) and **hyphen bullets** (MD004 is per-file) — match them.
- **Before commit, grep the kit files for the private-repo name set** — the built-in-the-open guarantee.
- Merge stays an owner gate; the agent parks the green PR, never auto squash-merges.

## Gotchas

- Prefix every `git`/`gh` with `env -u GH_TOKEN -u GITHUB_TOKEN`; commit `--no-gpg-sign` and `-F` (not
  `-m`). Full list: [unattended tax](../unattended-execution.md#the-unattended-tax).
- The kit is **contract-only** — resist adding runnable `ui_sweep.py` / `workflow.js` here; that belongs
  downstream per the META -> MECHANISM split. If tempted, it is a new engine/plugin arc, not this one.
- `settings.unattended.jsonc` is a **template with comments** — settings.json is strict JSON; strip the
  comments when merging into a real repo.
