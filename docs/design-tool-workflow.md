# Design-tool workflow

How to work with AI design tools (Claude Design, and the same test applies to v0, Figma Make and
similar) so that what the tool produces ships as code, stays in sync, and does not bottleneck on one
person or one session. Learned by taking one product from design-tool canvas to a deployed, synced site.

## The one rule: templates ship, artifacts do not

- A **template** is a page built on a design system you own: an HTML entry file plus scripts that load
  the design-system bundle. You can fetch it, copy it into a repo and deploy it.
- An **artifact** (a canvas or one-off page) is a picture of a design. Someone has to re-implement it.
- Tool-agnostic test: can the tool export a page that loads a design bundle you own and can re-fetch
  when it changes? If not, its output is a reference, not a deliverable.
- So each product moves towards: a design system synced from its repo, templates built on it, and
  artifacts only for exploration, audits and one-off assets.

## Two flows, one direction each

| What | Source of truth | Flows to |
| --- | --- | --- |
| Tokens and components | the product repo (a design-system package) | the design tool's design-system project |
| Page templates | the design tool | the product repo's site folder, then the host |

- Deploy-only files (404 page, robots.txt, sitemap, headers, llms.txt) live only in the repo.
- Keep a written list, in the site package README, of every change made to the fetched template
  (asset paths, removed preloads, metadata blocks). Each sync re-applies the list.
- **Exception, when a fix cannot wait for the design:** patch the snapshot in the repo, list the patch
  in the same README, send the same change to the design tool, and drop the patch at the next sync once
  the template carries it. Never patch silently.

## Design system to design tool

- Upload with full writes in a fixed order: a sentinel file, all content, deletes exactly as the diff
  lists them, the sentinel again, and the sync-state file last. A partial write list can desync the
  project silently.
- Re-fetch the remote sync state right before uploading; if it moved, re-run the diff.
- Record the upload anchor (bundle hash) in the plan after each upload.
- Write CSS the tool's checker can read: declare tokens on the scope it registers (the theme root), not
  on child selectors; tag tokens it cannot classify (easings, durations, gradients, filters).
- A container query never matches its own container. Width-dependent tokens need the size container on
  an outer wrapper, with the wrapper taking the component's className and style so width-based previews
  still work.
- Ask the design tool which CSS shape it accepts before restructuring; its answer is a spec.
- "Renders cleanly" is not "renders correctly": look at the mobile previews, or have a second model
  review the diff.
- If sub-agents cannot call the design tool's API, let them build and validate the bundle and keep the
  upload in the main session.

## Template to site

- Diff each new template version against the site folder before copying.
- Check before and after each deploy, in a real browser at desktop and phone sizes: page errors,
  console errors, responses of 400 or more, and one real interaction.
- Deploy to production only, then verify with a cache-busting fetch and a content marker; the edge can
  serve the old page for a few minutes.
- Make the site readable without JavaScript: llms.txt, a plain-text index, canonical and Open Graph
  meta, JSON-LD, and a noscript summary. Publish no organisation facts that are not confirmed.
- Precompile when you can: a design tool's runtime often compiles JSX in the browser; a build step with
  self-hosted assets is the biggest speed win and allows a strict content security policy.
- Run simulated-visitor reviews (the people you want to reach, a keyboard user, an AI agent) and tag
  each finding as a repo fix or a design fix.

## A base design system products derive from

- The design tools already work this way: a built-in design system is one component set plus a small
  parameter file (hue, light or dark, saturation, fonts, density, radius, layout, image treatment, icon
  set, button style) from which every token is derived.
- The estate has the same shape in [`brand/DESIGN.md`](../brand/DESIGN.md): parameters in the open
  design.md format, a generator, and a published theme package.
- Proposed (not built yet): each product writes its own `DESIGN.md` in the same format and uses the same
  generator, so products share the token structure, the accessibility rules and the checker-safe CSS
  shape while keeping their own look. Plain CSS custom properties are the shared contract; a React theme
  wrapper stays optional. Neutral token prefixes keep brands apart by value, not by name.
- Each product keeps its own design-tool project, synced from its own repo. Upgrades are opt-in version
  bumps, never a push across products.
