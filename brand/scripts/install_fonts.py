# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Download Inter and JetBrains Mono fonts into brand/fonts/.

Both are SIL OFL 1.1 licensed and free to redistribute.
"""

from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

FONTS_DIR = Path(__file__).resolve().parent.parent / "fonts"

FONTS = {
    "Inter-Bold.ttf":
        "https://cdn.jsdelivr.net/fontsource/fonts/inter@latest/latin-700-normal.ttf",
    "Inter-Regular.ttf":
        "https://cdn.jsdelivr.net/fontsource/fonts/inter@latest/latin-400-normal.ttf",
    "JetBrainsMono-Regular.ttf":
        "https://cdn.jsdelivr.net/fontsource/fonts/jetbrains-mono@latest/latin-400-normal.ttf",
    "JetBrainsMono-Bold.ttf":
        "https://cdn.jsdelivr.net/fontsource/fonts/jetbrains-mono@latest/latin-700-normal.ttf",
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


def main() -> int:
    FONTS_DIR.mkdir(parents=True, exist_ok=True)
    try:
        for name, url in FONTS.items():
            download(url, FONTS_DIR / name)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(f"\nfonts installed to {FONTS_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
