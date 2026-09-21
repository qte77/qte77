---
plan: 004-productization-research.md
status: lane 1 of 3 complete — comparables teardown only
scope: EPHEMERAL working state. Mine into the BRD, then prune.
updated: 2026-08-03
---

# Findings — comparables teardown (backlog #1, sanity-check run)

7 companies, 1 researcher + 1 adversarial source-verifier each (14 agents, 0 errors, ~35 min,
~900k subagent tokens). Run: `wf_a936c3bb-a2c`.

## Reliability of this document — read first

**Zero of seven teardowns came back `RELIABLE`. All seven are `PARTIALLY_RELIABLE`.** The verify
stage caught, among ~324 checked claims:

- a **fabricated verbatim quote** ("Airbyte is still a data movement company") reused four times as
  a load-bearing citation — a gist-accurate paraphrase rendered in quotation marks;
- a **cited source URL that returns 404**, listed in `sources` as if fetched (Devin MultiDevin);
- a **$2,000 billing threshold** attached to a page that does not contain it (real provenance: a
  19-month-old blog post);
- **micro1's OSS posture flatly refuted** — the teardown said "no repos, no SDK, no license"; micro1
  in fact runs `github.com/micro1-research` with an MIT eval harness and CC-BY-4.0 datasets on
  HuggingFace, plus a public vendor leaderboard;
- **Linear's pricing model wrong** — asserted as clean per-seat; actually hybrid seat + prepaid
  workspace-level AI credits;
- **Swarmia's GTM wrong** — asserted "every paid tier is demo-gated"; self-serve checkout is
  documented on a page the teardown itself cited.

Every one is the same failure: a plausible, archetype-shaped prior rendered with the confidence of a
fetched fact. **Conclusion for the rest of the arc: the adversarial verify stage is mandatory, not
optional.** Per-field trust ratings are in the run journal; consult them before quoting any specific
number into the BRD.

## Verdict on the owner-named three

| Company | Good comparable? | What it actually is |
| --- | --- | --- |
| **Airbyte** | **Yes** | Open-core → managed cloud. 600+ connectors, MIT connector layer, ELv2 platform. Paid tier is entirely governance |
| **monaco.com** | **No** (confidence: high) | AI-native sales/revenue platform (CRM replacement) by Sam Blond. Contact-sales only, no OSS, no free tier, forward-deployed onboarding, $85M+ raised |
| **micro1** | **No** (confidence: medium) | Expert-human-labor-backed data + evaluation services sold to frontier AI labs. Contact-sales, no self-serve |

Both rejects still donated one thing each: monaco's wedge is **removing setup labor** ("we set up
your TAM for you on day 1"), which maps onto polyforge's real adoption barrier; micro1's Cortex
supplies P2's **vocabulary** ("define the task, success criteria, rubrics, and scoring approach")
and proves enterprises pay for exactly that framing — as a service.

## The decisive finding: three independent teardowns converge

**P2 sold standalone does not carry a price.** Reached separately, from different evidence:

- **Swarmia** — gives everything away below 10 developers. A priced-in admission the category has no
  value until an org has a coordination problem. Needed a four-module platform + finance-grade
  capitalization reporting to justify EUR 42-55/dev/mo. The honest comparable for a narrow
  governance module is their EUR 4-5/dev/mo AI-adoption module.
- **LangSmith** — gives away 5k traces and the entire code-evaluator surface at $0; charges $39/seat
  only when a second human needs access. "Eval-only was not a business, it was a feature that had to
  be surrounded by a platform and a field sales org funded by venture capital."
- **Linear** — Insights sits inside the $16/user/mo Business tier. The market's revealed price for
  analytics over work items is a seat uplift, not a line item.

Plus micro1's warning: "prove your AI produced outcomes" is a problem **shaped like consulting** —
every step toward richer evaluation is a step toward billing humans.

## But the gap is real, and precisely located

Nobody in the incumbent stack enforces a success criterion **written before work starts**:

- **Swarmia is entirely read-path.** It observes, scores, notifies — nothing in the product blocks
  anything. "OKR" appears **zero times** in their ~395KB docs corpus. Their goal-adjacent primitives
  (Initiatives, working agreements, targets) are advisory and set alongside or after the work —
  precisely the goalpost-moving P2 exists to prevent.
