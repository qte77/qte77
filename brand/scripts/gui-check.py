#!/usr/bin/env python3
"""gui-check.py — the qte77 check-and-fetch UI verifier (dual-scope).

Runs over polyfetch-scrape's bundled Patchright — the single shared browser stack, no
per-repo install. Recommended (OPTIONAL, not a required CI gate) to check & fetch a
qte77-branded UI headlessly, early — before real users hit the page. See
brand/ui-kit/ci-verify.example.yml to opt into CI.

Two scopes, one codebase:
  * single-repo / in-project:  gui-check.py --url http://localhost:8137
  * cross-repo / multi-project: gui-check.py --urls urls.txt   (drift sweep)

The cross-repo sweep audits each deployed UI's *live computed tokens* against the canonical
EyeRest set (synced from brand/DESIGN.md) — this is what establishes the baseline and
prevents drift. It is the GUI analogue of repo-baseline's audit.sh.

Run via the shared env:
  uv run --directory /workspaces/qte77/polyfetch-scrape patchright install chromium   # once
  uv run --directory /workspaces/qte77/polyfetch-scrape python gui-check.py --url <url>

Gotchas honored (see findings/04): SwiftShader flags for headless WebGL; do NOT nest
sync_playwright() with polyfetch's attempt(); a reachable 200 page needs Patchright (not
fetch()) to execute JS.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from patchright.sync_api import sync_playwright

# Canonical EyeRest tokens — SYNCED from brand/DESIGN.md (single source of truth, D5).
# gui-baseline regenerates this block from DESIGN.md; do not hand-edit independently.
CANONICAL = {
    "light": {
        "--bg": "#ece8d8", "--surface": "#e2dec8", "--border": "#c8c4b0",
        "--text": "#2c2818", "--text-muted": "#686040",
        "--primary": "#7a6010", "--primary-on": "#ece8d8",
        "--data-positive": "#4a6818", "--data-caution": "#787010",
        "--data-negative": "#983828", "--data-alt": "#587818",
    },
    "dark": {
        "--bg": "#1c1a14", "--surface": "#242018", "--border": "#383428",
        "--text": "#d8d0b8", "--text-muted": "#a89878",
        "--primary": "#c8a858", "--primary-on": "#1c1a14",
        "--data-positive": "#8aa860", "--data-caution": "#c8b868",
        "--data-negative": "#c08060", "--data-alt": "#a8b870",
    },
}

# Headless Chromium has no GPU → SwiftShader. WebGL canvases need these or the context is
# lost and the screenshot is blank. Harmless for 2D canvas / DOM-only pages.
LAUNCH_ARGS = ["--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"]


def _norm(v: str) -> str:
    return (v or "").strip().lower()


def audit_tokens(page, theme: str) -> list[str]:
    """Force a scheme, read the live computed tokens, diff against canonical. -> failures."""
    page.evaluate("t => document.documentElement.setAttribute('data-theme', t)", theme)
    names = list(CANONICAL[theme].keys())
    computed = page.evaluate(
        """names => {
            const s = getComputedStyle(document.documentElement);
            const o = {};
            for (const n of names) o[n] = s.getPropertyValue(n);
            return o;
        }""",
        names,
    )
    fails = []
    for n, expected in CANONICAL[theme].items():
        got = _norm(computed.get(n, ""))
        if got != _norm(expected):
            fails.append(f"[{theme}] {n}: expected {expected}, got {got or '(unset)'}")
    return fails


def check_a11y(page) -> list[str]:
    """Theme control must have a dynamic accessible name + a live-region announce."""
    fails = []
    info = page.evaluate(
        """() => {
            const b = document.getElementById('theme-toggle');
            const s = document.getElementById('theme-status');
            return {
                hasBtn: !!b,
                label: b ? (b.getAttribute('aria-label') || '') : '',
                hasLive: !!s && s.getAttribute('aria-live') === 'polite',
            };
        }"""
    )
    if not info["hasBtn"]:
        fails.append("a11y: #theme-toggle missing")
    elif "theme" not in info["label"].lower():
        fails.append(f"a11y: #theme-toggle aria-label not descriptive ({info['label']!r})")
    if not info["hasLive"]:
        fails.append("a11y: #theme-status aria-live=polite region missing")
    return fails


def check_fonts(page) -> list[str]:
    ok = page.evaluate(
        """async () => {
            await document.fonts.ready;
            return document.fonts.check('400 16px Inter')
                && document.fonts.check('700 16px Inter');
        }"""
    )
    return [] if ok else ["fonts: Inter 400/700 not loaded (document.fonts.check failed)"]


def check_favicon(page) -> list[str]:
    try:
        status = page.evaluate(
            "async () => (await fetch('favicon.svg', {method:'GET'})).status"
        )
    except Exception:
        return ["favicon: fetch threw (favicon.svg unreachable)"]
    return [] if status == 200 else [f"favicon: favicon.svg returned {status}"]


def check_webgl(page) -> list[str]:
    info = page.evaluate(
        """() => {
            const c = document.querySelector('canvas');
            if (!c) return {canvas: false};
            const gl = c.getContext('webgl2') || c.getContext('webgl');
            if (!gl) return {canvas: true, gl: false};
            return {canvas: true, gl: true,
                    lost: gl.isContextLost(),
                    pointRange: gl.getParameter(gl.ALIASED_POINT_SIZE_RANGE)};
        }"""
    )
    if not info.get("canvas"):
        return []  # not a canvas GUI — skip
    if not info.get("gl"):
        return ["webgl: canvas present but no WebGL context"]
    if info.get("lost"):
        return ["webgl: context lost (missing --enable-unsafe-swiftshader?)"]
    return []


def check_url(pw, url: str, out_dir: Path, *, webgl: bool) -> list[str]:
    """Run the full gate against one URL. Returns a list of failure strings."""
    fails: list[str] = []
    browser = pw.chromium.launch(headless=True, args=LAUNCH_ARGS)
    try:
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto(url, wait_until="networkidle")

        for theme in ("light", "dark"):
            fails += audit_tokens(page, theme)
            shot = out_dir / f"{_slug(url)}-{theme}.png"
            page.screenshot(path=str(shot), full_page=False)

        fails += check_a11y(page)
        fails += check_fonts(page)
        fails += check_favicon(page)
        if webgl:
            fails += check_webgl(page)
    finally:
        browser.close()
    return fails


def _slug(url: str) -> str:
    return "".join(c if c.isalnum() else "-" for c in url).strip("-")[:60]


def _load_urls(args) -> list[str]:
    if args.url:
        return [args.url]
    if args.urls:
        p = Path(args.urls)
        if p.exists():
            return [ln.strip() for ln in p.read_text().splitlines() if ln.strip()]
        return [u.strip() for u in args.urls.split(",") if u.strip()]
    return []


def main() -> int:
    ap = argparse.ArgumentParser(description="qte77 GUI pre-user check-and-fetch gate")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--url", help="single-repo / in-project: one URL (e.g. localhost)")
    g.add_argument("--urls", help="cross-repo: a file (one URL/line) or comma list")
    ap.add_argument("--org", help="(future) resolve deployed URLs from orgs/<org>.yaml")
    ap.add_argument("--out", default="gui-check-out", help="screenshot output dir")
    ap.add_argument("--webgl", action="store_true", help="also run WebGL sanity")
    args = ap.parse_args()

    if args.org:
        print("note: --org resolution from orgs/<org>.yaml is a gui-baseline tool;",
              "pass --urls with the deployed URLs for now.", file=sys.stderr)

    urls = _load_urls(args)
    if not urls:
        print("error: no URLs to check", file=sys.stderr)
        return 2

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    total_fails = 0
    # ONE sync_playwright context for the whole run — never nest it with attempt().
    with sync_playwright() as pw:
        for url in urls:
            print(f"\n=== {url} ===")
            fails = check_url(pw, url, out_dir, webgl=args.webgl)
            if fails:
                total_fails += len(fails)
                for f in fails:
                    print(f"  FAIL  {f}")
            else:
                print("  OK    tokens · a11y · fonts · favicon"
                      + (" · webgl" if args.webgl else ""))

    print(f"\n{'DRIFT' if total_fails else 'CLEAN'}: "
          f"{total_fails} failure(s) across {len(urls)} URL(s). "
          f"Screenshots in {out_dir}/")
    return 1 if total_fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
