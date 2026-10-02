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

## Quick start

Goal: build a design system and page templates in Claude Design (or a similar tool) and publish them to a
real website. The sections below give the detail for each step.

1. **Design-system package in your repo.** Tokens generated from a `DESIGN.md`-style parameter file by a
   small local generator, plus a drift check in CI and React components.
2. **Sync it to the design tool's design-system project.** Upload order: sentinel, all content, deletes
   as the diff lists them, sentinel again, sync-state file last.
3. **Build templates in the design tool on that design system.** Ask for these up front: title,
   description and favicon in the static head; `viewport-fit=cover`; landmarks and one `h1`; no CDN-only
   dependencies; exported media; a weak-device path.
4. **Fetch every template file into the repo as an untouched snapshot.** Use an extract script for large
   files. A sync script re-applies the written change list; each change is applied, already carried by
   the template, or failed, and a failure writes nothing.
5. **Deploy build next to the snapshot.** Precompile the JSX, self-host React (checked against its
   integrity hash, loaded first), a CSP of `'self'` plus inline-script hashes, and rewrite only the
   anchored CSP line. The build fails if an anchor moves. Run it in CI.
6. **Deploy, then verify in a real browser at phone and desktop sizes.** Page and console errors, CSP
   violation events, responses of 400 or more, response headers, the main visual mounted, one real
   interaction. Restore the last good build first if anything breaks.
7. **Mobile-first and agent-ready.** Use the checklists in the sections of those names.

Rules: the design tool owns the template. Repo patches only as listed exceptions, sent upstream and
dropped at the next sync. Verify vendor and spec claims at source before publishing.

## What to ask the design tool to build into templates

Ask for these up front — each one skipped becomes a repo patch later.

- Title, description and favicon set in the static head, not only at runtime.
- `viewport-fit=cover` on the viewport meta.
- Landmarks (header, nav, main, footer) and exactly one `h1`.
- No hard dependency on a third-party CDN that a build cannot replace.
- Media (video, poster images) exported as files, not only referenced by URL.
- A weak-device and reduced-motion path (see Mobile-first).
- Canvas sized to the element it renders into, not a fixed pixel size (see Mobile-first).
- Accessible names on every control.
- One live region per group of values that update together, not one per value.

## Two flows, one direction each

| What | Source of truth | Flows to |
| --- | --- | --- |
| Tokens and components | the product repo (a design-system package) | the design tool's design-system project |
| Page templates | the design tool | the product repo's site folder, then the host |

- Deploy-only files (404 page, robots.txt, sitemap, headers, llms.txt) live only in the repo.

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

## Template to production

### Fetch

- The design tool's API can return files too large to handle inline. A small extract script reads
  the fetched results from the session's saved output and writes them to disk, so no content is
  retyped by hand.
- Fetch every file of the template.
- Diff each new version against the snapshot before copying.

### Snapshot and sync

- Keep the fetched template as a read-only snapshot folder.
- Keep a written list, in the site package README, of every change made to the fetched template
  (asset paths, removed preloads, metadata blocks).
- A sync script copies the snapshot in and re-applies the list. Each change is reported as applied,
  as already carried by the template (then drop it from the list and the script), or as failed — on
  any failure nothing is written.
- **Exception, when a fix cannot wait for the design:** patch the snapshot in the repo, list the patch
  in the same README, send the same change to the design tool, and drop the patch at the next sync once
  the template carries it. Never patch silently.
- Repo-only blocks in the HTML (agent metadata) are fenced with marker comments, lifted from the old
  file and re-inserted into the new one, so they have one source.
- After each sync, check plain-text summaries (llms.txt, the plain-text page, the no-JS block)
  against the new template text, or they drift silently.

### Deploy build

- Production serves a build output, not the snapshot: a design tool's runtime often compiles JSX in
  the browser, and a build step with self-hosted assets is the biggest speed win and allows a strict
  content security policy.
- Precompile the template's JSX: an esbuild transform to classic `React.createElement`, no bundling
  needed.
- Wrap each compiled file in the scope the runtime gave it.
- Load the files as deferred scripts, in their original order.
- Prefer the runtime's own hooks over patching its code — a component taken from the global scope
  with no source URL is read off `window` instead of fetched and evaluated; a React already on the
  page makes the runtime skip its own CDN load.
- Self-host React and similar libraries under a versioned path, verify each file against the
  integrity hash the runtime pins (Subresource Integrity), and cache that path as immutable.
- Load React before anything that reads it: a design-system bundle that runs first can fail silently
  in a load-order race.
- The build fails loudly when an anchor it rewrites — an import attribute, a script tag, a pinned
  hash, the CSP line — is missing, so a template change shows up in CI, not in production.
- Run the build in CI.

### Security headers

- Set them in the static host's headers file: CSP, HSTS, `frame-ancestors` or `X-Frame-Options`,
  `nosniff`, referrer and permissions policies, COOP/CORP, long caching for fonts and versioned
  assets.
