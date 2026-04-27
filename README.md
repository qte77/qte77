<!-- markdownlint-disable-file MD033 - Inline HTML -->
<!-- https://github.com/DavidAnson/markdownlint/blob/v0.25.1/doc/Rules.md#md033 -->

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="brand/images/wordmark_dark.dejavu.png">
    <img src="brand/images/wordmark_light.dejavu.png" alt="qte77" width="35%">
  </picture>
</p>

**qte77** hosts a framework for compounding agentic work — keeping goals, specs, builds, and learnings in one feedback loop instead of drifting. Agents drive it; humans approve and steer.

Proof: [30+ repos](https://github.com/qte77?tab=repositories) running on it; this README itself was shaped by agent PRs (e.g. [#83](https://github.com/qte77/qte77/pull/83), [#84](https://github.com/qte77/qte77/pull/84)).

## Mental Model

Agentic development across 30+ repos drifts without a shared map. This fixes the feedback loop from learnings back to specs so the system compounds instead of forgetting.

Read it as: goals at the top feed specs, specs feed builds, builds emit learnings, and learnings flow back into the next goals.

<img src="assets/images/mental-model.svg" alt="qte77 Mental Model — clusters, flow, feedback loop" width="100%" />

### Authority Chain

Policy, mechanism, and state get confused and duplicated across repos. Naming where each decision lives prevents the drift and keeps 30+ repos DRY.

- **META** — policy: what we optimize for (rules, principles)
- **KERNEL** — invariants: rules that must hold (core-principles, compound-learning)
- **MECHANISM** — code that enforces rules (skills, hooks, GHA pipelines)
- **STATE** — data the system reads and writes (goals, specs, learnings)
- **CONSUMERS** — where it lands (30+ companion repos)

<details>
  <summary>Diagram: META, KERNEL, MECHANISM, STATE, CONSUMERS</summary>
  <img src="assets/images/authority-chain.svg" alt="qte77 Authority Chain — META, KERNEL, MECHANISM, STATE, CONSUMERS" width="100%" />
</details>

<details>
  <summary>GHA automation pipeline — the GitHub Actions running across the ecosystem</summary>
  <img src="assets/images/pipeline-layers.svg" alt="GHA automation pipeline — layers across the ecosystem" width="100%" />
</details>

### What this means concretely

- **Agents** — Claude Code (and compatible LLM coding agents) running per-repo, coordinated by orchestrators in this workspace.
- **Office work** — real workflows where humans and agents collaborate, orchestrated by office-forge and powered by the wider qte77 framework (engines like doc-pipeline-engine handle the heavy lifting).
- **Engines** — reusable components orchestrators compose: [doc-pipeline-engine](https://github.com/qte77/doc-pipeline-engine) (document processing) and [polyfetch-scrape](https://github.com/qte77/polyfetch-scrape) (HTTP scraping with anti-bot fallback).
- **Humans** — approve goals, review PRs, and steer the orchestrators. Agents propose; humans decide.
- **Where to look** — start with [polyforge-orchestrator](https://github.com/qte77/polyforge-orchestrator) for the dev loop or [office-forge-orchestrator](https://github.com/qte77/office-forge-orchestrator) for the office loop. 30+ companion repos live as siblings under [qte77](https://github.com/qte77?tab=repositories).

## Get started

- Dev loop → [polyforge-orchestrator](https://github.com/qte77/polyforge-orchestrator)
- Office loop → [office-forge-orchestrator](https://github.com/qte77/office-forge-orchestrator)
- Engine sample → [doc-pipeline-engine](https://github.com/qte77/doc-pipeline-engine)

Each repo carries its own quickstart.

## Roadmap

- **Now** — GitHub-native (Actions, Issues, PRs); Claude Code agents.
- **Next** — spec-forge methodology landing in [claude-code-plugins](https://github.com/qte77/claude-code-plugins).
- **Later** — runtime portability: air-gapped, BYOM, your stack.

## Positioning

qte77 is a cross-repo coordination layer, not a single-repo agent runner or per-prompt orchestrator. It assumes you already have agents (Claude Code, etc.) and need them to stop drifting across many repos.

Reach for something else if you're building one agent for one repo, or your loop fits in a single prompt.

## Lineage

How the current system got here — proof of work, not required reading.

The spec-generation work started in [`context-engineering-template-legacy`](https://github.com/qte77/context-engineering-template-legacy) (2025-07-06), where the BRD → PRD → FRD pipeline first took shape. [`RAPID-spec-forge-legacy`](https://github.com/qte77/RAPID-spec-forge-legacy) carried it forward until archived (2026-04-26).

## Tools

<div><!--
  --><img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original.svg" title="Python" alt="Python" width="32" height="32"/><!--
  --><img src="https://github.com/devicons/devicon/blob/master/icons/typescript/typescript-original.svg" title="TypeScript" alt="TypeScript" width="32" height="32"/><!--
  --><img src="https://github.com/devicons/devicon/blob/master/icons/linux/linux-original.svg" title="Linux" alt="Linux" width="32" height="32"/><!--
  --><img src="https://github.com/devicons/devicon/blob/master/icons/bash/bash-original.svg" title="Bash" alt="Bash" width="32" height="32"/><!--
  --><picture><source media="(prefers-color-scheme: dark)" srcset="https://github.com/devicons/devicon/blob/master/icons/git/git-plain.svg"><img src="https://github.com/devicons/devicon/blob/master/icons/git/git-original.svg" title="Git" alt="Git" width="32" height="32"/></picture><!--
  --><img src="https://github.com/devicons/devicon/blob/master/icons/githubactions/githubactions-original.svg" title="GitHub Actions" alt="GitHub Actions" width="32" height="32"/><!--
  --><img src="https://github.com/devicons/devicon/blob/master/icons/docker/docker-original.svg" title="Docker" alt="Docker" width="32" height="32"/><!--
  --><picture><source media="(prefers-color-scheme: dark)" srcset="assets/images/icons/devcontainers-dark.svg"><img src="assets/images/icons/devcontainers-light.svg" title="Dev Containers" alt="Dev Containers" width="32" height="32"/></picture><!--
  --><picture><source media="(prefers-color-scheme: dark)" srcset="https://github.com/devicons/devicon/blob/master/icons/azure/azure-original.svg"><img src="https://github.com/devicons/devicon/blob/master/icons/azure/azure-plain.svg" title="Azure" alt="Azure" width="32" height="32"/></picture><!--
  --><img src="https://github.com/devicons/devicon/blob/master/icons/amazonwebservices/amazonwebservices-plain-wordmark.svg" title="AWS" alt="AWS" width="32" height="32"/><!--
  --><img src="https://github.com/devicons/devicon/blob/master/icons/googlecloud/googlecloud-plain.svg" title="Google Cloud" alt="Google Cloud" width="32" height="32"/><!--
  --><picture><source media="(prefers-color-scheme: dark)" srcset="assets/images/icons/ros-dark.svg"><img src="assets/images/icons/ros-light.svg" title="ROS" alt="ROS" width="32" height="32"/></picture><!--
  --><img src="assets/images/icons/huggingface.svg" title="Hugging Face" alt="Hugging Face" width="32" height="32"/><!--
  --><picture><source media="(prefers-color-scheme: dark)" srcset="assets/images/icons/gh-models-dark.svg"><img src="assets/images/icons/gh-models-light.svg" title="GitHub Models" alt="GitHub Models" width="32" height="32"/></picture><!--
  --><img src="assets/images/icons/claude.svg" title="Claude" alt="Claude" width="32" height="32"/><!--
--></div>

## Posts

<!-- BLOG-POST-LIST:START -->
- [Agentx Agentbeats Writeup](https://qte77.github.io/agentx-agentbeats-writeup/)
- [AI Agents-eval Comprehensive Analysis](https://qte77.github.io/ai-agents-eval-comprehensive-analysis/)
- [AI Agents-eval Enhancement Recommendations](https://qte77.github.io/ai-agents-eval-enhancement-recommendations/)
- [AI Agents-eval Papers Meta Review](https://qte77.github.io/ai-agents-eval-papers-meta-review/)
<!-- BLOG-POST-LIST:END -->

## Profile

More: [Topics, Interests, TODO](PROFILE.md).
