<!-- markdownlint-disable-file MD033 - Inline HTML -->
<!-- https://github.com/DavidAnson/markdownlint/blob/v0.25.1/doc/Rules.md#md033 -->

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="brand/images/wordmark_dark.dejavu.png">
    <img src="brand/images/wordmark_light.dejavu.png" alt="qte77" width="35%">
  </picture>
</p>

Turn goals into merged PRs across many repos at once. Agents handle dev and office work end to end, in parallel.

> Without coordination, agentic work across many repos drifts — learnings get lost, work duplicates, goals lose their thread. qte77 keeps the goal → spec → build → learn loop compounding, not forgetting.

## Mental Model

Agentic development across 30+ repos drifts without a shared map. This fixes the feedback loop from learnings back to specs so the system compounds instead of forgetting.

<img src="assets/images/mental-model.svg" alt="qte77 Mental Model — clusters, flow, feedback loop" width="100%" />

### Authority Chain

Policy, mechanism, and state get confused and duplicated across repos. Naming where each decision lives prevents the drift and keeps 30+ repos DRY.

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
- **Office work** — non-code tasks an agent can drive end-to-end (drafting, scheduling, triage, ops glue), handled by the office-forge orchestrator alongside the dev forges.
- **Where to look** — orchestrators (`polyforge-orchestrator`, `office-forge-orchestrator`) and 30+ companion repos live as siblings under [qte77](https://github.com/qte77?tab=repositories).

## Profile

### Topics

- Agentic Software Development, Autonomous Coding
- Self-Evolving Agents, Compound Learning
- Multi-Repo Orchestration, Cross-Repo Issue Sync
- AI Agent Evaluation, MAS Benchmarking
- Goal-Driven Lifecycle Management, OKR Traceability
- Claude Code Plugins, MCP Integrations
- Agent UI (AG-UI/A2UI), Voice (TTS/STT)
- Robotics, Bio-Lab Automation

### Interests

- GitHub Actions, CI/CD Automation
- Inductive Priors, Automatic Differentiation
- Data Centric vs Model Centric
- QML, Barren Plateaus

### Posts

<!-- BLOG-POST-LIST:START -->
- [Agentx Agentbeats Writeup](https://qte77.github.io/agentx-agentbeats-writeup/)
- [AI Agents-eval Comprehensive Analysis](https://qte77.github.io/ai-agents-eval-comprehensive-analysis/)
- [AI Agents-eval Enhancement Recommendations](https://qte77.github.io/ai-agents-eval-enhancement-recommendations/)
- [AI Agents-eval Papers Meta Review](https://qte77.github.io/ai-agents-eval-papers-meta-review/)
<!-- BLOG-POST-LIST:END -->

### Tools

<div style="align: left;">
  <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original.svg" title="Python" alt="Python" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/pytorch/pytorch-original.svg" title="Pytorch" alt="Pytorch" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/jupyter/jupyter-original.svg" title="Jupyter" alt="Jupyter" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/kaggle/kaggle-original.svg" title="Kaggle" alt="Kaggle" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/linux/linux-original.svg" title="Linux" alt="Linux" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/bash/bash-original.svg" title="Bash" alt="Bash" width="40" height="40"/>&nbsp;  
  <img src="https://github.com/devicons/devicon/blob/master/icons/git/git-original.svg#gh-light-mode-only" title="Git" alt="Git" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/git/git-plain.svg#gh-dark-mode-only" title="Git" alt="Git" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/docker/docker-original.svg" title="Docker" alt="Docker" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/kubernetes/kubernetes-plain.svg" title="Kubernetes" alt="Kubernetes" width="40" height="40"/>&nbsp;  
  <img src="https://github.com/devicons/devicon/blob/master/icons/azure/azure-plain.svg#gh-light-mode-only" title="Azure" alt="Azure" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/azure/azure-original.svg#gh-dark-mode-only" title="Azure" alt="Azure" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/amazonwebservices/amazonwebservices-plain-wordmark.svg" title="AWS" alt="AWS" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/googlecloud/googlecloud-plain.svg" title="Google Cloud" alt="Google Cloud" width="40" height="40"/>&nbsp;
  <img src="https://cdn.simpleicons.org/claude/D97757" title="Claude" alt="Claude" width="40" height="40"/>&nbsp;
 </div>

### TODO

- [x] Kaggle Playgrounds
- [x] Kaggle Competitions
- [ ] Codewars Python
- [ ] AdventOfcode

## Lineage

How the current system got here — proof of work, not required reading.

The spec-generation pillar started in [`context-engineering-template-legacy`](https://github.com/qte77/context-engineering-template-legacy) (2025-07-06), where the BRD → PRD → FRD pipeline first took shape. [`RAPID-spec-forge-legacy`](https://github.com/qte77/RAPID-spec-forge-legacy) carried it forward until archived (2026-04-26). The methodology is now landing in [`claude-code-plugins`](https://github.com/qte77/claude-code-plugins) as the `spec-forge` plugin.
