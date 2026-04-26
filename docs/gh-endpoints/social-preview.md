# GitHub social preview upload — endpoint reverse-engineering

> **This is a reverse-engineering snapshot, not GitHub documentation.**
> GitHub publishes no specification for this endpoint. Everything below
> is inferred from inspecting the live Settings page form, Rails web-app
> conventions, and prior community reverse-engineering. The live form
> is the source of truth — `brand/scripts/upload_social_preview.py` parses
> the actual form action URL and CSRF token at runtime rather than
> trusting hardcoded paths. If the script logs different values than
> this document describes, **update the document**.

GitHub provides **no public API** for setting a repository's social
preview image. The Settings UI is the only supported mechanism. This
document records the undocumented internal endpoint that the UI uses,
so that `brand/scripts/upload_social_preview.py` can call it directly.

> **Use at your own risk.** This endpoint is not part of the GitHub
> REST/GraphQL API. It can change shape, move, or start enforcing
> additional bot protections without notice. If the script breaks, the
> endpoint structure has likely shifted — re-inspect the UI form and
> update the parser. Manual UI upload remains the supported fallback.

## What this document claims with confidence

- The endpoint exists (the UI demonstrably calls *something*)
- Auth is via session cookie, not personal access token (verifiable —
  PATs return 302 to login)
- CSRF protection via hidden form field (standard Rails)
- READ endpoints exist publicly: GraphQL `openGraphImageUrl` and REST
  `social_preview_image_url`

## What this document is guessing (verify against the live form)

- Exact action URL path (likely `/<owner>/<repo>/edit_open_graph_image`)
- Exact field names (likely `repository[open_graph_image]` and
  `authenticity_token`)
- Response status code semantics (302 redirect = success is
  best-effort interpretation)

## Why no API?

Two long-standing community requests confirm the gap:

- [community#52294](https://github.com/orgs/community/discussions/52294) — feature request
- [community#172072](https://github.com/orgs/community/discussions/172072) — explicit "no endpoint exists"

Read access exists in two forms:

- GraphQL: `Repository.openGraphImageUrl`
- REST: `GET /repos/{owner}/{repo}` returns `social_preview_image_url`

Both return a CDN URL like `https://opengraph.githubassets.com/<hash>/<owner>/<repo>`.
The actual PNG/JPG bytes are stored on GitHub's CDN, not in the repo.

## Authentication

The Settings UI uses **session-cookie auth**, not the GitHub API. A
personal access token (`gho_...`, `ghp_...`) does NOT work for this
endpoint — it returns 302 to login.

You need the value of the `user_session` cookie from your authenticated
browser session.

### Extracting the cookie

1. Log into GitHub in your browser
2. Open DevTools → Application tab (Chrome) or Storage tab (Firefox)
3. Cookies → `https://github.com`
4. Find row `user_session`, copy the `Value` column
5. Treat it like a password — same level of access as your logged-in browser

The cookie expires per GitHub's session policy (typically ~14 days of
inactivity). If you get a 302 redirect to `/login` from the script,
re-extract.

## Endpoint mechanics

### Step 1 — fetch the settings page

```
GET https://github.com/<owner>/<repo>/settings
Cookie: user_session=<value>; __Host-user_session_same_site=<value>
```

Status 200 with HTML. If 302 → cookie invalid. If 404 → repo not found
or no admin access.

### Step 2 — parse the form

The Settings page contains a form with `enctype="multipart/form-data"`
that includes a file input named `repository[open_graph_image]`. The
form has:

- **action** — typically `/<owner>/<repo>/edit_open_graph_image`
  (relative URL on `https://github.com`)
- a hidden `<input name="authenticity_token" value="...">` (CSRF token,
  unique per page load and tied to the session)
- the file input, which accepts PNG / JPG / GIF up to 1 MB

### Step 3 — upload

```
POST <action>
Cookie: user_session=<value>; __Host-user_session_same_site=<value>
Origin: https://github.com
Referer: https://github.com/<owner>/<repo>/settings
Content-Type: multipart/form-data; boundary=...

--boundary
Content-Disposition: form-data; name="authenticity_token"

<token from form>
--boundary
Content-Disposition: form-data; name="_method"

patch
--boundary
Content-Disposition: form-data; name="repository[open_graph_image]"; filename="<name>.png"
Content-Type: image/png

<binary>
--boundary--
```

The `_method=patch` field is a Rails convention — the underlying route
is a PATCH, but browsers can only POST multipart forms, so Rails
overrides via this hidden field.

### Expected response

| Status | Meaning |
|---|---|
| 302 / 303 redirect to `/<owner>/<repo>/settings` | Likely success |
| 200 with HTML form re-rendered | Validation error (file too large, wrong type, CSRF mismatch) |
| 422 | CSRF token rejected or file rejected by server validation |
| 401 / 302 to `/login` | Cookie invalid or expired |
| 404 | Repo not found or no admin permission |

There is no JSON success body — the UI relies on the redirect-to-settings
pattern. To **confirm** the upload took effect, GET the public REST API:

```
GET https://api.github.com/repos/<owner>/<repo>
```

and read `social_preview_image_url`. The CDN URL changes after upload
(propagation typically <30s).

## What can change without notice

Any of these would break the script:

- Form action URL path (`/edit_open_graph_image` → something else)
- Field names (`repository[open_graph_image]` → e.g. `og_image`)
- CSRF mechanism (currently hidden form field; could move to header-only)
- Required cookies (a third cookie name might appear)
- Bot detection / rate limiting on the route
- Required headers like `X-CSRF-Token` becoming mandatory

The script discovers the form action and CSRF token at runtime rather
than hardcoding them, which gives some resilience to action-URL changes
but doesn't help if the field-name or cookie shape shifts.

## Verification flow

After upload, check propagation:

```bash
uv run brand/scripts/upload_social_preview.py qte77/qte77 --verify-only
```

This calls the public REST endpoint and prints the CDN URL. Open it in
a browser to confirm the new image is being served.

For external rendering check (Twitter/Slack/Discord card preview):

- https://www.opengraph.xyz/url/https%3A%2F%2Fgithub.com%2Fqte77%2Fqte77
- Slack: paste the repo URL into a channel, the unfurl shows current OG image
- Twitter/X: paste into a draft tweet (don't post)

## Scope and ethics

This script is intended for:

- ✅ Repos you own or have admin access to
- ✅ Your own session cookie
- ✅ Routine branding work (single-developer / small-org scope)

It is **not** for:

- ❌ Repos you don't control
- ❌ Hijacked sessions or shared cookies
- ❌ Mass-uploading to many repos (would trigger rate limiting / bot detection
  even if technically allowed)

The endpoint exists to support the official UI. Using it programmatically
for your own admin tasks is consistent with intent. Probing it at scale,
or sharing cookies, is not.
