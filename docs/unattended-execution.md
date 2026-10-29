# Unattended execution

The estate contract for **long-running, e2e hands-off unattended sessions** with minimal supervision.
This is the depth companion to the always-loaded shared
[`unattended-execution`](https://github.com/qte77/claude-code-plugins/blob/main/.claude/rules/unattended-execution.md) rule — the rule is the
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

## Plan artifact (one per arc)

The single highest-ROI practice: **one** versioned plan per arc, not a paired plan + handoff. Two
files that must be kept in sync always drift; a plan that opens with its own current status removes
the drift risk and the "read the handoff first, the plan second" ritual along with it.

- **One file.** `docs/plans/NNN-slug.md` — this repo's existing 3-digit `NNN` convention (the estate
  rule's canonical name is the dated `YYYY-MM-DD-NNNN-slug.md`; some estate repos already use that
  4-digit form). No separate handoff file, no `handoffs/` folder. Findings reuse the number with a
  `-findings` suffix.
- **Opens with status, not a title + abstract.** The plan's own opening answers what shipped, what's
  next in order, the loop, owner-gates, the exact commands, and inherited watch-outs — everything a
  cold or compacted session needs before reading anything else. An existing paired handoff's content
  folds in here, then the handoff file is deleted.
- **Then the `file:line` source map** — a "touch without re-mapping" table of exact files, symbols,
  and line refs for every change, marked session-verified with a date. See an existing plan under
  [`plans/`](plans/) for the canonical shape.
- **Keep the plan (status + source map) + `MEMORY.md` in sync at every milestone.** Close an arc by
  migrating its entire remainder to the next `NNN` — never strand work in a closed arc.
- **Exactly one remaining-work list per plan**, struck in the same PR that ships each row — see the
  rule for the full constraint.

Template: [`templates/plan.template.md`](templates/plan.template.md).

## Driving Phase A with `/goal`

