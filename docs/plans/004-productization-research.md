---
status: proposed — not started
phase: Phase A — market/competition/ICP research fan-out
handoff: ../handoffs/004-productization-research.md
updated: 2026-08-03
---

# Productization research — market, competition, ICP, USP for the qte77 approach

Decide whether — and as what — the qte77 approach is sellable: the orchestrators
([polyforge](https://github.com/qte77/polyforge-orchestrator) +
[office-forge](https://github.com/qte77/office-forge-orchestrator)) as the adoption wedge, and the
BRD/PRD/FRD → OKR/KPI governance layer as the paid tier. This arc produces **research + a BRD, not
code**; PRD/FRD and any implementation are downstream. This doc is the source map so a fresh session
executes without re-exploring; read the paired [handoff](../handoffs/004-productization-research.md)
first.

## Why

`docs/operating-model.md` recorded a **commercial** adversarial verdict in 2026-06 and then
**voided its moat/TAM/competition cuts** on the grounds that "our purpose is to _showcase_ a working
agentic estate, not to sell one" (`docs/operating-model.md:85-90`). Productizing **re-arms every
voided cut**. This arc does not get to inherit that voiding — it must re-run the commercial frame
honestly, against real market evidence rather than reasoning-from-first-principles, and produce a
BRD that either survives or kills the idea cheaply.

## Owner decisions (locked, 2026-08-03)

| Decision | Rationale |
| --- | --- |
| **Two products, not one** — P1 orchestrator (wedge) + P2 governance/eval layer (paid) | Different buyers, competitors, and pricing logic; fusing them produces an unanalysable BRD |
| **P1 is the wedge, P2 is the monetization hypothesis** | Nobody buys governance first; they buy "run N agents without chaos," then discover they cannot prove outcomes |
| **Stage 0 (this plan) precedes any research spend** | Sharpens the questions before a 12–15 agent fan-out burns tokens on the wrong ones |
| **Research fan-out runs as a dynamic workflow; BRD synthesis runs single-threaded** | Fan-out is wide + independent; synthesis needs one coherent voice and does not parallelize |

## Decide-by-default (apply silently unless overridden at the Phase B checkpoint)

| Open decision | Default applied |
| --- | --- |
| Comparable set beyond the three named (Airbyte, monaco.com, micro1) | Add Cognition/Devin, Swarmia **or** DX, LangSmith **or** Braintrust, Linear — covering agent-execution, eng-effectiveness, eval, and work-tracking adjacencies |
| P2 scope in the BRD | Scope P2 to the **narrow eval-before-work forcing function** (`operating-model.md:60-65`), _not_ the full traceability spine (`:71` = commercial DISCARD) |
| Licensing/OSS posture | Open-core: orchestrators stay permissive; governance layer is the commercial candidate. Revisit only if research shows the wedge does not convert |
| Positioning framework | April Dunford (competitive alternatives → unique attributes → value → who cares most) — it forces the competitive frame the prior distillation says is the weak point |
| Named-company facts | Treat **all** GTM/pricing/ICP claims as research outputs requiring a citation; assert nothing from model priors (esp. monaco.com, which is unverified here) |
| Tracking issue | Open one `goal`-labelled issue for the arc — but only after owner OK (Phase B), since issues are outward-facing |

## Source map — touch without re-mapping (verified 2026-08-03, file:line)

### Prior-art / constraint documents (read before writing the BRD)

| File | Symbols / content | Role in this arc |
| --- | --- | --- |
| `docs/operating-model.md:43-81` | "The de-risking — adversarial distillation"; the fatal-flaw paragraph `:51-58`; **"What fell"** table `:69-77` | The un-voided commercial verdict. Every row is a BRD risk that must be answered with market evidence or conceded |
| `docs/operating-model.md:60-65` | "What survives — the bedrock (one thing)" — eval-before-work; "incentive, thin"; **~12–18 month** window | The only defensible P2 core. The time-box is the BRD's urgency argument _and_ its biggest risk |
| `docs/operating-model.md:82-107` | "Calibration" — `:88` voids moat/TAM/"reinventable" **for a showcase**; `:103-107` two-loops-one-apex (dev + office) | `:88` is what this arc reverses. `:103-107` is the P1 dual-vertical positioning asset |
| `docs/operating-model.md:125-141` | "What would earn building more" preconditions; "Kill conditions" | Preconditions are currently **unmet** (see Open questions). Kill conditions become BRD kill-criteria |
| `docs/cto-handbook-mapping.md` | handbook themes → operating model, adopt/defer status | Existing external-reference framing; both orchestrator READMEs already link it as their "baseline" |
| `AGENT_LEARNINGS.md` | "Calibrate adversarial / moat red-teams to the actual purpose" | The learning that _caused_ the voiding. Must be amended when this arc lands — the frame is no longer "showcase" |

### P1 — orchestrator product surface

| File | Symbols / content | Role in this arc |
| --- | --- | --- |
| `../../polyforge-orchestrator/README.md:4-9` | positioning line; "**For** teams running Claude Code across multiple repos" | Current P1 (dev) positioning statement — the baseline the BRD rewrites |
| `../../polyforge-orchestrator/README.md:30-46` | "How It Works" — `make setup_all`, sibling `devcontainer.json` lifecycle replay | The concrete technical differentiator to test for defensibility (multi-root workspaces drop sibling lifecycle hooks) |
| `../../polyforge-orchestrator/scripts/cc-parallel.sh` | `--preset validate` / `security-all` / `security-pr` | Feature surface for the FRD; the preset registry is the productizable unit |
| `../../polyforge-orchestrator/config/{repos.conf,contributions.json}` | fleet config + `--resume` execution state | State model; `contributions.json` is the cross-repo plan-execution SOT |
| `../../polyforge-orchestrator/docs/context-hygiene.md` | cascade flags, `--bare` dial | Differentiator candidate: multi-repo context isolation is a real, non-obvious problem |
| `../office-forge-orchestrator/README.md:4-11` | "invoices, contracts, reports, email"; **For** office workers / ops teams | P1's second vertical — the dual-loop proof, and a _different_ ICP to size separately |
| `../office-forge-orchestrator/{templates,mcp}/` | project scaffolds; business-API MCP configs | Vertical-templates surface — the likeliest office-side monetization unit |

### P2 — governance / eval rails (already built; the BRD's "existing asset" column)

| File | Symbols / content | Role in this arc |
| --- | --- | --- |
| `.github/workflows/kr-eval-gate.yml:23-53` | the gate step; `closingIssuesReferences` lookup `:31-33`; dormant-pass `:35-36`; `^eval:\s*\S` check `:47-48` | **The one commercially-surviving artifact.** ~50 lines. Demo centerpiece and the thing to price |
| `.github/ISSUE_TEMPLATE/goal-kr.md:16-22` | `goal_id`, `eval:`, `**Cynefin:**` fields | Where a PRD outcome becomes an enforced KR — the BRD/PRD/FRD → tracking join point |
| `goals.json:5-6` | minimal schema; `"goals": []` — **empty** | The rails are dormant: zero closed KR cycles. Blocks the "proven in production" claim |
| `scripts/goal_rollup.py:35-69` | `render()`; `issue_state()` via `gh` `:23-32`; `--write` → `STATUS.md` `:75-77` | The KPI rollup. Dependency-free; the "how KPIs get tracked" answer in the PRD |
| `docs/goals.md:41-55` | the 7-step loop (Author → Open → Work → Enforce → Trace → Track → Learn) | The end-to-end flow the BRD/PRD/FRD layer plugs into at step 1 |
| `docs/goals.md:57-61` | "Current state — empty by design" | Honesty constraint: do not let the BRD claim traction the rails do not have |
| `CLAUDE.md` "Task-tracking authority" | Issues = SOT; `contributions.json`/tracker = derived; `goals.json` = META | The entity model the BRD/PRD/FRD layer must not violate (no second tracking system) |
| `docs/architecture.md:44-52` | Roadmap: Now / Next / Later (air-gapped, BYOM) | Existing public roadmap — the BRD must either adopt or explicitly supersede it |

### Estate conventions this arc obeys

| File | Role |
| --- | --- |
| `.claude/rules/unattended-execution.md` | Phase A/B/C shape; arc = plan+handoff pair; ephemeral-scaffolding rule; merge is an owner gate |
| `docs/doc-structure.md` | README/CONTRIBUTING/AGENTS split — any product-facing README this arc proposes must conform |
| `.claude/rules/context-management.md` | Incorrect > missing > noisy. Drives the adversarial-verify stage on every market claim |

## Phase plan (non-blocked A/B/C)

- **Phase A — agent-only.** Research fan-out (workflow, 12–15 agents, three lanes: comparables
  teardown / ICP+JTBD / category+competition per product), each returning a fixed schema; then an
  adversarial verify stage where every market claim must survive an independent skeptic or be dropped
  to "unsourced." Findings land in `docs/plans/004-productization-research-findings.md`. Then
  single-threaded BRD synthesis. **Pre-stage for Phase B:** the tracking-issue body, the
  `goals.json` goal+KR entries (written, uncommitted), and the customer-discovery interview guide.
- **Phase B — one owner sitting.** Approve/override the decide-by-default table; open the tracking
  issue; approve the BRD's go/no-go; authorize (or decline) customer-discovery outreach — the only
  step that touches real people and cannot be agent-run.
- **Phase C — activation.** PRD + FRD per surviving product (one subagent each); wire BRD objectives
  → `goals.json` → KR issues; run `goal_rollup.py --write`; amend `AGENT_LEARNINGS.md` for the frame
  flip; update `docs/operating-model.md` with the re-armed verdict.

## Backlog (each item states its done-when)

| # | Item | Gate | Done-when |
| --- | --- | --- | --- |
| 1 | Comparables teardown — Airbyte, monaco.com, micro1 + 4 defaults | agent | Each has ICP, wedge, pricing/packaging, OSS-vs-cloud split, positioning language, explicit non-goals — every claim carrying a source URL |
| 2 | ICP + JTBD per candidate segment (platform eng, AI-mandate CTO, ops/back-office, agencies) | agent | Each segment has a job-to-be-done, current alternative, trigger event, and a rough reachable-population basis |
| 3 | Category + competitive matrix, **separately for P1 and P2** | agent | Matrix with a named wedge per product and the nearest incumbent that closes it |
| 4 | Adversarial verify pass on all of 1–3 | agent | Every surviving claim is sourced; unsourced claims are relegated to an explicit "assumption" list |
| 5 | Re-run the `operating-model.md:69-77` "What fell" table under the **commercial** frame | agent | Each of the 7 rows answered with market evidence: still-falls / survives-with-evidence / now-untestable |
| 6 | Positioning + USP statement (Dunford) per product | agent | Competitive alternatives → unique attributes → value → who-cares-most, each line traceable to item 1–3 evidence |
| 7 | Pricing + packaging hypothesis | agent | Open-core boundary drawn explicitly: what is free, what is paid, and the defensibility argument for the paid line |
| 8 | **BRD** — problem, market, business case, kill-criteria | agent | Single doc; carries the unmet-preconditions risk (`operating-model.md:127-136`) and the ~12–18mo window as explicit, dated risks |
| 9 | Tracking issue + `goals.json` seed entries, pre-staged | agent | Issue body + goal/KR JSON written and reviewable, **not** posted/committed |
| 10 | Customer-discovery interview guide | agent | 8–12 questions targeting willingness-to-pay, which public research cannot answer |
| 11 | Owner checkpoint — approve defaults, open issue, go/no-go, authorize outreach | **owner** | Decisions recorded in this plan's Owner-decisions table |
| 12 | PRD + FRD per surviving product | agent | One PRD + one FRD each, outcomes expressed as KRs with pre-committed `eval:` lines |
| 13 | Wire BRD → `goals.json` → KR issues → `STATUS.md` | agent | `python scripts/goal_rollup.py` renders non-empty per-goal % ; gate passes on a real KR PR |
| 14 | Amend `AGENT_LEARNINGS.md` calibration entry + `operating-model.md` for the frame flip | agent | Both state that the commercial frame is now live and the `:88` voiding no longer applies |

## Owner-gates (the only things that block hands-off)

| Gate | Pre-staged in Phase A | The switch the owner flips |
| --- | --- | --- |
| Tracking issue creation | Issue body drafted (backlog #9) | `gh issue create` approval |
| BRD go/no-go | Full BRD + kill-criteria (#8) | Proceed to PRD/FRD, or kill |
| Customer-discovery outreach | Interview guide (#10) | Authorize contacting real people |
| `goals.json` commit | Goal/KR entries written, uncommitted (#9) | Approve — goals are **human-authored** per `CLAUDE.md` task-tracking authority |
| Any merge | Green PR parked | Squash-merge; never agent auto-merge |

## Verification

No build/test gate applies (docs-only arc). The gate is:

```bash
markdownlint $(git ls-files '*.md')
lychee $(git ls-files '*.md')        # --offline to skip network
```

Plus the arc-specific quality gate: **every market claim in the findings and BRD carries a source
URL, or is listed as an assumption.** Per `.claude/rules/context-management.md`, incorrect
information is the worst failure mode, and market research is where confabulation is most likely —
an unsourced-but-confident BRD is a _worse_ outcome than no BRD.

## Open questions

- **The preconditions in `operating-model.md:127-136` are unmet.** `goals.json:6` is empty — the
  eval-gate has run across **zero** closed KR cycles, not the required ≥3, and no second tenant's
  loop has closed. Productizing now inverts the repo's own recorded sequencing. Trade-off: research
  is the cheap way to decide _whether_ to invest in meeting them, but the BRD cannot claim validated
  traction. **Recommendation:** proceed with research; block any "proven" language in the BRD.
- **Public research cannot establish willingness-to-pay.** Pricing pages, docs, job ads and
  changelogs yield inference, not demand. The BRD must carry this as a stated assumption with
  customer discovery as the validating step (backlog #10, gate #11).
- **The ~12–18 month window (`operating-model.md:64-65`) started 2026-06-28** — roughly 13 months
  remain by that estimate. Whether that is enough to productize is a genuine unknown the research
  should inform.
- **Is monaco.com actually a relevant comparable?** Named by the owner; its GTM archetype is
  unverified here and must not be asserted from priors.

## Refs

- Paired handoff: [`004-productization-research`](../handoffs/004-productization-research.md)
- [`docs/operating-model.md`](../operating-model.md) — the prior commercial verdict this arc re-arms
- [`docs/goals.md`](../goals.md) — the 7-step loop the BRD/PRD/FRD layer plugs into
- [`docs/cto-handbook-mapping.md`](../cto-handbook-mapping.md) — existing external-reference framing
- Comparables named by the owner: <https://airbyte.com/>, <https://www.monaco.com/>, <https://www.micro1.ai/>
- Tracking issue: TBD (backlog #9, owner-gated)
