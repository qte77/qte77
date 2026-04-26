# How to enumerate a gap and document an endpoint

Concise methodology for adding a new entry to [`INDEX.md`](INDEX.md) and,
when needed, a `<feature>.md` file describing an internal endpoint.

## Step 1 — Confirm the gap is real

Before writing anything, rule out that the API already supports it:

1. Search [GitHub's REST docs](https://docs.github.com/en/rest) for the
   feature name and the resource type
2. Search the [GraphQL schema reference](https://docs.github.com/en/graphql/reference)
   for matching queries and mutations
3. Run `gh api --help` and `gh <noun> --help` for the relevant noun
4. Check [`github/rest-api-description`](https://github.com/github/rest-api-description)
   for the canonical OpenAPI shape

If you find coverage, the gap isn't real. Stop.

## Step 2 — Find first-party evidence

Acceptable sources only:

- `docs.github.com` (any subpath)
- `github.com/orgs/community/discussions/*`
- `github.com/cli/cli/issues/*` and PRs
- `github.com/github/rest-api-description`
- `github.blog`

Acceptable evidence shapes:

- A staff member acknowledging the limitation in a community discussion
- An open feature-request discussion that hasn't been resolved
- An open `gh` CLI issue confirming the gap
- A comparison between GraphQL and REST mutation lists where one has
  the operation and the other doesn't

If you can't find first-party evidence, drop the candidate. Do not cite
Stack Overflow, Reddit, third-party tools, or blog posts.

## Step 3 — Add to INDEX.md

Append a row with:

- One-liner of the missing capability
- UI path the user actually clicks
- Which surface(s) lack it (REST / GraphQL / gh / all)
- Evidence URLs (markdown links, first-party only)
- Pointer to detail file or `tbd`

## Step 4 — Optional: capture the internal endpoint

Only if you need to script around the gap. Otherwise stop at step 3.

1. Open Chrome DevTools → Network tab on a logged-in browser, on a repo
   you own
2. Filter to `Doc` and `Fetch/XHR`
3. Trigger the UI action once
4. Identify the request that effects the change (usually a POST on the
   same domain as the UI, not `api.github.com`)
5. Note: method, URL, request `Content-Type`, request body shape
   (multipart, urlencoded, JSON), response status, response location
   header
6. Save the HAR if useful, but **strip cookies before keeping the file**
7. Inspect the form on the Settings page (or wherever the action lives)
   to find the action URL and CSRF field — these are the values your
   script should discover at runtime, not hardcode

## Step 5 — Write `<feature>.md`

Use [`social-preview.md`](social-preview.md) as the template. Lead with
a disclaimer that this is reverse-engineering, not GitHub
documentation. Separate confident claims from inferences. Include:

- Why no public API exists (cite step-2 evidence)
- Auth model (cookie vs. token)
- Step-by-step request shape
- Expected response statuses
- What can change without notice

## Step 6 — Update the script (if any)

Scripts must parse the live form at runtime so they survive minor
shape changes. The `<feature>.md` file is a snapshot to update if the
script ever logs values that differ from what's documented.

## Scope rules

- Own resources only. Don't probe endpoints under accounts you don't
  control.
- Reads first. Test reads before writes.
- No mass operations. One-off per repo or per setting, not loops over
  many targets.
- Don't share session cookies or commit them anywhere.