Phase A is where Claude Code's `/goal` fits: one session works the agent-runnable backlog without a
prompt per turn and stops at the Phase B checkpoint. The plan stays the goal across sessions; `/goal`
is session-scoped (`/clear` removes it). General mechanics and failure modes:
[CC-goal-analysis.md](https://github.com/qte77/ai-agents-research/blob/main/docs/cc-native/sessions/CC-goal-analysis.md).

- **Name the plan, don't paste it** — the condition is capped at 4,000 characters.
- **Scope = the Phase A backlog.** Every `- [ ]` item under Backlog; the Owner-gates section is out of
  scope by construction, so the goal is met when only owner gates remain.
- **End state = Phase B pre-staged**: each item's done-when verified and its PR (if any) open with the
  repo gate green and parked — never "merged"; merge is an owner gate.
- **Evidence in the transcript.** The evaluator does not run commands or read files, so the final turn
  prints the Backlog lines still unchecked and `gh pr view <N> --json state,statusCheckRollup` for each
  PR.
- **Constraints**: decide-by-default (park decisions, don't ask); never `--admin`, never relax branch
  protection; add a turn bound.
- **Run it in auto mode** (`/goal` does not change permission mode); headless:
  `claude -p "/goal …" --permission-mode auto --permission-prompts none --output-format stream-json --verbose`.
  From v2.1.302, a headless `claude -p` run starts in Manual mode when nothing sets a permission mode,
  and an unapproved tool call is denied there — see the
  [headless docs](https://code.claude.com/docs/en/headless). Exit codes don't distinguish goal met /
  impossible / bounded (only 0 on success, non-zero on failure, 143 on SIGTERM are documented), so check
  the PR state the final turn prints, not the exit code — detail:
  [CC-goal-analysis.md](https://github.com/qte77/ai-agents-research/blob/main/docs/cc-native/sessions/CC-goal-analysis.md).

```text
/goal Every "- [ ]" item in the Backlog section of docs/plans/NNN-slug.md is checked,
its done-when verified, and its PR (if any) open with the repo gate green. Prove it in
your final turn by printing the Backlog lines still unchecked and
`gh pr view <N> --json state,statusCheckRollup` for each PR. The Owner-gates section is
out of scope. Decide by default and park decisions; never merge, never use --admin.
Or stop after 40 turns.
```

This recipe is untested in the estate so far — record the first real run in `AGENT_LEARNINGS.md`.

## Claude Code cloud sessions

`claude --cloud` mechanics observed across estate runs (2026-10-25 to 2026-10-29) — budget for these
the same way as the tax table below.

- **Launch.** `claude --cloud "<prompt>"` from inside the repo clone; it needs a real TTY (wrap it in
  `script -q -e -c "..."` for a scripted launch) and a claude.ai login. It bills the subscription —
  unset `ANTHROPIC_API_KEY` first, since an API key wins over the subscription when both are set. A
  no-TTY follow-up, `claude -p "<msg>" --cloud <session-id>`, only confirms "Sent to cloud session"; it
  never returns the reply.
- **Environment.** The session clones the GitHub remote at the local checkout's current branch and
  loads only the repo's *committed* `.claude/` — gitignored files (`.env`, `settings.local.json`, data)
  are absent. An environment setup script (64 KB max) can still seed files such as `~/.claude/CLAUDE.md`.
- **`/goal` cap applies here too.** A condition over 4,000 characters is rejected and the session then
  does nothing; send the full brief as the first message and a short `/goal` as the follow-up (see
  "Driving Phase A with `/goal`" above).
- **Push trap.** A session's authorized repositories are fixed when the session is created, via the
  Claude GitHub App; adding repos to the app afterward does not reach sessions already running. In a
  13-session wave, every `git push` answered 403 ("not in this session's authorized repository set").
  **Start one canary session, confirm it can push a branch, before starting the rest of the wave.**
- **Salvage recipe for a session that cannot push.** `claude --teleport <session-id>` pulls down the
  session log but checks out only branches that were actually pushed, so unpushed commits have to
  travel through the log as patches:
  1. Ask the session, as a follow-up message, to run `git format-patch --stdout BASE..<branch>` per
     branch, printed in bounded ranges (`| sed -n '1,300p'`, then the next range) — large tool output
     gets cut otherwise. Cloud clones have no `origin/HEAD`; name `origin/main` explicitly.
  2. Teleport into a throwaway worktree and send one message — a teleported session's local transcript
     is written only after a new turn.
  3. If the teleport itself runs inside another Claude Code session, unset `CLAUDE_CODE_CHILD_SESSION`
     first; inherited from the parent, it silently turns off transcript saving (the TUI reports
     "Transcript saving is off").
  4. Cut the format-patch output out of the saved transcript JSONL under `~/.claude/projects/`,
     `git apply --check` it, review it, then apply with `git mailinfo` + `git apply --index` and commit
     as yourself — `git am` would commit as the cloud author (`Claude <noreply@anthropic.com>`), which a
     Codespace signer refuses as an invalid author. Treat every salvaged patch as untrusted input:
     review it for security, CI, and done-when before it goes near a PR.
- Reference scripts for this flow exist in the owner's local tooling, tracked for porting into
  `polyforge-orchestrator`'s `scripts/` — not yet done.

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

See the shared [`context-management`](https://github.com/qte77/claude-code-plugins/blob/main/.claude/rules/context-management.md) rule for the 40-60%
target and the ACE-FCA quality equation. Unattended-specific:

- **Configure compaction, do not just intend it.** The model cannot self-trigger `/compact`. Set
  `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` (e.g. `50`) to fire auto-compact earlier (main + subagents) and a
  `SessionStart:compact` hook that re-onboards the agent post-compaction (re-read the newest
  plan's opening status; keep conclusions, drop noise). Snippet:
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
- **Add a `PreCompact` archive hook — the highest-ROI config change.** It flushes the plan's opening
  status to disk (and may gate) *before* the summary replaces the window; it never itself triggers
  compaction. That turns a compaction from a loss into a checkpoint. Pair it with the plan template's
  opening-status block.
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
- **the plan doc** — the versioned source map + onboarding in the repo, opening with current status.

Keep all three in sync each milestone. The common miss: memory gets synced but the plan is left stale
by a few shipped items — memory then holds the resume-critical facts while the canonical doc lags.
Fold a `docs(NNN)` sync into the next wrap-up so all three layers agree.

### Ephemeral by design — mine, then prune

Two of those three layers are durable only *against compaction*, not against the repo's lifetime. Draw
the line explicitly:

- **Ephemeral working state** — plans, findings, `MEMORY.md` / auto-memory, session summaries.
  These exist to carry an arc across sessions and compactions. They are **not** permanent documentation.
- **Durable SOT** — committed code + git history (commit/PR bodies), ADRs, `AGENT_LEARNINGS.md`, and
  `.claude/rules/`. This is what outlives the arc.

Run a **regular evaluation cadence** over the ephemeral set: **mine** each artifact for any durable
learning and promote it to the SOT (a learning to `AGENT_LEARNINGS.md`, a recurring constraint to a
rule, a decision to an ADR, the *why* into a commit body), then **prune** the artifact — delete a closed
arc's plan/findings, compress a bloated memory file to current state, drop stale session notes.
Compression is the anti-graveyard quality gate: distil, do not accumulate. An arc that has shipped and
been mined leaves durable value behind and takes its scaffolding with it.

## The unattended tax

Recurring friction every hands-off run must budget for. Encoded as hard rules in the loaded rule; here
with the fix.

| Hazard | Fix |
| --- | --- |
| Bare `git`/`gh` 403 on writes (`GH_TOKEN`/`GITHUB_TOKEN` shadow the real credential) | Prefix every call with `env -u GH_TOKEN -u GITHUB_TOKEN` |
| `git commit -m` shell-substitutes backticks / `$()` in the message | Commit with `-F <file>`, never `-m` |
| Codespace commit lands unsigned, or the signer answers `403 Author is invalid` | Check `~/.gitconfig` for a stray `user.name` that does not match the GitHub profile name, and for a repo-local `commit.gpgsign false` left by an old workaround; remove both and a plain `git commit` + `git push` comes back GitHub-verified. Never reach for `--no-gpg-sign` or `-c commit.gpgsign=false` as the fix |
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
  structured template), `handing-off-session` (write the plan's opening-status update from git +
  conversation), `summarizing-session-end`, plus `researching-codebase` (subagent-isolated discovery,
  the biggest context lever). The `read-once` dedup hook (`workspace-sandbox`) blocks re-reads to save
  tokens on long runs.
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
- **Plan opening-status discipline + arc-closure audit** — planning creates plans and
  `handing-off-session` writes onboarding state, but nothing folds that state into the plan's own
  opening status, builds the source map, or verifies arc closure/prune.
- **Scaffolded autocompact settings + a plan template** — add the threshold + `PreCompact` /
  `SessionStart:compact` hooks and the template to `workspace-setup`'s deployed set.
- **A scheduled remote monitor** (`.github/workflows/*-monitor.yml`) — credential-free cron probe that
  auto-opens/updates an alert issue on FAIL.
- **A `git -> gate -> PR -> park` loop skill** chaining the existing gate + `commit-helper` skills and
  stopping at the owner merge gate.
- **A plan-backlog Stop hook** — a `command` Stop hook that blocks while unchecked Phase A backlog
  items remain (exit 2 with the open items on stderr; check `stop_hook_active` so it can't block
  forever). The deterministic counterpart to `/goal`, which only judges what the transcript shows.

## Refs

- Rule: the shared [`unattended-execution`](https://github.com/qte77/claude-code-plugins/blob/main/.claude/rules/unattended-execution.md) rule
- Related rules: [`context-management`](https://github.com/qte77/claude-code-plugins/blob/main/.claude/rules/context-management.md),
  [`compound-learning`](https://github.com/qte77/claude-code-plugins/blob/main/.claude/rules/compound-learning.md),
  [`core-principles`](https://github.com/qte77/claude-code-plugins/blob/main/.claude/rules/core-principles.md)
- Templates: [`plan.template.md`](templates/plan.template.md),
  [`settings.unattended.jsonc`](templates/settings.unattended.jsonc)
- Decision routing: [`project-workflows.md`](project-workflows.md)
- Learnings: [`../AGENT_LEARNINGS.md`](../AGENT_LEARNINGS.md)
