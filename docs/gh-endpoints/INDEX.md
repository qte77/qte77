# Confirmed gaps in GitHub's public APIs

Each row is a capability the web UI offers that REST, GraphQL, and/or
`gh` CLI do not. Evidence URLs are first-party only (`docs.github.com`,
`github.com/orgs/community/discussions`, `github.com/cli/cli/issues`,
`github.com/github/rest-api-description`).

| #  | Capability | UI path | Missing in | Evidence | Detail |
| -- | ---------- | ------- | ---------- | -------- | ------ |
| 1 | Set repository social preview image | Settings → General → Social preview | REST, GraphQL, gh | [community#172072](https://github.com/orgs/community/discussions/172072), [community#52294](https://github.com/orgs/community/discussions/52294) | [social-preview.md](social-preview.md) |
| 2 | Star lists: create, assign repos, delete | `/{user}?tab=stars` → Lists | REST (all), GraphQL (writes), gh | [community#8293](https://github.com/orgs/community/discussions/8293), [community#38693](https://github.com/orgs/community/discussions/38693), [cli/cli#13226](https://github.com/cli/cli/issues/13226) | tbd |
| 3 | Upload user profile avatar | `/settings/profile` → Change avatar | REST, GraphQL | [community#65206](https://github.com/orgs/community/discussions/65206) | tbd |
| 4 | Set profile status | Profile menu → Set status | REST only (GraphQL has `changeUserStatus`) | [community#108473](https://github.com/orgs/community/discussions/108473) | tbd |
| 5 | Pin/unpin items on user profile | Profile → Customize your pins | REST (all), GraphQL (writes) | [community#24696](https://github.com/orgs/community/discussions/24696), [GraphQL mutations ref](https://docs.github.com/en/graphql/reference/mutations) | tbd |
| 6 | Pin/unpin a discussion | Discussion kebab → Pin | REST, GraphQL, gh | [GraphQL mutations ref](https://docs.github.com/en/graphql/reference/mutations) (no `pinDiscussion`; contrast `pinIssue`) | tbd |
| 7 | Lock/unlock a discussion | Discussion sidebar → Lock | REST, GraphQL, gh | [GraphQL mutations ref](https://docs.github.com/en/graphql/reference/mutations) (`lockLockable` covers Issue/PR only) | tbd |

## Notes per row

- **Row 1** is the only one with a documented internal endpoint here.
  See [`social-preview.md`](social-preview.md) and the upload script
  in `brand/scripts/upload_social_preview.py`.
- **Row 2** is partial — read of list names/IDs works via GraphQL
  `viewer { lists }`; writes do not.
- **Row 4** is REST-only — workflows that already use GraphQL have a
  supported path.
- **Row 5** allows reading pins via `user { pinnedItems }` GraphQL
  query; setting/changing them is UI-only.
- **Row 7** verify against current `gh` CLI version before relying on
  the gap; some discussion-scoped commands have shifted.

## Out of scope (not gaps)

These were investigated and found to have public API coverage:

- Repository topics — `GET/PUT /repos/{owner}/{repo}/topics`
- Archive/unarchive — `PATCH /repos/{owner}/{repo}` `archived` field
- Template flag — `PATCH /repos/{owner}/{repo}` `is_template` field
- Pages custom domain — `PUT /repos/{owner}/{repo}/pages` `cname` field
