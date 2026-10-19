---
status: proposed — not started
phase: <which phase is the recommended first build>
updated: YYYY-MM-DD
---

# <Title — what this arc delivers>

<One paragraph: the change, and that this doc is the source map so a fresh session executes without
re-exploring. The status below is the onboarding — read it first.>

> Delete this callout before use. This template instantiates the estate
> [unattended-execution contract](../unattended-execution.md). One file per arc — no separate handoff
> file. Keep the `file:line` source map — it is what lets a cold or compacted session act without
> re-mapping. Match the repo's digit width for `NNN`.

## Status (as of YYYY-MM-DD)

<The plan's own onboarding — read this before anything else below. Update at every milestone.>

- **Shipped:** <merged PR numbers + one-liners, or "nothing yet">.
- **Next, in order:** <the ordered resume steps — what to build first and why; the literal first
  branch/commands/files to touch if resuming cold>.
- **The loop:** <RED-first TDD for modules; glue/config/rendering covered by build+lint+e2e; run the
  whole gate == CI before pushing; merge is an owner gate, never agent auto squash-merge>.
- **Owner-gates:** <each pre-staged gate + the single switch the owner flips — point at "Owner-gates"
  below for detail>.
- **Commands:** <the exact verification commands — point at "Verification" below>.
- **Watch-outs:** <inherited gotchas: the
  [unattended tax](../unattended-execution.md#the-unattended-tax) and arc-specific traps verified
  this session>.

## Why

<2-4 lines: incumbent state -> the gap -> what this arc changes. Link specs, do not inline them.>

## Repo + role map

<Only for cross-repo arcs; drop for single-repo. Local path | GitHub | Role. Restate estate git
conventions once: `env -u GH_TOKEN -u GITHUB_TOKEN`; `--no-gpg-sign`; branch per topic; merge is an
owner gate.>

## Owner decisions (locked, YYYY-MM-DD)

<Decisions already made — the agent does NOT re-litigate these. Each with a one-line rationale.>

## Decide-by-default (apply silently unless the owner overrides at the Phase B checkpoint)

<Every OPEN decision with its recommended default, so the run proceeds unattended.>

## Source map — touch without re-mapping (verified YYYY-MM-DD, file:line)

<The load-bearing section. One table per subsystem/repo.>

| File | Symbols / content | Role in this arc |
| --- | --- | --- |
| `path/to/file.py` | `func_name` (signature), line ~NN | what changes here |

## Phase plan (non-blocked A/B/C)

- **Phase A — agent-only.** <Front-loaded slices, in order. Split independent tails to run in parallel.
  Pre-stage every Phase B gate here (migration SQL PR'd-but-unapplied, scripts, dry-runs).>
- **Phase B — one owner sitting.** <Every gate, batched: migrations, DB mutations, secrets, spend,
  merge. Each item names the exact owner action + the pre-staged artifact that makes it an approval.>
- **Phase C — activation.** <Verify gated features, e2e local + remote, deploy + probe, report, close.>

## Backlog (each item states its done-when)

- [ ] **<Item>** — <what> — *done-when:* <the exact self-verification>. <MODULE (RED-first) or glue->e2e.>

## Owner-gates (the only things that block hands-off)

<Enumerate: migration apply, secret set, service-role/scoped-key mint, deploy, spend, merge. For each:
what is pre-staged, and the single switch the owner flips.>

## Verification

<The gate command (`make check` / `npm run validate` == CI, run whole) + the audit target. The e2e
sweep command (local AND remote), the console-error-fail expectation, expected pass counts as
regression sentinels, and the run-manifest path.>

## Open questions

<Genuinely unresolved — distinct from decide-by-default. Each with the trade-off.>

## Refs

<Tracking issue; related plans/ADRs; external blueprints. Links only.>
