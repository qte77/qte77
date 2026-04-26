# Theme-aware images in GitHub Markdown

Three techniques for serving different images to viewers in GitHub
light vs. dark mode. Two are documented; one is implicit. One is
formally deprecated. All three currently render.

## 1. `<picture>` element with `prefers-color-scheme` (current, recommended)

GitHub's documented method for both raster and SVG images.

```markdown
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./logo-dark.png">
  <img src="./logo-light.png" alt="qte77">
</picture>
```

Source: [basic writing and formatting syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
on `docs.github.com`. Same syntax appears in the
[quickstart guide](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github).

Pros: works everywhere `<picture>` works (all current browsers). One
documented mechanism for raster and SVG alike. No source-file changes
needed for the assets.

Cons: requires two image files when one would suffice (compare
technique 3 for SVG).

## 2. URL fragments `#gh-light-mode-only` / `#gh-dark-mode-only` (older method, superseded)

The older method, still rendering today.

```markdown
![qte77](./logo-light.png#gh-light-mode-only)
![qte77](./logo-dark.png#gh-dark-mode-only)
```

### Timeline (first-party)

| Date       | Event                                | Source |
|------------|--------------------------------------|--------|
| 2021-11-24 | Fragments introduced                 | [github.blog changelog](https://github.blog/changelog/2021-11-24-specify-theme-context-for-images-in-markdown/) |
| 2022-05-19 | `<picture>` element entered beta     | [github.blog changelog](https://github.blog/changelog/2022-05-19-specify-theme-context-for-images-in-markdown-beta/), [community#16910](https://github.com/orgs/community/discussions/16910) |
| 2022-08-15 | `<picture>` element became GA        | [github.blog changelog](https://github.blog/changelog/2022-08-15-specify-theme-context-for-images-in-markdown-ga/) |
| —          | Cloud docs silently drop the fragments | [current basic writing and formatting syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax) (only `<picture>` present) |

### What "deprecated" actually means here

GitHub has never published a changelog entry, blog post, or
cloud-docs page that uses the word "deprecated" for these fragments.
The fragments still render at time of writing.

The literal word "deprecated" appears in exactly one first-party
location: the **Enterprise Server 3.5–3.8** docs, which retained
documentation of the older method long enough to add a migration
notice:

> The old method of specifying images based on the theme, by using a
> fragment appended to the URL (`#gh-dark-mode-only` or
> `#gh-light-mode-only`), is deprecated and will be removed in favor
> of the new method described above.

Source: [enterprise-server@3.8 basic-writing-and-formatting-syntax](https://docs.github.com/en/enterprise-server@3.8/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
(same language across 3.5–3.8). This is a snapshot of older Cloud
docs that the public Cloud docs have since removed; it is the
strongest first-party text calling the fragments deprecated, but it
is **not** an authoritative Cloud-side deprecation notice.

Practical reading: the fragments are unannounced-but-superseded.
Treat them as legacy. Migrate to `<picture>`.

Pros: more compact than `<picture>` for a single line.

Cons: legacy; no SLA; will likely stop rendering at some point. Use
`<picture>` in new code.

## 3. Inline `@media (prefers-color-scheme: dark)` inside SVG (works, not formally documented)

A single SVG file containing a `<style>` block with a media query
auto-adapts to viewer theme.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 80">
  <style>
    .fg { fill: #1f2328; }
    @media (prefers-color-scheme: dark) {
      .fg { fill: #e6edf3; }
    }
  </style>
  <text class="fg" ...>qte77</text>
</svg>
```

Empirical evidence inside this repo:
- `assets/images/mental-model.svg`
- `assets/images/pipeline-layers.svg`
- `brand/logo-mark.svg`
- `brand/logo-wordmark.svg`

All four are referenced from READMEs via plain `<img>` tags and adapt
correctly in GitHub's light and dark themes.

First-party context for why this works:
- A GitHub team member confirmed in
  [community#62430](https://github.com/orgs/community/discussions/62430)
  that GitHub itself handles `prefers-color-scheme` correctly; reported
  rendering issues there were traced to a WebKit engine bug, not
  GitHub's pipeline.
- GitHub's
  [Working with non-code files](https://docs.github.com/en/repositories/working-with-files/using-files/working-with-non-code-files)
  page is the closest documentation: it states SVG inline scripting
  and animation are blocked, but says nothing about `<style>` blocks
  or media queries — they pass through. SVGs are served with a CSP
  that permits inline styles.

Pros: one file. Pairs naturally with the rest of the design system
(palette tokens applied via class names; theme switch handled at the
CSS layer). No HTML wrapper needed.

Cons: not formally documented as a supported feature. A future GitHub
sandboxing change could in principle restrict inline `<style>` —
unlikely but not contractually stable. WebKit-based browsers
(non-Chromium) have had engine-side gaps that affect rendering on
some platforms; verify across targets if cross-browser fidelity
matters.

## Recommendation

- For raster images: technique 1 (`<picture>`). Migrate any remaining
  `#gh-*-mode-only` usages.
- For SVGs you control and can edit: technique 3 (inline `@media`)
  for compactness, with technique 1 as a fallback if you also need
  raster variants for environments that don't render SVG (e.g.,
  GitHub social previews, which are raster only).
- Never use technique 2 in new code.
