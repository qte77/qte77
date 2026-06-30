---
title: Agent Learning Documentation
description: Non-obvious patterns that prevent repeated mistakes across sprints
---

## Template

- **Context**: When/where this applies
- **Problem**: What issue this solves
- **Solution**: Implementation approach
- **Example**: Working code
- **References**: Related files

## Learned Patterns

### Calibrate adversarial / moat red-teams to the actual purpose

- **Context**: Running `/adversarial-distillation` (or any moat / defensibility / "is this sellable" red-team) on **internal or personal** tooling.
- **Problem**: The method optimises for **commercial defensibility** — its "no moat", "reinventable → discard", "a hyperscaler will build it", "TAM too small" cuts are irrelevant off-commercial and will wrongly kill worth-building work.
- **Solution**: Split the verdict — **frame-dependent** cuts (moat / TAM / competition) → discard when not selling; **frame-independent** cuts (logic, ROI, rot, Goodhart, cold-start) → keep. Re-read through the real purpose first. "Showcase not sell" voids the moat cuts; the engineering/economics cuts survive.
- **References**: `docs/operating-model.md` (Calibration section).

### Persistence: commit-then-cache + scrape-then-compress (git is the only durable SOT)

- **Context**: Preserving session/agent knowledge across sessions in an agentic estate.
- **Problem**: `~/.claude/.../memory/` is **local container disk** — disk break / codespace delete / rebuild loses it. Nothing critical can live only there.
- **Solution**: Durable SOT = **git-committed + pushed** (repo docs, GitHub Issues, this file, `.claude/rules/`). Memory is a *regeneratable cache*. Periodically **scrape** the ephemeral layer for learnings and **compress** (distil, don't dump — compression is the anti-graveyard quality gate), then commit. Commit-as-you-go during a session + a backstop scrape.
- **References**: `qte77/qte77#94`.
