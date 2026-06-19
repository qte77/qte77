# Font licenses

Canonical license texts for every font downloaded by
[`../../scripts/install_fonts.py`](../../scripts/install_fonts.py). The font
binaries themselves are gitignored (fetched on demand); these license files are
committed so this folder is the single source of truth a consumer vendors a
font *and* its license from — no downstream repo hand-maintains a copy.

All fonts here are free/libre and redistributable, but under **three different
licenses** — not all are OFL. Match each `.ttf` to its license below.

| Font file(s) | Family | License | Reserved Font Name | Text |
| ------------ | ------ | ------- | ------------------ | ---- |
| `Inter-Regular.ttf`, `Inter-Bold.ttf` | Inter | SIL OFL 1.1 | — | [`OFL.txt`](OFL.txt) |
| `JetBrainsMono-Regular.ttf`, `JetBrainsMono-Bold.ttf` | JetBrains Mono | SIL OFL 1.1 | — | [`OFL.txt`](OFL.txt) |
| `CascadiaMono-Bold.ttf` | Cascadia Code | SIL OFL 1.1 | Cascadia Code | [`OFL.txt`](OFL.txt) |
| `FiraMono-Bold.ttf` | Fira Mono | SIL OFL 1.1 | Fira | [`OFL.txt`](OFL.txt) |
| `SourceCodePro-Bold.ttf` | Source Code Pro | SIL OFL 1.1 | Source | [`OFL.txt`](OFL.txt) |
| `IBMPlexMono-Bold.ttf` | IBM Plex Mono | SIL OFL 1.1 | Plex | [`OFL.txt`](OFL.txt) |
| `DejaVuSansMono-Bold.ttf` | DejaVu Sans Mono | Bitstream Vera + Arev | — | [`DejaVu-LICENSE.txt`](DejaVu-LICENSE.txt) |
| `UbuntuMono-Bold.ttf` | Ubuntu Mono | Ubuntu Font Licence 1.0 | — | [`UbuntuMono-UFL.txt`](UbuntuMono-UFL.txt) |

## Vendoring a font downstream

When a consumer repo self-hosts one of these fonts (ships the `.ttf`), copy the
matching license text from this folder next to the font, e.g.:

```text
ui/src/assets/fonts/Inter-Regular.ttf   # the font
ui/src/assets/fonts/OFL.txt             # from brand/fonts/LICENSES/OFL.txt
```

The license must travel with the font (OFL §2, UFL §1, Bitstream Vera). Rendered
output — rasterized PNGs, path-baked SVGs — counts as a *document created using
the font* and carries no such obligation, which is why this repo's committed
`brand/images/` artifacts need no bundled license.
