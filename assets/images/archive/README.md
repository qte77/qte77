# Legacy SVG archive

Earlier-generation diagrams, retired during the #32 / PR #37 audit. Kept for reference
so the historical design is traceable without `git log` archaeology. The current SVG
set lives one level up.

## Why archived (not deleted)

Each was superseded by a simpler artifact. Listing here so the replacement is obvious:

| Archived | Replaced by | Reason |
| --- | --- | --- |
| `architecture.svg` | `mental-model.svg` | cluster view grew to 39 repo-boxes across 7 layers; maintenance tax too high |
| `universe.svg` | `mental-model.svg` | short-lived cluster catalog — mental-model is a strict superset (adds flow + feedback) |
| `toolchain-layers.svg` | `mental-model.svg` | 7-layer goal→delivery stack collapsed into mental-model's linear flow |
| `agent-architecture.svg` | `docs/project-workflows.md` | per-repo isolation + 5 bridges already documented in prose |
| `decision-flow.svg` | `docs/project-workflows.md` | task routing already documented as ASCII decision tree |
| `weekly-cycle.svg` | `docs/project-workflows.md` | weekly rhythm already documented as ASCII schedule |

## Do not link from README

The archive exists for history, not for end users. If a diagram here is load-bearing
enough to reference, promote it back to `assets/images/` and delete the archived copy.
