# Unattended execution

The estate contract for **long-running, e2e hands-off unattended sessions** with minimal supervision.
This is the depth companion to the always-loaded rule
[`.claude/rules/unattended-execution.md`](../.claude/rules/unattended-execution.md) — the rule is the
constraint, this page is the rationale, the mechanism spec, and the templates that instantiate it.

Distilled from **learnings across prior unattended runs, tasks, and projects** in the estate — several
independently converged on the same architecture, each strongest in a different dimension. This contract
is the best-of-breed union so a new repo inherits the whole stack instead of re-deriving most of it from
scratch.

Per the estate's META -> MECHANISM split ([`doc-structure.md`](doc-structure.md)), this page defines the
**contract**. The runnable **mechanism** (the browser sweep, the orchestration workflow, the monitor
workflow) is derived downstream — see [Mechanism](#mechanism-derived-downstream).

## What "unattended" means here

Automation of *coordination*, not elimination of the owner's sign-offs. A hands-off run does every
agent-runnable slice on its own, parks safely at each genuine gate, and reports the single switch the
owner must flip. Merge, deploy, DB mutations, secrets, and spend stay owner-gated by design — that is
what makes unattended merges acceptable, not a maturity gap.

## The non-blocked phase shape

Structure every arc as three phases so the owner is never in the critical path mid-run.

- **Phase A — agent-only.** Front-load every agent-runnable slice; never interleave an owner-gated item
  mid-sequence. Split by repo so independent tails (e.g. a data pipeline) run parallel to the main work.
  **Pre-stage every gate here**: migration SQL PR'd-but-unapplied, remediation scripts written, dry-run
  reports generated — so the gate is later an *approval*, not a work session.
- **Phase B — one owner sitting.** All gates batched into a single pre-staged checkpoint: migrations,
  DB mutations, secrets, spend, and **merge**. Because everything was pre-staged in A, this is minutes
  of approvals, not a build session.
- **Phase C — activation.** The agent resumes: verify the gated features now that data/secrets landed,
  run e2e, deploy, probe, write the progress report, close the arc.

Three cross-cutting rules make the phases run unattended:

- **Decide-by-default.** Every open decision carries a recommended default. The agent proceeds under the
  default; the owner overrides at the Phase B checkpoint. Record locked decisions in the plan so they
  are not re-litigated. **This overrides core-principles' "when in doubt, STOP, ask the user" for
  hands-off mode** — the always-loaded `core-principles.md` optimizes for an interactive session, so
  without this exception an unattended agent would block on the first ambiguity. The reconciliation:
  proceed under the safe default and *park* the decision for the owner; escalate mid-run only when a
  decision has **no safe default** or the action is **irreversible/destructive** (delete, DB mutation,
  spend, deploy, force-push to a shared/protected branch). Force-pushing your own unmerged feature
  branch (with `--force-with-lease`) is routine, not an escalation. Everything else waits at the Phase B
  checkpoint, not in a blocked run.
- **Done-when per item.** Each backlog item states its own verification, so the agent self-certifies and
  moves on without asking.
- **Build-behind-gate.** Ship data-dependent features dormant behind their gate; code never waits on
  data. The feature activates when the data lands in Phase C.

## Plan + handoff artifacts

The single highest-ROI practice: a paired plan + handoff per arc that collapses per-session
re-onboarding to near zero.

- **Pairing.** `docs/plans/NNN-slug.md` + `docs/handoffs/NNN-slug.md`, same number, kebab slug. Match
  the repo's existing digit width (this repo uses 3-digit `NNN`; some estate repos use 4-digit).
  Findings reuse the number with a `-findings` suffix.
- **The plan carries a `file:line` source map** — a "touch without re-mapping" table of exact files,
  symbols, and line refs for every change, marked session-verified with a date. This is what lets a
  cold or compacted session act without re-exploring. See an existing plan under [`plans/`](plans/) for
  the canonical shape.
- **The handoff onboards the next session**: dated state (branch, prod version, shipped PRs), the
  ordered next steps with done-whens, the loop, owner-gates, exact commands, and inherited gotchas.
  Read the handoff first, the plan second.
- **Keep plan + handoff + `MEMORY.md` in sync at every milestone.** Close an arc by migrating its entire
  remainder to the next `NNN` — never strand work in a closed arc.

Templates: [`templates/plan.template.md`](templates/plan.template.md),
[`templates/handoff.template.md`](templates/handoff.template.md).

## Quality gates

- **One canonical gate == CI.** Run the exact CI gate locally, whole, before pushing — the repo's
  `make check` / `npm run validate` (format + lint + type + test + build). Never à la carte, so "green"
  is trustworthy. Watch the trap seen in the estate: **CI must not under-cover the local gate** — if
  `audit`, e2e, or secret-scan run only locally, a green PR check is not the full gate. Push them into
  CI.
- **Strict TDD, RED first.** Model the desired behavior and observe the red before implementing.
  Modules only (parsers, validators, pure lib); rendering, wiring, glue, config, and one-shot scripts
  are covered by build + lint + e2e — that is the e2e suite's job, not a unit test's. Value-add tests
  only; never chase coverage.
- **Strict lint + typing + security always**, on every file, whether or not it carries unit tests. Run
  the audit/security target (`npm audit`, dependency + secret scan) as part of the gate. Pin every
  GitHub Actions `uses:` to a full commit SHA.

## Verification loop (verdict-is-the-status)

The verification's exit code IS the status. A run either self-certifies or fails loud.

- **Verify on the live target.** Run e2e against **local AND the remote deploy** — never assume from a
  localhost 200 or a `curl`. `curl` can pass where the browser fails on a per-encoding cache variant.
- **Browser e2e = patchright/Chromium** across a viewport x device matrix, each rotated portrait AND
  landscape. Click every interactive control (not just assert render). Capture screenshots always +
  opt-in video; **read 2-3 screenshots** — appearance is a vision step the headless run cannot fully
  self-assert.
- **App console errors fail the run** (`page.on("console"/"pageerror")`); capture failed network
  requests. A standing security regression falls out for free: assert the browser never reaches a model
  host or leaks a secret.
- **Edge-settle before verifying.** A deploy-race against an immutable-asset/SPA-fallback cache is the
  dominant *silent* failure mode learned from prior runs (one shipped blank pages undetected for a long
  time). Add a settle wait + an asset-hash/MIME poll before the remote sweep; some hosts need a
  headed-under-xvfb leg to clear a managed challenge.
- **Commit a run manifest** (append-only `runs.jsonl`, PASS/FAIL kept honestly — an honest-FAIL budget,
  not hidden). A later session reads history instead of re-running. Add a **scheduled remote monitor**
  (credential-free) that auto-opens/updates an alert issue on FAIL.

## Context economy

See [`.claude/rules/context-management.md`](../.claude/rules/context-management.md) for the 40-60%
target and the ACE-FCA quality equation. Unattended-specific:

- **Configure compaction, do not just intend it.** The model cannot self-trigger `/compact`. Set
  `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` (e.g. `50`) to fire auto-compact earlier (main + subagents) and a
  `SessionStart:compact` hook that re-onboards the agent post-compaction (re-read the newest
  handoff+plan; keep conclusions, drop noise). Snippet:
  [`templates/settings.unattended.jsonc`](templates/settings.unattended.jsonc).
- **What to preserve on compaction:** the current arc + its state, this session's shipped PR list,
  ordered next steps + done-whens, branch/PR/CI state + anything uncommitted, parked owner-gated items +
  their pre-staged artifacts, and unresolved decisions + the defaults being applied. Drop raw command
  output, file dumps, and search results already distilled into the above.
- **Delegate discovery to subagents** — fan out read-only exploration, return structured findings only;
  the main thread keeps conclusions, not dumps. Redirect verbose command output to files; read back the
  relevant slice.

### Tuning compaction

Learned from prior runs, in ROI order:

- **Subagent discovery + verification aggressively — the single biggest lever.** Raw file reads dominate
  token spend (they can eat the majority of a window); isolating them in subagents keeps the dumps out
  of the main window entirely, so compaction fires later and loses less. Do this before tuning anything.
- **Add a `PreCompact` archive hook — the highest-ROI config change.** It flushes a rich handoff to disk
  (and may gate) *before* the summary replaces the window; it never itself triggers compaction. That
  turns a compaction from a loss into a checkpoint. Pair it with the handoff format.
- **"Compact at each phase transition" is not directly triggerable** — the model cannot fire `/compact`;
  only the `%` threshold or a manual call does. Practical substitutes: (a) **tune the threshold** — an
  aggressive value (e.g. 50) fires often and risks firing mid-task, a higher value (~65-70) gives more
  runway while still leaving recovery room; (b) lean on **milestone-flushing** (the durable ledger) so
  the exact trigger point stops mattering.
- **Sharpen "what to preserve" to the LIVE arc state**, not generic guidance — the automatic summarizer
  reads that section, so naming the current arc's shipped list, one-step resume, and parked gates makes
  the *right* specifics survive.
- **Quality drop is real but bounded.** The summary keeps the gist and drops specifics: exact snippets,
  constraints discussed-but-not-written, half-formed mid-task reasoning. Worst mid-task, smallest at a
  milestone boundary. The mitigation is the durable ledger — the post-compaction session reads facts
  from git + memory + docs rather than trusting the summary; quality holds when the stores are complete
  and degrades only on nuance that lived only in chat.
- **Make the statusline unambiguous.** A "free until compact" figure measures against the threshold, not
  the full window; show both (e.g. `46% used - compacts at 50%`) or an "imminent" flag.

### The durable ledger

Learned from prior runs: **treat the conversation as scratch; the ledger is durable.** The transcript is
volatile and lossy — a compaction summarizes and can drop specifics — so it is never the source of
truth. Flush the state that matters into three durable layers at *every milestone*, so a compaction or a
cold new session is a non-event: the next turn reads the summary plus the stores and continues exactly
where you were.

- **git / the remote** — the code is the artifact. Commit and PR bodies carry the *why* + the
  verification that the transcript would otherwise hold; if the whole session evaporated, `git log` +
  the branches reconstruct everything.
- **auto-memory** (`MEMORY.md` index + an arc-state file) — the wake-up briefing loaded at session
  start: the shipped list, the exact one-step resume command, branch/commit refs, deferred items, and
  the parked owner-gates.
- **plan + handoff docs** — the versioned source map + onboarding in the repo.

Keep all three in sync each milestone. The common miss: memory gets synced but the plan/handoff are left
stale by a few shipped items — memory then holds the resume-critical facts while the canonical docs lag.
Fold a `docs(NNN)` sync into the next wrap-up so all three layers agree.

### Ephemeral by design — mine, then prune

Two of those three layers are durable only *against compaction*, not against the repo's lifetime. Draw
the line explicitly:

- **Ephemeral working state** — plans, handoffs, findings, `MEMORY.md` / auto-memory, session summaries.
  These exist to carry an arc across sessions and compactions. They are **not** permanent documentation.
- **Durable SOT** — committed code + git history (commit/PR bodies), ADRs, `AGENT_LEARNINGS.md`, and
  `.claude/rules/`. This is what outlives the arc.

Run a **regular evaluation cadence** over the ephemeral set: **mine** each artifact for any durable
learning and promote it to the SOT (a learning to `AGENT_LEARNINGS.md`, a recurring constraint to a
rule, a decision to an ADR, the *why* into a commit body), then **prune** the artifact — delete a closed
arc's plan/handoff/findings, compress a bloated memory file to current state, drop stale session notes.
Compression is the anti-graveyard quality gate: distil, do not accumulate. An arc that has shipped and
been mined leaves durable value behind and takes its scaffolding with it.

## The unattended tax

Recurring friction every hands-off run must budget for. Encoded as hard rules in the loaded rule; here
with the fix.

| Hazard | Fix |
| --- | --- |
| Bare `git`/`gh` 403 on writes (`GH_TOKEN`/`GITHUB_TOKEN` shadow the real credential) | Prefix every call with `env -u GH_TOKEN -u GITHUB_TOKEN` |
| `git commit -m` shell-substitutes backticks / `$()` in the message | Commit with `-F <file>`; sign off with `--no-gpg-sign`; rebase with `-c commit.gpgsign=false` |
| Merge classifier / branch protection blocks agent auto-merge | Merge is an owner gate — park the green PR for approval; `--admin` bypasses only the signature gate, never a failing check; never relax protection |
| Stuck required check (e.g. `CodeFactor: ERROR`) | Update the branch to `main` for a fresh signed SHA; never nudge-commit, never `--admin` past a genuinely absent check |
| Deploy-race / edge cache serves the old build | Settle wait + asset-hash/MIME poll before verifying; never start a sweep in the same breath as the deploy |
| Session/container death loses uncommitted work | git is the only durable SOT; commit-as-you-go; long runs use resume-from-run-id |
| Broad Bash allowlist widens prompt-injection blast radius (acute for scrapers) | Keep the allowlist narrow; use `Read`/`Grep`/`Glob` + `uv run python` one-liners over `cat`/`grep` |
| markdownlint MD049 (per-file emphasis) / MD004 (per-file bullet) flips on a mixed edit | Match the target file's existing emphasis + bullet char; gate the linter with `if`, not `set -e` |

## Mechanism (derived downstream)

Per the META -> MECHANISM split, the runnable pieces are NOT hosted in this repo. This contract
specifies them; the mechanism lives in the
[`claude-code-plugins`](https://github.com/qte77/claude-code-plugins) marketplace
(`qte77-claude-code-plugins`). Reuse what exists; build the rest.

**Already in the marketplace — reuse, do not reinvent:**

- **Scaffolding** — `workspace-setup` (idempotent SessionStart deploy of rules + statusline + base
  settings + governance MD). This is where the kit's rule + templates + autocompact settings must be
  added so new repos inherit them automatically.
- **Context economy** — the `cc-meta` plugin: `compacting-context` (distil verbose output to a
  structured template), `handing-off-session` (write a durable handoff from git + conversation),
  `summarizing-session-end`, plus `researching-codebase` (subagent-isolated discovery, the biggest
  context lever). The `read-once` dedup hook (`workspace-sandbox`) blocks re-reads to save tokens on
  long runs.
- **Docs + git gates** — `docs-governance` (hierarchy + AGENTS.md audits), `security-audit`,
  `readme-generator`, `tdd-core`, `simplify`, and `commit-helper` (commit + PR skills with explicit
  approval pauses — the owner merge gate, respected).
- **Planning** — the `planning` plugin's planner agent (phased plans with file-level steps).

**Gaps to build (the kit's true missing mechanism):**

- **A scaffolded `unattended-execution` rule** — `workspace-setup` currently deploys only
  core-principles / context-management / compound-learning. Add this contract's rule to that set so
  hands-off mode ships by default. It must reconcile with core-principles (see below).
- **A browser-sweep skill** (patchright/Chromium) — none exists (`web-recon` is API-only,
  `website-audit` is WebFetch-only). Must implement the
  [verification loop](#verification-loop-verdict-is-the-status): device matrix, console-error-fail,
  local + remote, screenshots, and a committed run manifest (`runs.jsonl`).
- **Auto-firing `PreCompact` + `SessionEnd` archiving** — only a PostCompact cache-clear exists. Wire
  `PreCompact` to `handing-off-session` and `SessionEnd` to `summarizing-session-end` so the flush is
  automatic, not manual-skill-triggered.
- **Plan+handoff pairing + arc-closure audit** — planning creates plans and `handing-off-session`
  creates handoffs, but nothing pairs them, builds the source map, or verifies arc closure/prune.
- **Scaffolded autocompact settings + plan/handoff templates** — add the threshold + `PreCompact` /
  `SessionStart:compact` hooks and the templates to `workspace-setup`'s deployed set.
- **A scheduled remote monitor** (`.github/workflows/*-monitor.yml`) — credential-free cron probe that
  auto-opens/updates an alert issue on FAIL.
- **A `git -> gate -> PR -> park` loop skill** chaining the existing gate + `commit-helper` skills and
  stopping at the owner merge gate.

## Refs

- Rule: [`.claude/rules/unattended-execution.md`](../.claude/rules/unattended-execution.md)
- Related rules: [`context-management.md`](../.claude/rules/context-management.md),
  [`compound-learning.md`](../.claude/rules/compound-learning.md),
  [`core-principles.md`](../.claude/rules/core-principles.md)
- Templates: [`plan.template.md`](templates/plan.template.md),
  [`handoff.template.md`](templates/handoff.template.md),
  [`settings.unattended.jsonc`](templates/settings.unattended.jsonc)
- Decision routing: [`project-workflows.md`](project-workflows.md)
- Learnings: [`../AGENT_LEARNINGS.md`](../AGENT_LEARNINGS.md)
