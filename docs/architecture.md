# Architecture

How qte77 coordinates 30+ agent-driven repos without drift. For the project
overview, see [the README](../README.md).

## Mental model

Agentic development across 30+ repos drifts without a shared map. This fixes the
feedback loop from learnings back to specs so the system compounds instead of
forgetting.

Read it as: goals at the top feed specs, specs feed builds, builds emit learnings,
and learnings flow back into the next goals.

<img src="../assets/images/mental-model.svg" alt="qte77 Mental Model — clusters, flow, feedback loop" width="100%" />

## Authority chain

Policy, mechanism, and state get confused and duplicated across repos. Naming where
each decision lives prevents the drift and keeps 30+ repos DRY.

- **META** — policy: what we optimize for (rules, principles)
- **KERNEL** — invariants: rules that must hold (core-principles, compound-learning)
- **MECHANISM** — code that enforces rules (skills, hooks, GHA pipelines)
- **STATE** — data the system reads and writes (goals, specs, learnings)
- **CONSUMERS** — where it lands (30+ companion repos)

<details>
  <summary>Diagram: META, KERNEL, MECHANISM, STATE, CONSUMERS</summary>
  <img src="../assets/images/authority-chain.svg" alt="qte77 Authority Chain — META, KERNEL, MECHANISM, STATE, CONSUMERS" width="100%" />
</details>

<details>
  <summary>GHA automation pipeline — the GitHub Actions running across the ecosystem</summary>
  <img src="../assets/images/pipeline-layers.svg" alt="GHA automation pipeline — layers across the ecosystem" width="100%" />
</details>

## What this means concretely

- **Agents** — Claude Code (and compatible LLM coding agents) running per-repo, coordinated by orchestrators in this workspace.
- **Office work** — real workflows where humans and agents collaborate, orchestrated by office-forge and powered by the wider qte77 framework (engines like doc-pipeline-engine handle the heavy lifting).
- **Engines** — reusable components orchestrators compose: [doc-pipeline-engine](https://github.com/qte77/doc-pipeline-engine) (document processing) and [polyfetch-scrape](https://github.com/qte77/polyfetch-scrape) (HTTP scraping with anti-bot fallback).
- **Humans** — approve goals, review PRs, and steer the orchestrators. Agents propose; humans decide.
- **Where to look** — start with [polyforge-orchestrator](https://github.com/qte77/polyforge-orchestrator) for the dev loop or [office-forge-orchestrator](https://github.com/qte77/office-forge-orchestrator) for the office loop.

## Roadmap

- **Now** — GitHub-native (Actions, Issues, PRs); Claude Code agents.
- **Next** — spec-forge methodology landing in [claude-code-plugins](https://github.com/qte77/claude-code-plugins).
- **Later** — runtime portability: air-gapped, BYOM, your stack.

See also: [cto-handbook-mapping.md](cto-handbook-mapping.md) — an external engineering-leadership reference (Startup CTO Handbook) mapped onto this operating model and roadmap.
