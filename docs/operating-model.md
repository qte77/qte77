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

**What fell:**

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

## The decision

1. **Build:** `kr-eval-gate.yml` (~50 lines) — _no eval block on the KR ⇒ no merge_ — as the
   **complete useful artifact**, NOT "phase 1 of the operating model" (framing it as phase 1 is
   itself a kill condition).
2. **Do not build (yet):** the ontology spine, OKF bundles, SHACL/MQO, steer-by-exception
   alerting, multi-tenant / cockpit. Use GitHub's native Issue↔PR graph for traceability and
   LangSmith/Braintrust for evals; accept their limits.
3. **Record + revisit:** this doc is the decision record — compound-learning applied to itself.

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

## Provenance

Output of a multi-turn design discussion plus an adversarial-distillation run (2026-06-28).
Concepts referenced: OKR · OKF (Google Cloud, Apache-2.0) · SHACL/MQO · Cynefin · the estate
compound-learning ladder. The landscape that grounded it lives in
`qte77/ai-agents-research` (`docs/non-cc/semantic-layers-data-catalog-landscape.md`,
`open-knowledge-format-analysis.md`).
