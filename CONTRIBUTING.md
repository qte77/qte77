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

No application code. Python scripts use PEP 723 inline deps via `uv run`. A small stdlib
`unittest` suite in `tests/` (brand contrast, goal rollup) runs in CI (`tests.yml`); the brand-contrast test needs PyYAML (present on the GitHub runner).

## Commands

```bash
make -C brand help               # brand tooling targets
markdownlint $(git ls-files '*.md')
lychee $(git ls-files '*.md')    # add --offline to skip network
python3 -m unittest discover -s tests -v   # stdlib only, no installs
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

## Releasing `@qte77/ui-theme`

`brand/ui-kit` is published to GitHub Packages as `@qte77/ui-theme` (Tailwind
theme tokens for the Vite/React apps). To cut a release: regenerate
(`make -C brand ui_kit`), bump `brand/ui-kit/package.json` `version`, and merge to
`main`. `.github/workflows/publish-ui-theme.yml` then publishes (idempotent; gated
on `gen_ui_kit.py --check`). Never hand-edit `tailwind/tokens.css` — it is
generated from `brand/DESIGN.md`.

## Pre-merge

1. `markdownlint $(git ls-files '*.md')` clean
2. `lychee --offline $(git ls-files '*.md')` clean
3. `uv run brand/scripts/gen_ui_kit.py --check` clean (if `brand/DESIGN.md` or `brand/ui-kit/` changed)
4. `python3 -m unittest discover -s tests` passes
5. CHANGELOG `[Unreleased]` updated
6. Conventional Commits title
