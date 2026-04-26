# /// script
# requires-python = ">=3.11"
# dependencies = ["Pillow>=10.0"]
# ///
"""Generate 1280x640 social preview PNGs from social-previews.toml.

Usage:
    uv run scripts/generate_social.py              # all repos
    uv run scripts/generate_social.py --only qte77 # one repo
    uv run scripts/generate_social.py --light      # force light theme

Output: dist/<repo>-social.png + dist/upload-checklist.md.
PNGs must be uploaded to each repo manually (Settings -> General ->
Social preview); GitHub exposes no API for setting the social image.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
import tomllib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BRAND = Path(__file__).resolve().parent.parent
PALETTE_FILE = BRAND / "palette.toml"
CONFIG_FILE = BRAND / "social-previews.toml"
FONTS_DIR = BRAND / "fonts"
DIST = BRAND / "dist"

FONT_TITLE = FONTS_DIR / "Inter-Bold.ttf"
FONT_BODY = FONTS_DIR / "Inter-Regular.ttf"
FONT_MONO = FONTS_DIR / "JetBrainsMono-Regular.ttf"


def load_toml(path: Path) -> dict:
    with path.open("rb") as f:
        return tomllib.load(f)


def hash_accent(repo: str, theme_palette: dict) -> str:
    """Deterministic accent fallback when none set explicitly."""
    digest = hashlib.sha256(repo.encode()).digest()
    hue = digest[0] / 255.0
    # Pick from a curated set so colors stay on-brand.
    options = [
        theme_palette["accent"],
        theme_palette["accent_warm"],
        "#3fb950",  # green
        "#a371f7",  # purple
        "#f85149",  # red
        "#d29922",  # yellow
    ]
    return options[int(hue * len(options)) % len(options)]


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    if not path.exists():
        sys.exit(
            f"missing font: {path}\n"
            f"run: uv run scripts/install_fonts.py"
        )
    return ImageFont.truetype(str(path), size)


def render_card(repo: dict, defaults: dict, palette: dict, force_theme: str | None) -> Image.Image:
    theme = force_theme or repo.get("theme") or defaults.get("theme", "dark")
    p = palette[theme]
    accent = repo.get("accent") or hash_accent(repo["name"], p)

    w = defaults.get("width", 1280)
    h = defaults.get("height", 640)

    img = Image.new("RGB", (w, h), p["bg"])
    d = ImageDraw.Draw(img)

    pad = 72
    # Vertical accent bar on the left
    d.rectangle([pad, pad, pad + 6, h - pad], fill=accent)

    x = pad + 32
    # Title
    title_font = font(FONT_TITLE, 112)
    d.text((x, pad - 8), repo["title"], font=title_font, fill=p["text"])

    # Subtitle
    sub_font = font(FONT_BODY, 32)
    d.text((x, pad + 132), repo.get("subtitle", ""), font=sub_font, fill=p["text_muted"])

    # Tagline (mono, near bottom)
    tag = repo.get("tagline", "")
    if tag:
        tag_font = font(FONT_MONO, 24)
        # word-wrap if too wide
        max_w = w - x - pad
        words = tag.split()
        lines: list[str] = []
        current = ""
        for word in words:
            trial = f"{current} {word}".strip()
            if d.textlength(trial, font=tag_font) <= max_w:
                current = trial
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        line_h = 36
        y0 = h - pad - line_h * len(lines)
        for i, line in enumerate(lines):
            d.text((x, y0 + i * line_h), f"> {line}" if i == 0 else f"  {line}",
                   font=tag_font, fill=p["text"])

    # Owner mark in top-right
    mark_font = font(FONT_MONO, 20)
    mark_text = "@qte77"
    mw = d.textlength(mark_text, font=mark_font)
    d.text((w - pad - mw, pad), mark_text, font=mark_font, fill=p["text_muted"])

    return img


def write_checklist(repos: list[dict]) -> None:
    DIST.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Social preview upload checklist",
        "",
        "GitHub provides no API for setting social previews. Upload each PNG",
        "manually via the repo's Settings → General → Social preview.",
        "",
    ]
    for r in repos:
        url = f"https://github.com/qte77/{r['name']}/settings"
        png = f"dist/{r['name']}-social.png"
        lines.append(f"- [ ] [{r['name']}]({url}) — `{png}`")
    (DIST / "upload-checklist.md").write_text("\n".join(lines) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="generate for one repo only")
    ap.add_argument("--light", action="store_true", help="force light theme")
    ap.add_argument("--dark", action="store_true", help="force dark theme")
    args = ap.parse_args()

    palette = load_toml(PALETTE_FILE)
    config = load_toml(CONFIG_FILE)
    defaults = config.get("defaults", {})
    repos = config.get("repo", [])

    if args.only:
        repos = [r for r in repos if r["name"] == args.only]
        if not repos:
            sys.exit(f"no repo entry for: {args.only}")

    force = "light" if args.light else "dark" if args.dark else None

    DIST.mkdir(parents=True, exist_ok=True)
    for r in repos:
        img = render_card(r, defaults, palette, force)
        out = DIST / f"{r['name']}-social.png"
        img.save(out, "PNG", optimize=True)
        print(f"wrote {out}")

    write_checklist(repos)
    print(f"checklist: {DIST / 'upload-checklist.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
