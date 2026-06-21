# Contributing

For agent behavioral rules see [AGENTS.md](AGENTS.md). For brand tooling specifics see [brand/README.md](brand/README.md).

## Documentation hierarchy

One audience per file — reference, don't duplicate (the estate contract is [docs/doc-structure.md](docs/doc-structure.md)):

| File | Audience | Owns |
| --- | --- | --- |
| [README.md](README.md) | users / evaluators | what this is, why, how — the front door |
| CONTRIBUTING.md (this file) | contributors | workflow, commands, conventions, releasing |
| [AGENTS.md](AGENTS.md) | AI agents | behavioural rules, decision frameworks (`CLAUDE.md` loads the same instructions) |
| [CHANGELOG.md](CHANGELOG.md) | everyone | notable changes by version |

## Scope

GitHub profile repository. Two surfaces:

- `brand/` — visual identity (palette, SVGs, avatar PNGs) and the Python tooling that produces them
- `docs/` — supporting documentation (image theming, gh-endpoints catalog)

No application code, no test suite. Python scripts use PEP 723 inline deps via `uv run`.

## Commands

```bash
make -C brand help               # brand tooling targets
markdownlint $(git ls-files '*.md')
lychee $(git ls-files '*.md')    # add --offline to skip network
```

## Conventional Commits

`feat`, `fix`, `docs`, `chore`, `refactor`, `experiment`. Optional scope: `feat(brand): ...`. PR titles match.

## Branches

- `feat/<topic>`, `fix/<topic>`, `docs/<topic>`, `chore/<topic>`
- `experiment/<topic>` for brittle work that may not merge

Squash-merge is default. Force-push only with `--force-with-lease`, never to `main`.

## CHANGELOG

Add an entry under `[Unreleased]` for any change that's visible to consumers (new asset, new tooling, fixed output, security hardening). Skip for typos, formatting, or internal refactors with no user-facing diff. Entries lead with the file path:

```text
- `brand/scripts/foo.py`: <change>
```

## Pre-merge

1. `markdownlint $(git ls-files '*.md')` clean
2. `lychee --offline $(git ls-files '*.md')` clean
3. CHANGELOG `[Unreleased]` updated
4. Conventional Commits title
