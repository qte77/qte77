<!-- markdownlint-disable-file MD033 - Inline HTML -->
<!-- https://github.com/DavidAnson/markdownlint/blob/v0.25.1/doc/Rules.md#md033 -->

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="brand/images/wordmark_dark.dejavu.png">
    <img src="brand/images/wordmark_light.dejavu.png" alt="qte77" width="35%">
  </picture>
</p>

**qte77** is a governed operating model for an agentic estate. Goals steer top-down, evals trace achievement bottom-up, all built in the open. Not a demo — a model to read, critique, and lift.

## What

<img src="assets/images/governed-loop.svg" alt="qte77 — the governed loop: GOALS (goals.json OKRs, each KR a pre-committed eval) steer down through ENFORCE + TRACE (the governance spine — eval-gate enforces, goal_id links, rollup proves %) to CODE (the cadence engine — agents open PRs that close KRs); achievement traces back up." width="100%" />

- **A governed loop:** intent flows down and proof flows up, as the diagram shows.
- **Dev loop:** [polyforge-orchestrator](https://github.com/qte77/polyforge-orchestrator).
- **Office loop:** [office-forge-orchestrator](https://github.com/qte77/office-forge-orchestrator).
- **Reusable engines:** [doc-pipeline-engine](https://github.com/qte77/doc-pipeline-engine) and [polyfetch-scrape](https://github.com/qte77/polyfetch-scrape).
- **Shared kernel:** [claude-code-plugins](https://github.com/qte77/claude-code-plugins), the rules, skills and plugins every session loads; [qte77/.github](https://github.com/qte77/.github) holds the org defaults and reusable CI workflows.
- **Build cycle:** [ralph-loop](https://github.com/qte77/ralph-loop-cc-tdd-wt-vibe-kanban-template) drives the autonomous build-and-improve cycle.
- **Humans steer:** agents propose; humans approve and steer. How responsibility maps across repos: the [authority chain](docs/architecture.md).

## How

Two ways in:

- **Run it** — start with an orchestrator: [polyforge](https://github.com/qte77/polyforge-orchestrator) (dev) or [office-forge](https://github.com/qte77/office-forge-orchestrator) (office); [doc-pipeline-engine](https://github.com/qte77/doc-pipeline-engine) is a sample engine.
- **Read it** — the [operating model](docs/operating-model.md) (the design plus its adversarial de-risking) and the [goal loop](docs/goals.md) (how intent becomes enforced and traced). Lift what's useful.

Companion repos live as siblings under [qte77](https://github.com/qte77?tab=repositories).

## Why

Run agents across many repos and it drifts into chaos — no shared goals, no traceability, no proof that "done" means "achieved." qte77 is the governance for exactly that: goals steer the work, a pre-committed eval gates every key result, and achievement traces back up — so the estate compounds instead of forgetting.

Built in the open, honestly: the rails ship before the goals, and what's live versus still dormant is shown as it is — see [STATUS.md](STATUS.md). It's a cross-repo operating model, not a single-repo agent runner; reach for something else if your loop fits in one repo or one prompt.

## Refs

- [Operating model](docs/operating-model.md)
- [Goal loop](docs/goals.md)
- [Architecture](docs/architecture.md)
- [Doc-structure contract](docs/doc-structure.md) · [Unattended execution](docs/unattended-execution.md)
- [Contributing](CONTRIBUTING.md) · [Agent instructions](AGENTS.md)
- [Profile](PROFILE.md) · [Lineage](docs/lineage.md) · [Hackathons](docs/hackathons.md) · [Agent reliability](docs/agent-reliability.md)
- [Agent-native surface](https://qte77.github.io) — where this estate is machine-discoverable ([why not here](brand/ui-kit/DISCOVERABILITY.md))

## License

Apache-2.0 — see [LICENSE](LICENSE).

## Tools

<div><!--
  --><img src="assets/images/icons/python.svg" title="Python" alt="Python" width="32" height="32"/><!--
  --><picture><source media="(prefers-color-scheme: dark)" srcset="assets/images/icons/astral-dark.svg"><img src="assets/images/icons/astral-light.svg" title="Astral (uv · ruff)" alt="Astral" width="32" height="32"/></picture><!--
  --><img src="assets/images/icons/typescript.svg" title="TypeScript" alt="TypeScript" width="32" height="32"/><!--
  --><img src="assets/images/icons/nodejs.svg" title="Node.js" alt="Node.js" width="32" height="32"/><!--
  --><picture><source media="(prefers-color-scheme: dark)" srcset="assets/images/icons/markdown-dark.svg"><img src="assets/images/icons/markdown-light.svg" title="Markdown" alt="Markdown" width="32" height="32"/></picture><!--
  --><img src="assets/images/icons/linux.svg" title="Linux" alt="Linux" width="32" height="32"/><!--
  --><img src="assets/images/icons/bash.svg" title="Bash" alt="Bash" width="32" height="32"/><!--
  --><picture><source media="(prefers-color-scheme: dark)" srcset="assets/images/icons/git-dark.svg"><img src="assets/images/icons/git-light.svg" title="Git" alt="Git" width="32" height="32"/></picture><!--
  --><img src="assets/images/icons/githubactions.svg" title="GitHub Actions" alt="GitHub Actions" width="32" height="32"/><!--
  --><img src="assets/images/icons/docker.svg" title="Docker" alt="Docker" width="32" height="32"/><!--
  --><picture><source media="(prefers-color-scheme: dark)" srcset="assets/images/icons/devcontainers-dark.svg"><img src="assets/images/icons/devcontainers-light.svg" title="Dev Containers" alt="Dev Containers" width="32" height="32"/></picture><!--
  --><picture><source media="(prefers-color-scheme: dark)" srcset="assets/images/icons/azure-dark.svg"><img src="assets/images/icons/azure-light.svg" title="Azure" alt="Azure" width="32" height="32"/></picture><!--
  --><img src="assets/images/icons/aws.svg" title="AWS" alt="AWS" width="32" height="32"/><!--
  --><img src="assets/images/icons/googlecloud.svg" title="Google Cloud" alt="Google Cloud" width="32" height="32"/><!--
  --><picture><source media="(prefers-color-scheme: dark)" srcset="assets/images/icons/ros-dark.svg"><img src="assets/images/icons/ros-light.svg" title="ROS" alt="ROS" width="32" height="32"/></picture><!--
  --><img src="assets/images/icons/huggingface.svg" title="Hugging Face" alt="Hugging Face" width="32" height="32"/><!--
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
