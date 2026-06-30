# Operating Model

> **Status: explored + pressure-tested. Most of this is deliberately _not_ built.**
> This records the operating-model concept, the adversarial distillation that de-risked it,
> and the decision it produced — _ship one cheap forcing-function, shelve the rest until it
> earns building._ It exists so the cathedral doesn't get re-proposed from scratch.

## The idea — steer top-down, trace bottom-up

A single human steers the agentic estate from the **top** (set goals, approve at a few
high-leverage gates, re-prioritise) while objective evidence flows back from the **bottom**
(code → story → spec → goal), so you **steer by exception** — intervene only when a signal
leaves its expected band — instead of micromanaging. Generalise the tenant (qte77 → other
projects / products / businesses) and it's a portfolio operating model: one operator, N
agent-run tenants, one shared engine. This is the `liminal-flux` North Star ("goals flow down ·
learnings flow back"), scaled and made measurable.

```text
            STEER (down)                          EVIDENCE (up)
META    goals (OKRs, per tenant)            ←   goal achievement % (eval-measured)
KERNEL  shared spec / eval templates                     ▲
MECH.   orchestrators: goals → specs → tasks             │   eval verdicts roll up
STATE   the trace backbone (join table)    ──────────────┤
CONSUM. repos: agents write code           ──────────────┘   commit → story → spec → goal
```

## The concept stack (as explored)

- **EDD (Eval-Driven Development)** as the intended keystone: `Achieved = DoD satisfied AND the
  KR's eval passes target` — outcome, not output.
- **Traceability spine** — `ontology.json` as a _semantic layer + data catalog over
  work-artifacts_ (entities goal/spec/story/code/eval + typed relationships).
- **Three-standard stack** — OKR (goals) · OKF (open-world, tolerant markdown/YAML knowledge
  bundles per tenant) · closed-world SHACL/MQO-style validation **only at the KR↔eval seam**
  ("loose by default, rigor only where achievement must be provable").
- **Cynefin discipline** — design the Clear/Complicated parts; **probe** the Complex parts
  (don't over-design "what counts as achieved" for fuzzy KRs).
- **Probe → learn → promote** — hypothesis → happy-path E2E → fail-fast → make-or-break (eval)
  → compound-learning ladder (inline → `AGENT_LEARNINGS.md` → `.claude/rules/` → skills).

## The de-risking — adversarial distillation (2026-06-28)

Ran a via-negativa distillation (concede every advantage to incumbents — Linear/Jira,
dbt/Cube, DataHub/OpenMetadata, Databricks Genie, LangSmith/Braintrust, OKR SaaS, AWS
Kiro/spec-driven frameworks — keep only what survives an independent red-team). Almost
everything fell. That is a **successful** early de-risk: the breaks were found before a line of
the spine was built.

**The fatal flaw.** EDD's "objective bottom-up signal" is **self-certified, not independent** —
the eval is authored by the same operator who benefits from "Achieved." That is _worse than
Goodhart_ (the metric isn't even an independent proxy being gamed; it's the beneficiary's own
definition). For **Complex KRs** — where the eval can't be specified before the work — you
either reverse-engineer the eval after seeing output (a guaranteed pass) or exclude them,
collapsing EDD's honest scope to the ~30% of deterministic KRs **LangSmith already serves**. The
failure is invisible from inside: the only one who could audit it is the one who needs it to
pass.

**What survives — the bedrock (one thing).** The **eval-before-work forcing function**: a
written, non-empty eval (with a target metric) on the KR _before any agent touches it_. It does
**not** make the signal objective — but it forces you to _operationalise success before burning
cycles_, which most operators skip. Barrier type: **incentive, thin** — no OKR SaaS enforces
this GitHub-native at KR-creation; time-bounded (~12–18 months before GitHub Projects / Copilot
Workspace / Kiro make "spec is the contract" a platform feature).

**What fell** _(this is the **commercial** verdict — read it with the Calibration below, which voids the moat / TAM / "GitHub-closes-it" cuts for a showcase and keeps only the frame-independent ones):_

| Claim | Verdict |
|---|---|
| Traceability spine / `ontology.json` | DISCARD — DataHub / dbt / GitHub's native Issue↔PR graph already serve it; link-rot has no mitigation |
| Solo-operator portfolio "moat" | FALLS — GitHub has zero revenue conflict closing it; one sprint |
| "Loose by default, rigor at seams" | FALLS — a one-sentence methodology rule; prior art in DDD (2003) / EIP |
| Compound-learning ladder "self-evolving" | DISCARD — no quality gate on promotions → markdown graveyard |
| Steer-by-exception / deadband | DISCARD — a solo operator can't generate the volume to calibrate a threshold → collapses to full inspection |
| Multi-tenant portfolio | DISCARD — marginal tenant cost is O(n); a spreadsheet that worsens as it grows, not a platform |
| SHACL/MQO anti-Goodhart layer | DISCARD — it is _itself_ an eval, subject to the same circularity |

**The meta-risk.** Building the spine **is** the yak-shave the model exists to prevent — "the
cure is the disease." It is the single most likely failure mode.

## Calibration — read the verdict above with two corrections

The distillation optimised for **commercial defensibility** (moat / TAM / "a rival could copy it" /
"where to invest"). **Our purpose is to _showcase_ a working agentic estate, not to sell one.** That
voids part of the verdict and reframes the rest.

**Voided — commercial-only, irrelevant to a showcase:** "no moat," "GitHub closes the gap," "TAM too
small," "reinventable → discard." You don't need a moat to demonstrate a capability; _building the
coherent artifact is the point_.

**Survives — reframed as KISS / credibility (frame-independent):**

- **Self-certification** → don't _oversell_ "objective." A showcase that claims objective achievement
  but self-grades is a credibility risk. Anchor the showcase's credibility on the genuinely-independent
  signals — **external-project merges + office/business outcomes** (paid / signed / delivered).
  "Objective" is dead; **"pre-committed"** is the honest word for the internal eval.
- **Yak-shave / rot** → a showcase of _abandoned scaffolding_ is worse than none. Build only what
  _visibly works_; don't erect an ontology/cockpit that decays. KISS · AHA · YAGNI.
- **Goodhart / green-farming** → 9,286 self-merged contributions read as _farming_ to a sophisticated
  viewer and weaken the showcase. Tie cadence to goals + the objective surfaces, not the graph.

**Structural correction — two loops, one apex** (we'd omitted the business half): the model spans
**polyforge (DEV)** _and_ **office-forge (OFFICE)**, both under one `qte77/goals.json`. The dev/office
split _is_ the "multi-loop" showcase — by work-type, not account. Office KRs (invoice paid, contract
signed) and external-contrib merges are externally verified and **binary**, so the
genuinely-objective-eval surface is **larger** than the roast assumed.

## The decision (showcase-calibrated)

1. **Build the minimal coherent spine that visibly works:**
   - seed `goals.json` (2–3 OKRs + IDs + Cynefin tag) — the apex;
   - `kr-eval-gate.yml` (~50 lines) — eval-_before_-work pre-commitment, your missing reviewer;
   - `goal_id` on `contributions.json` plans (and office projects) — the goal→campaign link, by
     _reference_, nothing relocated;
   - **optional** (if it showcases well): a lite GitHub-native goal-rollup (a `gh` query →
     README/Action), not a cockpit.
2. **Keep shelved — KISS / anti-rot, not "no moat":** OKF bundles, SHACL/MQO, `ontology.json`
   goal/eval extension, self-evolving ladder automation, multi-tenant infra. Lean on GitHub-native
   trace + LangSmith/Braintrust for evals.
3. **Anchor credibility on the objective surfaces:** external-project merges + office outcomes — the
   showcase's honest "it actually works" evidence.
4. **Record + revisit:** this doc is the decision record — compound-learning applied to itself.

## What would earn building more

Revisit the spine only after **all** of these hold:

- The eval-gate runs across **≥3 closed KR cycles** and the forcing function proves it earns its
  friction.
- Your KR mix is genuinely **mostly Clear/Complicated** (deterministic success writable
  upfront). If it skews research/product/business (fuzzy), EDD's scope is too small to justify
  the spine — stop here.
- You have **never** reverse-engineered an eval after seeing output (one slip silently corrupts
  the signal, unrecoverably).
- A **second tenant's** loop closes without O(n) setup/maintenance blowing up.

## Kill conditions

**WINS IFF:** evals are written _before_ the work, consistently; KRs are mostly
Clear/Complicated; GitHub Issues is the _actual_ work surface; the gate ships _before_ the spine.

**LOSES IFF:** an eval is reverse-engineered after seeing output (even once); most KRs are fuzzy
with no prior definition of success; the spine ships before one governed cycle; or the gate is
framed as "phase 1" rather than the complete artifact.

## How it runs — two refinements

- **Steer by exception = _discrete_ signals, not a statistical deadband.** A solo operator can't
  generate the volume to calibrate a threshold (the roast's cut), so "exception" means
  **deterministic** events — a KR with no passing eval past its horizon, a stalled/blocked Issue,
  an unlinked PR — surfaced by a weekly `gh` query. Caveat: _no-alarm must mean on-track, not
  detector-asleep_ — keep a liveness/coverage check, or absence-of-exception is meaningless.
- **Cadence is the existing engine; goals make it _directed_.** The estate's throughput (parallel
  `cc-parallel` runs across many repos) already exists — the contribution graph is its _exhaust_.
  Top-down adds direction, not throughput: `goal → plan (goal_id) → cc-parallel fan-out →
  eval-gated PRs → exception-review`. Steer by goals + the objective surfaces (external merges,
  office outcomes), **never by the graph** (steering the graph is how cadence becomes farming).

## Open decisions — the draft index (everything links from here)

| Open item | Tracked in | Decision pending |
|---|---|---|
| Seed `goals.json` | qte77 #143 | which 2–3 OKRs |
| Ship the eval-gate | qte77 #144 | — (the build) |
| `goal_id` on plans | polyforge #79 | — (the link) |
| Persistence cycle + scrape job | qte77 #94 | cadence · mechanism · compression gate |
| Authority-chain terminology | qte77 #145 | is "KERNEL = invariant rules/skills, packaged in claude-code-plugins" right? |
| AI-authorship guardrail | qte77 #146 | hard-never + human-only lane? |
| Promote principles to `AGENTS.md` | — | once the model exits draft |

## Glossary — the BBOM is these five conflated

- **goal** — an OKR; strategic; human-set; in `goals.json` (META); stable ID `G0x`.
- **plan / campaign** — an operational batch of contributions; machine-tracked in `contributions.json`
  (polyforge) or office projects (office-forge); references a `goal_id`.
- **task / story** — a unit of work; a GitHub Issue / ralph `prd.json` `STORY-xxx`.
- **contribution** — a single PR / commit; the _output_.
- **achievement / eval** — _outcome_ verification; **pre-committed** internally, **independently
  verified** for external merges + office outcomes. Done ≠ Achieved.

## Provenance

Output of a multi-turn design discussion plus an adversarial-distillation run (2026-06-28).
Concepts referenced: OKR · OKF (Google Cloud, Apache-2.0) · SHACL/MQO · Cynefin · the estate
compound-learning ladder. The landscape that grounded it lives in
`qte77/ai-agents-research` (`docs/non-cc/semantic-layers-data-catalog-landscape.md`,
`open-knowledge-format-analysis.md`).
