---
title: Agent Learning Documentation
description: Non-obvious patterns that prevent repeated mistakes across sprints
---

## Template

- **Context**: When/where this applies
- **Problem**: What issue this solves
- **Solution**: Implementation approach
- **Example**: Working code
- **References**: Related files

## Learned Patterns

### Calibrate adversarial / moat red-teams to the actual purpose

- **Context**: Running `/adversarial-distillation` (or any moat / defensibility / "is this sellable" red-team) on **internal or personal** tooling.
- **Problem**: The method optimises for **commercial defensibility** — its "no moat", "reinventable → discard", "a hyperscaler will build it", "TAM too small" cuts are irrelevant off-commercial and will wrongly kill worth-building work.
- **Solution**: Split the verdict — **frame-dependent** cuts (moat / TAM / competition) → discard when not selling; **frame-independent** cuts (logic, ROI, rot, Goodhart, cold-start) → keep. Re-read through the real purpose first. "Showcase not sell" voids the moat cuts; the engineering/economics cuts survive.
- **References**: `docs/operating-model.md` (Calibration section).

### Persistence: commit-then-cache + scrape-then-compress (git is the only durable SOT)

- **Context**: Preserving session/agent knowledge across sessions in an agentic estate.
- **Problem**: `~/.claude/.../memory/` is **local container disk** — disk break / codespace delete / rebuild loses it. Nothing critical can live only there.
- **Solution**: Durable SOT = **git-committed + pushed** (repo docs, GitHub Issues, this file, `.claude/rules/`). Memory is a *regeneratable cache*. Periodically **scrape** the ephemeral layer for learnings and **compress** (distil, don't dump — compression is the anti-graveyard quality gate), then commit. Commit-as-you-go during a session + a backstop scrape.
- **References**: `qte77/qte77#94`.

### markdownlint MD049: emphasis style is per-file; gate it with `if`, not `set -e`

- **Context**: Editing Markdown docs in this estate and running `markdownlint` before commit.
- **Problem**: (1) MD049 enforces emphasis-style *consistency within each file* — `docs/operating-model.md` is all-underscore, `docs/cto-handbook-mapping.md` is all-asterisk; mixing styles fails. (2) `set -e; markdownlint …` did **not** abort on a non-zero exit here (shipped a violating commit twice in one session).
- **Solution**: Match the *target file's existing* emphasis char before editing. Gate explicitly — `if markdownlint "$f"; then …; else exit 1; fi` — never rely on `set -e` for the lint step.
- **References**: PR #147.

### Stuck `CodeFactor: ERROR` clears on a real update-to-main, not on nudge commits

- **Context**: A required `CodeFactor` status check shows `ERROR` (often null description / empty target URL) and blocks a PR merge — common when a head SHA's analysis got stuck (seen on docs-only PRs).
- **Problem**: Pushing empty "nudge CI" commits to force re-analysis does **not** clear it — the stuck SHA keeps its errored status — and it pollutes history. (Two nudge commits failed before the fix was found.)
- **Solution**: Bring the branch **up to date with `main`** (`gh pr update-branch <n>`, or a local `git merge origin/main`). The fresh, GitHub-signed SHA gets a clean CodeFactor re-analysis that goes green. Never nudge-commit.
- **References**: PRs #158 / #159.

### Unattended hands-off runs converge on one repeatable shape

- **Context**: Running long, e2e hands-off unattended sessions across estate repos. Learned from prior runs, tasks, and projects that each independently rebuilt the same scaffolding.
- **Problem**: Without a shared contract, every repo re-derives the same 80%: the non-blocked phase shape, the plan/handoff source map, the verify-on-live-target loop, and the same recurring footguns (bare `git`/`gh` 403, deploy/edge-cache race, session-death losing uncommitted work, broad Bash allowlist widening injection blast radius). Mistakes recur per-repo instead of being prevented once.
- **Solution**: The contract is now codified once as the always-loaded rule + depth guide + templates. Instantiate it per repo (rule + settings snippet), do NOT re-list the footguns inline (DRY — they live in the rule). Merge stays an owner gate, never agent auto squash-merge. The runnable mechanism (browser sweep, orchestration workflow, monitor) is derived downstream per the META -> MECHANISM split.
- **References**: [`.claude/rules/unattended-execution.md`](.claude/rules/unattended-execution.md), [`docs/unattended-execution.md`](docs/unattended-execution.md), `docs/templates/{plan,handoff}.template.md`, `docs/templates/settings.unattended.jsonc`.
