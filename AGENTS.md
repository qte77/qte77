# Agent Instructions

**Behavioral rules, compliance requirements, and decision frameworks for AI coding
agents.** For technical workflows, lint/commit conventions, and the documentation
hierarchy, see [CONTRIBUTING.md](CONTRIBUTING.md). For project overview, see
[README.md](README.md). For brand tooling specifics, see
[brand/README.md](brand/README.md).

**External References:**

- @CONTRIBUTING.md - Workflows, coding standards, doc hygiene
- @AGENT_REQUESTS.md - Escalation and human collaboration
- @AGENT_LEARNINGS.md - Pattern discovery and knowledge sharing
- @CHANGELOG.md - Notable changes by version

## Claude Code Infrastructure

**Rules** (`.claude/rules/`): Session-loaded constraints (always active)
**Skills** (`.claude/skills/`): Modular capabilities with progressive disclosure

## Core Rules & AI Behavior

- Follow SDLC principles: maintainability, modularity, reusability, adaptability
- **Never assume missing context** - Ask questions if uncertain about requirements
- **Never hallucinate libraries** - Only use packages verified in project dependencies
- **Always confirm file paths exist** before referencing in code or tests
- **Never delete existing code** unless explicitly instructed or documented refactoring
- **Document new patterns** in AGENT_LEARNINGS.md (concise, laser-focused, streamlined)
- **Request human feedback** in AGENT_REQUESTS.md (concise, laser-focused, streamlined)

## Decision Framework

**Priority Order:** User instructions > AGENTS.md compliance > Documentation
hierarchy > Project patterns > General best practices

**Anti-Scope-Creep Rules:**

- **NEVER implement features without requirement validation**
- **Always validate implementation decisions against project scope boundaries**

**Anti-Redundancy Rules:**

- **NEVER duplicate information across documents** - reference authoritative sources
- **Update authoritative document, then remove duplicates elsewhere**

**When to Escalate to AGENT_REQUESTS.md:**

- User instructions conflict with safety/security practices
- AGENTS.md rules contradict each other
- Required information completely missing
- Actions would significantly change project architecture

## AR vs GitHub Issue

`AGENT_REQUESTS.md` is for **ephemeral session-level escalations only** —
something an agent surfaces *during* a session that needs human input *now* or
*this session*. Once resolved (typically within a session or two), the entry
is removed.

Anything that will outlive the current session — long-running decisions,
multi-step migrations, blockers requiring multiple discussions — must
graduate to a **GitHub Issue**. Per the task-tracking authority chain,
GitHub Issues are the source of truth for persistent state.

If an AR entry persists beyond a few sessions, file it as an Issue and
remove the AR entry.

## Task-tracking authority

Workspace state lives across four artifacts with distinct, non-overlapping
scopes. The canonical entity model is
[`polyforge-orchestrator/config/ontology.json`][ontology] — this section
quotes it; do not redefine the model here.

| Artifact | Scope | Writers |
| -------- | ----- | ------- |
| **GitHub Issues** | Canonical task SOT (per `ontology.json`: `entity: issue`, `persisted: true`) | human, agent, GHA |
| **[`contributions.json`][contrib]** | Polyforge cross-repo plan execution state — `--resume` source, survives container rebuilds | machine-written by `cc-parallel.sh` |
| **[`.github-private-project-tracker`][tracker]** | Per-repo tactical issue mirror; bidirectional sync via [`gha-cross-repo-issue-sync`][sync] (close/reopen/labels propagate) | tracker GHA + maintainers |
| **`goals.json`** (this repo) | Workspace OKRs / strategic goals | humans only |

**Rule:** GitHub Issues are the SOT for tasks. `contributions.json` and
the tracker are derived state — never write tasks to them without a
corresponding Issue. `goals.json` is meta to all of these (it describes
*why* tasks exist, not which tasks).

**DRY:** the entity definitions, storage, and writer/reader matrix live
in `ontology.json`. Link out, do not duplicate. If the model changes,
update the ontology in polyforge — this section reflects it.

