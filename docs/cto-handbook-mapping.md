# Startup CTO Handbook — mapping to the qte77 operating model

How [Zach Goldberg's *Startup CTO Handbook*][handbook] — a breadth-first reference
for engineering leadership — maps onto the qte77 estate. The handbook is written
for a human CTO running a team; qte77 runs an *agentic* estate where **agents
propose and drive, humans approve and steer**. This note translates the
handbook's themes onto structures we already have ([authority chain][arch],
[`goals.json`](../goals.json), the dev/office loops) and records what we adopt,
defer, or deliberately leave out — it does not reproduce the book.

Audience: humans steering the estate, and agents that read this as context. It is
a map, not a build — concrete work lives in the *Candidate expansions* backlog
and in GitHub Issues.

## How the handbook maps

| Handbook area | Estate home | Status |
| --- | --- | --- |
| People & Culture → leadership model, CEO/OKR alignment, measuring success | This repo: [`goals.json`](../goals.json) (OKRs), the "agents propose, humans decide" stance, a future cockpit consumer | Partial — the *operating-model* half is in scope; the human-team half is not |
| Technology Roadmap | [`architecture.md` → Roadmap][arch] (Now / Next / Later) | Adopted in shape; thin on detail |
| Technical Team Management (tech debt, tech process, developer experience) | Dev loop: [polyforge-orchestrator] + [compound-learning][cl] (learnings → specs) | Partial |
| Tech Architecture ops (DevOps, testing, source control, security & compliance, RCA) | [polyforge-orchestrator] presets (`validate` / `security-all` / `security-pr`) + per-repo CI | Partial — enforced as presets, not documented as practice |
| Business Processes, IT | Office loop: [office-forge-orchestrator] | Deferred — thematic link, no artifact yet |
| People management (hiring, 1:1s, coaching, performance, team makeup) | — | **Out of scope** — this estate has no human reports to manage |

## The slices, concretely

- **Leadership & decision authority.** The handbook's central management question —
  who decides what — is already answered structurally by the [authority chain][arch]
  (META → KERNEL → MECHANISM → STATE → CONSUMERS) and the "agents propose, humans
  decide" rule. The handbook's CTO-archetype framing (Architect / VP-Eng /
  external) reads, for this estate, as *the human operator's role*: set goals,
  approve PRs, steer orchestrators.
- **OKRs & measuring success.** The handbook's "align with the CEO" and "measure
  success" chapters map directly onto [`goals.json`](../goals.json) (intentionally
  a minimal placeholder until a cockpit/dashboard consumer pressure-tests it).
  This is the strongest, most actionable overlap.
- **Roadmap.** [`architecture.md`][arch] already carries a Now/Next/Later roadmap;
  the handbook's roadmap guidance (stakeholder-visible, decision-led) is the
  reference for fleshing it out.
- **Engineering execution** (tech debt, process, DX, DevOps, testing, RCA) belongs
  to the *loops*, not this META repo — polyforge for the dev loop, office-forge for
  the office loop. Those repos carry [light pointers](#cross-repo-pointers) back
  here; the practice itself stays with the mechanism (per the authority chain).
- **Deliberately excluded.** The people-management half of the handbook (hiring,
  1:1s, coaching, performance reviews, team makeup) has no surface in an estate
  whose "team" is agents. Recorded here so the omission is a decision, not a gap.

## Candidate expansions (backlog — not done here)

Per the "mapping note first, then expand" decision, these are deferred — now tracked
in [qte77#134]:

1. Use the handbook's *measuring-success* framing to shape the [`goals.json`](../goals.json)
   OKR schema.
2. Expand the [`architecture.md` Roadmap][arch] using the handbook's roadmap
   structure (decision-led Now/Next/Later with rationale).
3. An *agentic RCA* pattern (what changes when an agent causes the incident?) for
   the dev loop — would live in polyforge, referenced from here.

## Cross-repo pointers

Light pointers back to this note live in the loops and the research corpus, each
scoped to that repo's slice:

- [polyforge-orchestrator] — engineering-execution slice (DevOps / testing / RCA)
- [office-forge-orchestrator] — business-process / IT slice
- [ai-agents-research] — uses the handbook only as a *traditional baseline* to
  contrast against agentic SDLC patterns

## Sources

- [*The Startup CTO's Handbook*, Zach Goldberg][handbook] — open license (copy,
  modify, redistribute with attribution; no commercial resale; share-alike). Cited
  and mapped, not reproduced.

[handbook]: https://github.com/ZachGoldberg/Startup-CTO-Handbook
[arch]: architecture.md
[cl]: ../.claude/rules/compound-learning.md
[polyforge-orchestrator]: https://github.com/qte77/polyforge-orchestrator
[office-forge-orchestrator]: https://github.com/qte77/office-forge-orchestrator
[ai-agents-research]: https://github.com/qte77/ai-agents-research
[qte77#134]: https://github.com/qte77/qte77/issues/134
