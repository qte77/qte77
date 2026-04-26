# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Download brand fonts into brand/fonts/.

All fonts are SIL OFL 1.1 (or compatible) and free to redistribute:
- Inter (sans, headings) — Fontsource CDN
- JetBrains Mono (mono, social-preview taglines) — Fontsource CDN
- Cascadia Mono (mark/wordmark default) — Fontsource CDN
- DejaVu Sans Mono, Liberation Mono — Linux defaults; raw GitHub via jsdelivr
- Fira Mono, Source Code Pro — additional Linux-leaning monos via Fontsource

The Linux monos are available so brand_paths can bake .paths.svg
variants from each, letting consumers pick the closest match to what
their viewers' systems render."""

from __future__ import annotations

import io
import sys
import urllib.request
import zipfile
from pathlib import Path

FONTS_DIR = Path(__file__).resolve().parent.parent / "fonts"

# Fonts only available via release archives (no raw TTF on a CDN).
# Each entry: dest filename -> (zip url, member path inside zip)
ZIPPED_FONTS = {
    "DejaVuSansMono-Bold.ttf": (
        "https://github.com/dejavu-fonts/dejavu-fonts/releases/download/version_2_37/dejavu-fonts-ttf-2.37.zip",
        "dejavu-fonts-ttf-2.37/ttf/DejaVuSansMono-Bold.ttf",
    ),
}

FONTS = {
    "Inter-Bold.ttf":
        "https://cdn.jsdelivr.net/fontsource/fonts/inter@latest/latin-700-normal.ttf",
    "Inter-Regular.ttf":
        "https://cdn.jsdelivr.net/fontsource/fonts/inter@latest/latin-400-normal.ttf",
    "JetBrainsMono-Regular.ttf":
        "https://cdn.jsdelivr.net/fontsource/fonts/jetbrains-mono@latest/latin-400-normal.ttf",
    "JetBrainsMono-Bold.ttf":
        "https://cdn.jsdelivr.net/fontsource/fonts/jetbrains-mono@latest/latin-700-normal.ttf",
    "CascadiaMono-Bold.ttf":
        "https://cdn.jsdelivr.net/fontsource/fonts/cascadia-mono@latest/latin-700-normal.ttf",
    # --- Linux monospaces (for paths.svg variants) ---
    # All Fontsource-hosted; DejaVu/Liberation aren't on Fontsource and their
    # raw GitHub paths don't resolve reliably, so we use four widely-deployed
    # Linux-friendly monos that download cleanly.
    "UbuntuMono-Bold.ttf":
        "https://cdn.jsdelivr.net/fontsource/fonts/ubuntu-mono@latest/latin-700-normal.ttf",
    "FiraMono-Bold.ttf":
        "https://cdn.jsdelivr.net/fontsource/fonts/fira-mono@latest/latin-700-normal.ttf",
    "SourceCodePro-Bold.ttf":
        "https://cdn.jsdelivr.net/fontsource/fonts/source-code-pro@latest/latin-700-normal.ttf",
    "IBMPlexMono-Bold.ttf":
        "https://cdn.jsdelivr.net/fontsource/fonts/ibm-plex-mono@latest/latin-700-normal.ttf",
}


def download(url: str, dest: Path) -> None:
    if dest.exists():
        print(f"[skip] {dest.name} already present")
        return
    # Reject anything that isn't an https URL (file://, http://, custom schemes).
    # The FONTS map is hardcoded https; this guards against future edits.
    if not url.startswith("https://"):
        raise ValueError(f"refusing non-https URL: {url}")
    print(f"[get ] {dest.name}")
    req = urllib.request.Request(url, headers={"User-Agent": "qte77-fonts/1.0"})
    # B310: scheme guarded above; URLs are hardcoded https constants
    with urllib.request.urlopen(req, timeout=30) as r, dest.open("wb") as f:  # nosec B310
        f.write(r.read())


def download_from_zip(zip_url: str, member: str, dest: Path) -> None:
    if dest.exists():
        print(f"[skip] {dest.name} already present")
        return
    if not zip_url.startswith("https://"):
        raise ValueError(f"refusing non-https URL: {zip_url}")
    print(f"[zip ] {dest.name}")
    req = urllib.request.Request(zip_url, headers={"User-Agent": "qte77-fonts/1.0"})
    # B310: scheme guarded above; URL is hardcoded https constant
    with urllib.request.urlopen(req, timeout=60) as r:  # nosec B310
        data = r.read()
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        with zf.open(member) as src, dest.open("wb") as f:
            f.write(src.read())


def main() -> int:
    FONTS_DIR.mkdir(parents=True, exist_ok=True)
    try:
        for name, url in FONTS.items():
            download(url, FONTS_DIR / name)
        for name, (zip_url, member) in ZIPPED_FONTS.items():
            download_from_zip(zip_url, member, FONTS_DIR / name)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(f"\nfonts installed to {FONTS_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