[ontology]: https://github.com/qte77/polyforge-orchestrator/blob/main/config/ontology.json
[contrib]: https://github.com/qte77/polyforge-orchestrator/blob/main/config/contributions.json
[tracker]: https://github.com/qte77/.github-private-project-tracker
[sync]: https://github.com/qte77/gha-cross-repo-issue-sync

## Cross-repo agent hygiene

Workspace-level policy for agents operating across multiple repos. Mechanism
(CLI flags, scripts, recipes) lives in
[polyforge-orchestrator/docs/context-hygiene.md][polyforge-context-hygiene] —
this section is policy only, per the META → MECHANISM authority split.

![qte77 authority chain](assets/images/authority-chain.svg)

**Plumbing vs content editing:**

- **Plumbing** (PRs, branches, merges, status checks, metadata) — use CLI-only
  tools (`gh`, `git`). Never `Read` a sibling repo's file from the
  orchestrator session; the implicit `CLAUDE.md` cascade fires on `Read`, not
  on shell ops, and cross-repo reads silently pull in the sibling's rules.
- **Content editing** (changes to a sibling repo's files) — open a dedicated
  Claude Code session inside the target repo, **or** delegate to a subagent in
  a nested worktree. Never edit child-repo files directly from the parent
  orchestrator session.

**Cascade discipline:**

Never run with implicit `CLAUDE.md` cascade enabled when orchestrating across
repos. Use polyforge presets or `--bare` to dial cascade behavior explicitly.
The mechanism doc carries the flag tables, recipes, and the
`--bare` dial-not-a-switch model.

**DRY:** do not inline flag tables, scripts, or recipes here. Mechanism stays
in polyforge per the authority chain.

[polyforge-context-hygiene]: https://github.com/qte77/polyforge-orchestrator/blob/main/docs/context-hygiene.md

## Agent Neutrality Requirements

**ALL AI AGENTS MUST MAINTAIN STRICT NEUTRALITY AND REQUIREMENT-DRIVEN DESIGN:**

1. **Extract requirements from specified documents ONLY**
   - Read provided task descriptions or reference materials
   - Do NOT make assumptions about unstated requirements
   - Do NOT add functionality not explicitly requested

2. **Request clarification for ambiguous scope**
   - If task boundaries are unclear, ASK for clarification
   - If complexity level is not specified, ASK for target complexity
   - Do NOT assume scope or make architectural decisions without validation

3. **Design to stated requirements exactly**
   - Match the complexity level requested
   - Follow "minimal," "streamlined," or "focused" guidance literally
   - Do NOT over-engineer solutions beyond stated needs

## Compliance Requirements

1. **Command Execution**: Use project make recipes or standard tooling
2. **Quality Validation**: Run validation before task completion; fix ALL issues
3. **Coding Style**: Follow existing project patterns and conventions
4. **Documentation Updates**: Update docs when introducing new patterns
5. **Testing**: Create tests for new functionality
6. **Code Standards**: Use absolute imports, add `# Reason:` comments for complex logic

## Quality Thresholds

**Before starting any task, ensure:**

- **Context**: 8/10 - Understand requirements, codebase patterns, dependencies
- **Clarity**: 7/10 - Clear implementation path and expected outcomes
- **Alignment**: 8/10 - Follows project patterns and architectural decisions
- **Success**: 7/10 - Confident in completing task correctly

### Below Threshold Action

Gather more context or escalate to AGENT_REQUESTS.md

## Agent Quick Reference

**Pre-Task:**

- Read AGENTS.md and the README of the surface you're touching (brand, docs, etc.)
- Verify quality thresholds met

**During Task:**

- Use project commands (document deviations)
- Follow existing patterns and conventions
- Update documentation when learning patterns

**Post-Task:**

- Run validation - must pass all checks (code tasks only)
- Update CHANGELOG.md for non-trivial changes
- Document new patterns in AGENT_LEARNINGS.md (concise, laser-focused, streamlined)
- Escalate to AGENT_REQUESTS.md if blocked
