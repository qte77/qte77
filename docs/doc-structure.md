# Documentation structure

The canonical README and document-hierarchy contract for every repo in the
[qte77 estate](https://github.com/qte77?tab=repositories). One shape, so anyone
landing on any repo knows where to look.

**This repo is the source of truth.** The
[`templates/README.template.md`](templates/README.template.md) skeleton is the
canonical artifact; the skills, rules, and plugins that audit or scaffold docs (in
[claude-code-plugins](https://github.com/qte77/claude-code-plugins)) are **derived
from it** — they enforce this contract, they do not define it. When the contract
changes, change it here and let the downstream mechanism follow. Same
generate-from-source discipline as `brand/DESIGN.md` → `eyerest.css`.

## README — canonical order

Value-first: lead with what it does and how to use it; defer the rationale. The hero
tagline carries the motivation, so `Why` can sit low.

```text
HERO       H1 name + one-line tagline   (optional theme-aware wordmark)
BADGES     License · Version · CI
## What    ≤ ~7 bullets  (+ optional screenshots <details> at bottom)
## How     minimal run example + link out
## Why     2–4 lines, deferred
## Refs    links only
## License SPDX + LICENSE link
<tail>     one repo-type section (profile · plugin · engine)
```

| Section | Required | Rule |
| --- | --- | --- |
| **Hero** | yes | H1 name + one-line tagline (*what · who-for · positioning*) — `**name** is …` or `# name` + a `>` blockquote. Visual wordmark/logo **optional** (theme-aware + self-hosted if present); a text hero fully adheres. |
| **Badges** | yes | License · Version · CI/status — see [Badges](#badges). Shields/CI images are the only sanctioned external images. |
| **What** | yes | ≤ ~7 tight bullets — what it does *for the reader*. Build internals → `docs/`. |
| ↳ Screenshots | optional | Collapsed `<details>` at the **bottom of What**; theme-aware; self-hosted at `assets/images/`. |
| **How** | yes | Minimal run example + "see `docs/…`" link. Not a full reference. |
| **Why** | yes | 2–4 lines, deferred below How. Pattern: incumbent → gap → how we differ. Link specs. |
| **Refs** | yes | Links only, no prose. |
| **License** | yes | SPDX + `LICENSE` link; attribute bundled third-party in `NOTICE`. |
| **`<tail>`** | optional | One repo-type section, after License or folded into What: profile → Tools/Posts · plugin → Plugins table · engine → API link. |

## Badges

Order (left→right), per the SSOT, [paperverse](https://github.com/qte77/paperverse):

1. **License** — shields.io static, `blue`, links to `LICENSE`; put the SPDX id in the label (`License: Apache-2.0`)
2. **Version** — shields.io static, `blue`, **linked** to `CHANGELOG.md` (never a bare `![…]`)
3. **CI / status** — CodeQL, CodeFactor, the primary CI workflow, lint, then any extras

Colors: static info badges (License, Version) are shields.io **`blue`**; dynamic status badges use the **service's native color** — never hardcode it, the color *is* the signal. Title-case labels. Left-aligned on consecutive lines immediately after the tagline — no `<p align="center">`.

Profile repos (no version/CI) may carry a License badge only, or omit the badge row.

## The front-door rule

A README orients; it does not document. Each section answers its one question at the
minimum and links depth out to `docs/` or external URLs — never inlines it. Anything
past a section's budget is the signal to extract to `docs/` and link, not to expand
the README.

## Screenshots & theme-aware images

Self-host at `assets/images/`; never hotlink (GitHub's camo proxy mangles external
image URLs). Make them theme-aware:

- **Raster (PNG):** `<picture>` + `<source media="(prefers-color-scheme: dark)">` → two committed files (dark + light).
- **SVG:** inline `@media (prefers-color-scheme: dark)` → one file.

Technique reference: [`github-image-theming.md`](github-image-theming.md). Keep the
blank lines inside `<details>`/`<picture>` so GitHub renders the nested markdown.

## Document hierarchy

One audience per file; no duplication.

| File | Audience | Owns |
| --- | --- | --- |
| `README.md` | users / evaluators | this contract |
| `CONTRIBUTING.md` | contributors | commands, conventions, the `## Documentation hierarchy` + `## Releasing` statements |
| `AGENTS.md` | AI agents | behavioural rules, decision framework |
| `CLAUDE.md` | Claude Code loader | a one-line `@AGENTS.md` pointer — never a copy |

## Releasing

For repos that cut versioned releases (skip for profile / docs / action-only repos). Semi-automatic by design — a **human-authored** bump PR (so the merge is a real-user event, sidestepping the bot `action_required` gotcha), then automatic tagging and a one-command publish. SemVer; the version source of truth lives in the package manifest, mirrored in the README version badge (`-blue`).

1. In a release PR, bump the version with the repo's tool (`uv run bump-my-version bump <part>`, `npm version <part> --no-git-tag-version`, …), update the README badge, and roll `## [Unreleased]` → `## [X.Y.Z] - <date>` in `CHANGELOG.md` (or `scriv collect` if using `changelog.d/` fragments).
2. Merge — a reusable `tag-release` workflow tags `vX.Y.Z` on the version change.
3. Optionally run `publish-release` to cut the GitHub Release from the matching `CHANGELOG.md` block. Tag-only is fine.

`tag-release` + `publish-release` are reusable workflows hosted in [qte77/.github](https://github.com/qte77/.github); each repo carries the `## Releasing` steps in its CONTRIBUTING. No GitHub App or auto-merge needed — the human merge is what makes tagging fire cleanly.

## Optional patterns

- **"What this isn't" callout** — a short blockquote disclaiming false expectations
  (e.g. "internal tool, not a published library"). Kills wrong assumptions early.
- **Why-as-comparison** — *incumbent pioneered X → but gap Y → we're different: Z*,
  with a link to the spec. Concise and differentiating.

## Enforcement

Derived from this page, never authoritative — see
[claude-code-plugins](https://github.com/qte77/claude-code-plugins): `docs-governance`
audits structure, `readme-generator` audits completeness, `workspace-setup` scaffolds
new repos from the template. Per-repo CI runs markdown + link lint. The contract stays
here; mechanism follows.
