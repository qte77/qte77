# /// script
# requires-python = ">=3.11"
# dependencies = ["requests>=2.31"]
# ///
"""Upload a social preview image to a GitHub repo via the undocumented
internal endpoint used by the Settings UI.

EXPERIMENTAL — this hits a non-public endpoint. GitHub can change the
form structure or response shape at any time without notice. If this
script breaks, fall back to the manual UI upload (Settings -> General
-> Social preview).

GitHub provides no public REST/GraphQL API for setting the social
preview, only for reading it (`openGraphImageUrl` in GraphQL,
`social_preview_image_url` in REST). See:
https://github.com/orgs/community/discussions/52294
https://github.com/orgs/community/discussions/172072

Authentication: requires the user_session cookie from your authenticated
browser session — a personal access token does NOT work because this
endpoint is part of the web UI, not the API. See docs/gh-endpoints/social-preview.md
for how to extract the cookie.

Usage:
    export GH_USER_SESSION="<value of user_session cookie>"
    uv run scripts/upload_social_preview.py qte77/qte77 dist/qte77-social.png

    # then verify
    uv run scripts/upload_social_preview.py qte77/qte77 --verify-only
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

import requests

UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)


def session_from_cookie(cookie: str) -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Accept": "text/html,application/xhtml+xml"})
    s.cookies.set("user_session", cookie, domain="github.com")
    s.cookies.set("__Host-user_session_same_site", cookie, domain="github.com", secure=True)
    return s


def fetch_settings_page(s: requests.Session, repo: str) -> str:
    url = f"https://github.com/{repo}/settings"
    r = s.get(url, allow_redirects=False)
    if r.status_code in (301, 302):
        sys.exit(
            f"redirected to {r.headers.get('Location')!r} — "
            f"cookie likely expired or wrong account. status={r.status_code}"
        )
    if r.status_code == 404:
        sys.exit(f"404 on {url} — repo doesn't exist or you lack admin access")
    r.raise_for_status()
    return r.text


def parse_form(html: str) -> dict:
    """Locate the social-preview form and extract its action URL + CSRF token.

    The form is the one whose enctype is multipart/form-data and which contains
    a file input named 'repository[open_graph_image]'.
    """
    form_match = re.search(
        r'<form[^>]*action="([^"]+)"[^>]*enctype="multipart/form-data"[^>]*>'
        r'(.*?)</form>',
        html,
        re.DOTALL,
    )
    if not form_match:
        sys.exit("could not locate multipart form on settings page")

    candidates = re.findall(
        r'<form[^>]*action="([^"]+)"[^>]*>([^\0]*?)</form>',
        html,
    )
    target_form = None
    for action, body in candidates:
        if "open_graph_image" in body:
            target_form = (action, body)
            break
    if not target_form:
        sys.exit("could not find social-preview form on settings page")

    action, body = target_form
    token_match = re.search(
        r'name="authenticity_token"[^>]*value="([^"]+)"', body
    )
    if not token_match:
        sys.exit("authenticity_token not found in form")
    return {
        "action": action if action.startswith("http") else f"https://github.com{action}",
        "token": token_match.group(1),
    }


def upload(s: requests.Session, action: str, token: str, image: Path, repo: str) -> None:
    files = {
        "authenticity_token": (None, token),
        "_method": (None, "patch"),
        "repository[open_graph_image]": (image.name, image.read_bytes(), "image/png"),
    }
    headers = {
        "Referer": f"https://github.com/{repo}/settings",
        "Origin": "https://github.com",
    }
    r = s.post(action, files=files, headers=headers, allow_redirects=False)
    print(f"POST {action} -> {r.status_code}")
    if r.status_code in (302, 303):
        loc = r.headers.get("Location", "")
        print(f"  redirect: {loc}")
        # success looks like a redirect back to /settings
        if repo in loc and "settings" in loc:
            print("  status: likely success (redirect to settings page)")
        else:
            print("  status: unexpected redirect target")
    elif r.status_code == 200:
        # form often re-renders on validation error
        print("  status: 200 (may indicate validation error — check manually)")
    elif r.status_code == 422:
        sys.exit(f"422 — likely invalid file or CSRF token mismatch. body[:300]={r.text[:300]!r}")
    else:
        sys.exit(f"unexpected status {r.status_code}. body[:300]={r.text[:300]!r}")


def verify(repo: str) -> None:
    """Read back the public OG image URL via REST."""
    api = f"https://api.github.com/repos/{repo}"
    r = requests.get(api, headers={"User-Agent": UA, "Accept": "application/vnd.github+json"})
    r.raise_for_status()
    data = r.json()
    url = data.get("social_preview_image_url") or data.get("custom_properties", {}).get("og")
    print(f"social_preview_image_url: {url}")
    print("(may take ~30s to update after upload)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("repo", help="owner/repo, e.g. qte77/qte77")
    ap.add_argument("image", nargs="?", type=Path, help="path to PNG/JPG/GIF")
    ap.add_argument("--verify-only", action="store_true",
                    help="skip upload, just read back the current OG image URL")
    args = ap.parse_args()

    if args.verify_only:
        verify(args.repo)
        return 0

    if not args.image:
        sys.exit("image path required unless --verify-only")
    if not args.image.exists():
        sys.exit(f"file not found: {args.image}")

    cookie = os.environ.get("GH_USER_SESSION")
    if not cookie:
        sys.exit(
            "set GH_USER_SESSION env var to your user_session cookie value\n"
            "see docs/gh-endpoints/social-preview.md for how to extract it"
        )

    s = session_from_cookie(cookie)
    print(f"fetching settings page for {args.repo} ...")
    html = fetch_settings_page(s, args.repo)
    form = parse_form(html)
    print(f"form action: {form['action']}")
    print(f"csrf token : {form['token'][:20]}...")
    print(f"uploading  : {args.image} ({args.image.stat().st_size} bytes)")
    upload(s, form["action"], form["token"], args.image, args.repo)
    print("\nverifying via REST API ...")
    verify(args.repo)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
