<!-- markdownlint-disable-file MD033 - Inline HTML -->
<!-- https://github.com/DavidAnson/markdownlint/blob/v0.25.1/doc/Rules.md#md033 -->

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="brand/images/wordmark_dark.dejavu.png">
    <img src="brand/images/wordmark_light.dejavu.png" alt="qte77" width="35%">
  </picture>
</p>

**qte77** is a polyrepo orchestration framework for AI coding agents — coordinating Claude Code and compatible agents across the estate so goals, specs, builds, and learnings compound instead of drift. Agents drive it; humans approve and steer, with the North Star a self-evolving, agent-operated GitHub account.

## What

qte77 is the META layer that keeps the agent-driven estate coherent — a shared map so goals, specs, builds, and learnings compound instead of drift.

- **Agents** — Claude Code and compatible LLM coding agents running per-repo, with [ralph-loop](https://github.com/qte77/ralph-loop-cc-tdd-wt-vibe-kanban-template) and its ralphy offspring driving the autonomous build-and-self-improve cycle.
- **Orchestrators** — [polyforge-orchestrator](https://github.com/qte77/polyforge-orchestrator) drives the dev loop; [office-forge-orchestrator](https://github.com/qte77/office-forge-orchestrator) the office loop.
- **Engines** — reusable components orchestrators compose: [doc-pipeline-engine](https://github.com/qte77/doc-pipeline-engine), [polyfetch-scrape](https://github.com/qte77/polyfetch-scrape).
- **Specs → eval → learnings** — spec-forge turns goals into BRD → PRD → FRD; an eval suite scores agent output; [ai-agents-research](https://github.com/qte77/ai-agents-research) distills the learnings back into specs.
- **Humans** — approve goals, review PRs, steer the orchestrators. Agents propose; humans decide.

<img src="assets/images/mental-model.svg" alt="qte77 Mental Model — clusters, flow, feedback loop" width="100%" />

## How

Each repo carries its own quickstart. Start with an orchestrator:

- Dev loop → [polyforge-orchestrator](https://github.com/qte77/polyforge-orchestrator)
- Office loop → [office-forge-orchestrator](https://github.com/qte77/office-forge-orchestrator)
- Engine sample → [doc-pipeline-engine](https://github.com/qte77/doc-pipeline-engine)

Companion repos live as siblings under [qte77](https://github.com/qte77?tab=repositories).

## Why

Agentic development across the estate drifts without a shared map — learnings don't flow back into specs, and the system forgets. qte77 fixes that feedback loop (goals → specs → builds → learnings → goals) so the system compounds instead.

It's a cross-repo coordination layer, not a single-repo agent runner or per-prompt orchestrator. Reach for something else if you're building one agent for one repo, or your loop fits in a single prompt.

## Refs

- [docs/architecture.md](docs/architecture.md) — mental model, authority chain, GHA pipeline, roadmap
- [docs/doc-structure.md](docs/doc-structure.md) — the README + doc-hierarchy contract for the estate
- [CONTRIBUTING.md](CONTRIBUTING.md) · [AGENTS.md](AGENTS.md) — how to work here

## License

Apache-2.0 — see [LICENSE](LICENSE).

## Tools

<div><!--
  --><img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original.svg" title="Python" alt="Python" width="32" height="32"/><!--
  --><img src="assets/images/icons/uv.svg" title="uv" alt="uv" width="32" height="32"/><!--
  --><img src="https://github.com/devicons/devicon/blob/master/icons/typescript/typescript-original.svg" title="TypeScript" alt="TypeScript" width="32" height="32"/><!--
  --><picture><source media="(prefers-color-scheme: dark)" srcset="assets/images/icons/markdown-dark.svg"><img src="assets/images/icons/markdown-light.svg" title="Markdown" alt="Markdown" width="32" height="32"/></picture><!--
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
  --><picture><source media="(prefers-color-scheme: dark)" srcset="assets/images/icons/mcp-dark.svg"><img src="assets/images/icons/mcp-light.svg" title="Model Context Protocol" alt="Model Context Protocol" width="32" height="32"/></picture><!--
--></div>

## Posts

<!-- BLOG-POST-LIST:START -->
- [An Open Agentic Coding Harness — the Loop, the Plugins, the Senses, the Eval](https://qte77.github.io/open-agentic-coding-harness/)
- [Building a Trustworthy Agent Loop for a Physical Lab](https://qte77.github.io/open-self-driving-lab-agent-loop/)
- [A $150 Pipetting Robot from a Stock 3D Printer](https://qte77.github.io/pipettebot-sub-150-pipetting-robot/)
- [GraphJudge — Measuring How Agents Collaborate](https://qte77.github.io/agentx-agentbeats-writeup/)
<!-- BLOG-POST-LIST:END -->

## Profile

More: [Topics, Interests, TODO](PROFILE.md).

## Lineage

How the current system got here — proof of work, not required reading.

[`context-engineering-template-legacy`](https://github.com/qte77/context-engineering-template-legacy) (first commit 2025-07-07) coined the BRD → PRD → FRD pipeline and the "CABIO" vision. The work was carried forward in **RAPID-spec-forge** (Requirements-to-Agent Pipeline & Implementation Driver; formerly CABIO-test) from 2026-02-26, archived 2026-04-26 as [`RAPID-spec-forge-legacy`](https://github.com/qte77/RAPID-spec-forge-legacy). Its parts were then decomposed under qte77 — now the META layer for the estate:

- **Spec methodology** → the spec-forge plugin landing in [claude-code-plugins](https://github.com/qte77/claude-code-plugins) (2026-02-22)
- **Implementation driver** → [ralph-loop](https://github.com/qte77/ralph-loop-cc-tdd-wt-vibe-kanban-template) + ralphy offspring — the autonomous build & self-improve cycle
- **Dev / office cockpit** → [polyforge-orchestrator](https://github.com/qte77/polyforge-orchestrator) (2026-03-17) · [office-forge-orchestrator](https://github.com/qte77/office-forge-orchestrator) (2026-03-27)
- **Doc-search + memory** → a planned doc-search + memory plugin
