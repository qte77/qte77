# gh-endpoints

Notes on GitHub functionality the public REST API, public GraphQL API,
and `gh` CLI do not cover, plus the undocumented internal endpoints
the web UI uses to provide it.

## Why this exists

- Surface real gaps so we know which workflows can't be scripted via
  supported APIs
- Capture reverse-engineering of internal endpoints when scripting
  matters more than supportability
- Make future-you's "is there an API for X?" research instant

## Layout

- [`INDEX.md`](INDEX.md) — table of confirmed gaps with first-party
  citations
- [`HOWTO.md`](HOWTO.md) — methodology for enumerating gaps and
  documenting endpoints
- `<feature>.md` — one file per documented internal endpoint (see
  [`social-preview.md`](social-preview.md) as the template)

## Standalone repo plan

This folder is sized to graduate into its own repo (e.g.
`qte77/gh-endpoints`) once it has 3+ documented endpoints or the upload
tooling matures. Tracking issue:
[qte77/qte77#44](https://github.com/qte77/qte77/issues/44).

When extracting:

```bash
# inside qte77/qte77
git subtree split --prefix=docs/gh-endpoints -b extract/gh-endpoints
# in the new repo
git pull <qte77/qte77 path> extract/gh-endpoints
```

`brand/scripts/upload_social_preview.py` would migrate at the same time.

## Scope and ethics

- Documenting public-UI behavior of GitHub-the-product is fair game.
- Tooling on own resources with own session cookies is in scope.
- Mass automation, scraping, or sessions you don't own are out.
- This is not a security research project.
