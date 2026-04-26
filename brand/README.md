# Brand assets

Source palette, logo, and font references for qte77 visual identity.

## Files

- `palette.toml` — color tokens (GitHub Primer, light + dark variants)
- `images/logo-mark.text.svg` / `logo-mark.paths.svg` — square mark; canonical text + path-baked variant
- `images/logo-wordmark.text.svg` / `logo-wordmark.paths.svg` — wordmark; same pair
- `images/avatar_dark.png` / `images/avatar_light.png` — 920×920 PNG
  rasters of the mark for use as a GitHub account avatar (rendered by
  `scripts/render_avatar.py`)
- `fonts/` — typography (downloaded by `scripts/install_fonts.py`, gitignored)
- `scripts/` — Python tooling (font download, avatar render, social
  preview render, SVG text-to-paths conversion)
- `Makefile` — entry point for all the above; see `make -C brand help`

<details>
<summary>Preview: <code>images/logo-mark.paths.svg</code></summary>

<img src="./images/logo-mark.paths.svg" alt="qte77 mark" width="120">

</details>

<details>
<summary>Preview: <code>images/logo-wordmark.paths.svg</code></summary>

<img src="./images/logo-wordmark.paths.svg" alt="qte77 wordmark" width="320">

</details>

<details>
<summary>Preview: <code>images/avatar_dark.png</code></summary>

<img src="./images/avatar_dark.png" alt="qte77 avatar (dark)" width="200">

</details>

<details>
<summary>Preview: <code>images/avatar_light.png</code></summary>

<img src="./images/avatar_light.png" alt="qte77 avatar (light)" width="200">

</details>

## Adaptive theming

### Single-file SVG with inline media query

Both SVGs in this folder use inline `@media (prefers-color-scheme: dark)`,
so one file adapts to the viewer's GitHub theme. The same pattern is used
in `assets/images/mental-model.svg` and `assets/images/pipeline-layers.svg`
(see those for live examples already rendered in the project README).

This is browser-native CSS behavior. GitHub does not formally document
SVG `prefers-color-scheme` as a supported feature, but a GitHub team
member has confirmed the platform handles it correctly:
[community#62430](https://github.com/orgs/community/discussions/62430).
Inline `<style>` is permitted because GitHub serves SVGs with
`Content-Security-Policy: style-src 'unsafe-inline'`. SVG inline
**scripting and animation** are blocked, but CSS is not — see
[Working with non-code files](https://docs.github.com/en/repositories/working-with-files/using-files/working-with-non-code-files).

Caveat: works reliably on Chromium-based browsers; WebKit has known
engine-side gaps unrelated to GitHub.

### Raster images (PNG/JPG/GIF)

Use the `<picture>` element with `prefers-color-scheme` in the `media`
attribute — this is GitHub's currently-documented method for theme-aware
images of any type:
[basic writing and formatting syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

```markdown
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./brand/logo-dark.png">
  <img src="./brand/logo-light.png" alt="qte77">
</picture>
```

The older `#gh-light-mode-only` / `#gh-dark-mode-only` URL fragments
still render today, but GitHub has marked them deprecated in the
Enterprise Server docs in favor of `<picture>`. Full comparison and
sources in [docs/github-image-theming.md](../docs/github-image-theming.md).

## Fonts

- **Inter** (sans, headings) — [rsms/inter](https://github.com/rsms/inter), OFL
- **JetBrains Mono** (mono, code) — [JetBrains/JetBrainsMono](https://github.com/JetBrains/JetBrainsMono), OFL

## Usage

All tooling lives in `brand/` and is driven by `brand/Makefile`.

```bash
make -C brand help            # list targets
make -C brand setup_brand_fonts
make -C brand brand_avatar    # avatar_{dark,light}.png
make -C brand brand_social    # dist/<repo>-social.png
make -C brand brand_paths     # logo-mark.paths.svg (text -> path derivation)
make -C brand brand           # all of the above (full refresh)
```

Or `cd brand && make <target>`. Output:

- `images/avatar_{dark,light}.png` — for GitHub account avatar (UI-only upload)
- `dist/<repo>-social.png` — for repo social preview (UI-only upload)
- `images/logo-mark.paths.svg` — derived path-only SVG used by the
  rasterizer (gitignored)

GitHub provides no API for setting either avatar or social preview;
both are UI-only. See [`docs/gh-endpoints/INDEX.md`](../docs/gh-endpoints/INDEX.md).