- **Linear's Initiatives** express "the goals and objectives an organization aims to achieve" but
  carry only status, priority, labels, owner, target date, description — **no key results, no
  measurable success criteria**. Insights measures flow (cycle time, lead time), never whether the
  work produced the intended outcome.
- **LangSmith has no timing requirement** — datasets are authored and edited whenever, so
  goalpost-moving is fully permitted. It also measures the wrong object: agent output against a
  dataset, not whether a unit of work achieved a stated goal.

So the qte77 claim that "LangSmith already serves this scope" (`operating-model.md:56`) is **half
right**: LangSmith owns deterministic eval *execution* (code evaluators, pytest/Vitest plugins, a
documented GitHub Actions pattern). P2 must not sell "run a deterministic eval in CI" — commoditized
and free. The defensible sliver is only the **pre-registration ritual plus the issue → KR → status
rollup**.

## Three repositionings the evidence forces

1. **The paid unit cannot be the gate logic.** LangSmith's paid unit is retained state, not logic;
   Airbyte's is governance over a free engine. P2's 50 lines can never be the priced thing — the
   **immutable, timestamped ledger of what was promised before work began**, and the rollup built
   from it, is the only candidate.
2. **Tracker-agnostic, enforcement in CI.** Do NOT position P2 as OKR/goal tracking — that fight is
   against Linear's roadmap and loses ("one field and one query away from being an incumbent
   feature"). The CI gate is the only structurally defensible placement, because a tracker vendor
   will never block a merge on behalf of a competitor's data model. Linear's own Method already
   contains "Set useful goals" as free advice: **the practice is uncontroversial, the enforcement is
   the product.**
3. **P1 must be the execution substrate, not a surface.** Cognition ships **MultiDevin** ("spin up a
   managed Devin for each module", "run this playbook across all services in parallel") as a bundled
   enterprise feature backed by $26B. Linear ships an agent directory including Codex, Devin, Cursor,
   Factory. "Parallel agents across repos" as the product is already a named section of two
   incumbents' homepages. Polyforge's lane is devcontainer lifecycle replay, multi-root workspace
   generation, cross-repo parallelism and validate/security presets — plugging INTO the tracker.

## What Airbyte validates, and what it undercuts

**Validates the structural shape:** free engine, paid governance. Their paid list is entirely
governance — SSO, RBAC, SCIM, field hashing, row filtering, external secrets, OpenTelemetry, data
residency, PrivateLink, SLA. Sold into the "CTO / CIO organization", matching P2's buyer signature.
The free tier is **capability-complete for the core job**; what is withheld is org-scale control.

**Undercuts the specific artifact:** the governance people actually pay for is **access control**,
not outcome-proof. And their wedge (620 connectors) is a **bought** moat — a venture-scale
maintenance liability, not an algorithm. Do not copy a moat whose cost structure you cannot fund.

## Two risks the teardowns raise that the plan did not

1. **Cultural tripwire / consent.** Swarmia states four separate times in its own docs that it must
   not be used for reviews, comp, promotion, discipline or termination — scar tissue from a market
   that punished individual-developer metrics. **A gate that blocks a merge is more coercive than a
   dashboard** and inherits all of that political risk. P2 needs an equally loud non-goal (gates the
   goal/KR issue, never the person) or it gets routed around.
2. **The buyer is slow and expensive to reach.** Swarmia founded 2019, still fronts paid tiers with
   "Get a demo", runs 30-50% first-year partner discounts to buy logos, passed SOC 2 Type 2 + SOC 1.
   The "prove the AI spend" buyer is a procurement-and-security buyer. LangSmith's ICP is the
   engineer with a bottom-up free-tier loop; **P2 has no such loop by construction** — its value is
   telling the buyer's own org it cannot move goalposts. **P1 must be the wedge that earns the right
   to sell P2.**

## Effect on plan 004

- Decide-by-default "comparable set": **drop monaco.com and micro1 from the core set**; retain as
  archetype notes (setup-labor removal; eval-as-service vocabulary + the services trap).
- Backlog #5 (re-run the `operating-model.md:69-77` "What fell" table) now has real inputs — the
  "traceability spine → DISCARD" row survives contact with evidence, but the **pre-commitment
  timing** row does not fall the same way.
- Add to the BRD risk register: the consent/coercion tripwire, and the no-bottom-up-loop problem.

## Sources

Per-agent structured results with source URLs and per-field trust ratings:
`subagents/workflows/wf_a936c3bb-a2c/journal.jsonl` (session-local, ephemeral).