- With precompiled scripts the CSP can drop third-party script hosts, `'unsafe-inline'` and
  `'unsafe-eval'` for scripts: `'self'` plus the SHA-256 hash of each inline script, computed by the
  build.
- Styles usually still need `'unsafe-inline'` — runtimes and React set inline styles.
- Rewrite only the exact header line, anchored. An unanchored pattern once matched a comment,
  swallowed a rule line, and production shipped with no security headers while the page looked fine.
- Make the build assert that every rule line survives and that `script-src` allows no eval, inline or
  third-party source.

### Verify

- Check before and after each deploy, in a real browser at desktop and phone sizes: page errors,
  console errors, responses of 400 or more, and one real interaction.
- Listen for CSP violation events (`securitypolicyviolation`), not only console errors.
- Fail on any request to a third-party host the page should no longer use.
- Check the response headers after every deploy.
- Wait for the main visual (e.g. a canvas) to mount, not only the first interactive block.
- Preview locally with the host's own dev server so the headers file applies; a plain file server
  ignores it.
- Headless browsers without a GPU give a lower bound on frame times, not device numbers.
- Deploy to production only, then verify with a cache-busting fetch and a content marker; the edge can
  serve the old page for a few minutes.
- When a deploy breaks something, restore the last good build first, then fix through review.
- Run simulated-visitor reviews (the people you want to reach, a keyboard user, an AI agent) and tag
  each finding as a repo fix or a design fix.

## Mobile-first

- Viewport: `width=device-width, initial-scale=1, viewport-fit=cover`. Pad full-bleed bars with
  `env(safe-area-inset-*)`, exposed as tokens.
- Use `svh` units for full-screen sections.
- Respond to the component's container, not the viewport: the size container goes on an outer
  wrapper, same setup as the design-tokens rule above — a container query never matches its own
  container.
- Tap targets at least 44×44 CSS px, from one token (alias it, don't duplicate the value), measured
  from rendered sizes.
- 16 px minimum text on phones — smaller form inputs make some mobile browsers zoom on focus.
- Phone patterns: stepped or tabbed panels instead of one long control column; a full-bleed 16:9
  stage with a chapter bar; horizontal swipe only, so vertical scroll is never hijacked.
- Canvas and video backing store = rendered size × `devicePixelRatio` (cap 2), re-measured once the
  size settles (`ResizeObserver`) — an early read can return the element's width attribute and
  render many times the pixels shown.
- Pause rendering when the page is hidden or the element is off screen.
- Probe for a weak device from `hardwareConcurrency`, `deviceMemory`, `saveData` and reduced motion.
  `deviceMemory` exists only in Chromium-based browsers and is bucketed, so a typical mid-range phone
  passes as strong.
- On weak devices: a 1× backing store and a still first frame.
- Compute WCAG contrast for every text/background pair, per theme (muted text at least 4.5:1); keep
  low-contrast tokens for lines and bars, not for text.
- Audit at 320, 390, 430, 768, 1280 and 1920 px, plus a landscape phone: horizontal overflow
  (`scrollWidth - innerWidth`) at 320, tap-target sizes, sticky elements while scrolling.
- Momentum scrolling and real frame rates need a real phone.

## Agent-ready

For pages built with JavaScript:

- A visible summary readable without JavaScript, with landmarks and the key questions answered.
  Agent-readiness scanners ignore `<noscript>`, so render it as a normal block and remove it with a
  one-line inline script when JavaScript runs (hash that script in the CSP).
- `llms.txt` saying what the site is, when to use it, and when not to.
- A plain-text twin (`index.md`) with frontmatter (title, description, canonical, last-updated),
  linked from the head as `rel="alternate" type="text/markdown"` and in a `Link` response header.
- JSON-LD for what the page actually is: `sameAs` only for verified official profiles, Person
  entries only with publicly stated facts, an FAQ type only when it mirrors visible questions, no
  organisation facts that are not confirmed, and never schema types or endpoints (API, MCP, OAuth)
  the site does not have.
- Agent Skills discovery at `/.well-known/agent-skills/index.json` (discovery RFC v0.2.0): a
  `$schema` field and a `skills` array with name, type `skill-md`, description, url and `digest` —
  the SHA-256 of the SKILL.md bytes. Update the digest whenever SKILL.md changes; keep the skill to
  what the site really offers, such as reading and citing.
- `/.well-known/ard.json` (Agentic Resource Discovery): an `entries` array with identifier
  `urn:air:<domain>:<namespace>:<name>`, displayName, type and url. Some scanners also require a
  top-level `specVersion`.
- Canonical and Open Graph meta (an `og:image` raises scores), `robots.txt` with an explicit AI
  policy such as a content-signal line, a sitemap with `lastmod`, and real 404s — no fallback that
  answers every path with the home page.
- Rescan after each deploy and read the scanner's authoritative per-check result, not summary chips,
  which can disagree between loads.

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
