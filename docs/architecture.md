# Architecture

How qte77 coordinates the agent-driven estate without drift. For the project
overview, see [the README](../README.md).

## Mental model

Agentic development across the estate drifts without a shared map. This fixes the
feedback loop from learnings back to specs so the system compounds instead of
forgetting.

Read it as: goals at the top feed specs, specs feed builds, builds emit learnings,
and learnings flow back into the next goals.

<img src="../assets/images/mental-model.svg" alt="qte77 Mental Model — clusters, flow, feedback loop" width="100%" />

## Authority chain

Policy, mechanism, and state get confused and duplicated across repos. Naming where
each decision lives prevents the drift and keeps the estate DRY.

- **META** — policy + strategic intent, human-authored: `AGENTS.md` rules and `goals.json` OKRs. Lives in `qte77/qte77`; records decisions, runs no mechanism.
- **KERNEL** — the invariant, reusable capability package: rules + skills + plugins, canonically in [claude-code-plugins](https://github.com/qte77/claude-code-plugins).
- **MECHANISM** — what runs the kernel across the estate: the orchestrators ([polyforge](https://github.com/qte77/polyforge-orchestrator), [office-forge](https://github.com/qte77/office-forge-orchestrator)) plus the GHA automation.
- **STATE** — machine-derived data the system reads and writes: GitHub Issues (task SOT), `contributions.json`, `ontology.json`.
- **CONSUMERS** — where agents land the work: the sibling repos.

<details>
  <summary>Diagram: META, KERNEL, MECHANISM, STATE, CONSUMERS</summary>
  <img src="../assets/images/authority-chain.svg" alt="qte77 Authority Chain — META, KERNEL, MECHANISM, STATE, CONSUMERS" width="100%" />
</details>

<details>
  <summary>GHA automation pipeline — the GitHub Actions running across the ecosystem</summary>
  <img src="../assets/images/pipeline-layers.svg" alt="GHA automation pipeline — layers across the ecosystem" width="100%" />
</details>

## What this means concretely

- **Office work** — real workflows where humans and agents collaborate, orchestrated by office-forge and powered by the wider qte77 estate (engines like [doc-pipeline-engine](https://github.com/qte77/doc-pipeline-engine) handle the heavy lifting).

The agents, engines, and humans that make up the estate — and where to start — are covered in the [README](../README.md); this doc focuses on how it stays coherent.

## Roadmap

- **Now** — GitHub-native (Actions, Issues, PRs); Claude Code agents.
- **Next** — spec-forge methodology landing in [claude-code-plugins](https://github.com/qte77/claude-code-plugins).
- **Later** — runtime portability: air-gapped, BYOM, your stack.

See also: [cto-handbook-mapping.md](cto-handbook-mapping.md) — an external engineering-leadership reference (Startup CTO Handbook) mapped onto this operating model and roadmap.

See also: [operating-model.md](operating-model.md) — the steer-top / trace-bottom operating-model concept, its adversarial de-risking, and the decision to ship a single eval-before-work gate rather than the full spine.
