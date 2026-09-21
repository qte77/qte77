# Agent reliability research

A research line across several sibling repos: measuring whether an agent — or the site/API
it acts on — can actually be trusted, not just whether a task finished.

- [`RDI-AgentBeats-MAS-GraphJudge`](https://github.com/qte77/RDI-AgentBeats-MAS-GraphJudge) —
  "measure how, not just whether": graph-based multi-agent coordination quality (NetworkX
  structural metrics + LLM-as-judge).
- [`RDI-AgentBeats-TestBehaveAlign`](https://github.com/qte77/RDI-AgentBeats-TestBehaveAlign) —
  "measure test quality, not just code correctness": deterministic test-generation scoring
  (mutation testing + fault detection, no LLM-as-judge).
- [`agent-readiness-kit`](https://github.com/qte77/agent-readiness-kit) — scans qte77-owned
  properties for agent-native readiness (Discovery/Content/Trust/Execution/A2A/Identity) and
  produces remediation, cross-referenced against [ora.ai](https://ora.ai)'s scoring.
- [`cc-recursive-team-mode`](https://github.com/qte77/cc-recursive-team-mode) — recursive
  Claude Code subprocess spawning; solo-vs-teams cost/reliability A/B benchmarking.
- [`coding-harness-eval`](https://github.com/qte77/coding-harness-eval) — hands-off coding
  agent comparison harness.
- [`multi-tasking-quality-benchmark`](https://github.com/qte77/multi-tasking-quality-benchmark) —
  correlates WakaTime coding activity with code quality metrics.
- [`ai-agents-research`](https://github.com/qte77/ai-agents-research) — field research and
  feature analysis for AI coding agents (sandboxing, orchestration, plugins, SDLC patterns).
