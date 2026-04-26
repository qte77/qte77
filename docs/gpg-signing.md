# GPG Signing — Policy

Every commit across the qte77 ecosystem must be GPG-signed. This applies to
human and agent commits alike, in any repo (workspace meta, orchestrators,
plugin sources, sibling consumers).

## Required global git config

```ini
[commit]
    gpgsign = true
[gpg]
    format = openpgp
```

These values must be set globally — `git config --global commit.gpgsign true`
and `git config --global gpg.format openpgp`. Repo-local overrides are not
expected; if you find one, treat it as drift.

## Two setup paths

### Codespaces

GPG signing in Codespaces can be auto-configured when the user-level setting
**Codespaces → Trusted repositories** is set to **All repositories**. With that
enabled, GitHub provisions the gpg binary + agent, and the global config above
is written automatically at container creation.

**Caveat:** if the trust toggle is flipped *after* a Codespace already exists,
or for sibling repos cloned into an existing Codespace, the config isn't
guaranteed. The durable fix is to write the two config lines from the
container's setup hook — see polyforge-orchestrator for the canonical Makefile
target that does this.

### Local development

1. Generate a key:

    ```bash
    gpg --full-generate-key
    ```

    Choose RSA 4096 (or ECC), set an expiration, use the email address
    associated with your GitHub account.

2. List the secret key and copy the long key ID:

    ```bash
    gpg --list-secret-keys --keyid-format=long
    ```

3. Export the public key and upload to GitHub → Settings → SSH and GPG keys:

    ```bash
    gpg --armor --export <KEY_ID>
    ```

4. Configure git globally:

    ```bash
    git config --global commit.gpgsign true
    git config --global gpg.format openpgp
    git config --global user.signingkey <KEY_ID>
    ```

5. Verify a fresh commit is signed (see below).

## Verification

After setup, every commit you make should pass:

```bash
git verify-commit HEAD
```

GitHub will display a **Verified** badge next to commits with a valid signature
matching an uploaded key.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `gpg: signing failed: Inappropriate ioctl for device` | No TTY available to gpg-agent | `export GPG_TTY=$(tty)` in your shell rc |
| `error: gpg failed to sign the data` | Wrong key selected, or no default key | Set `user.signingkey` to the correct ID |
| Codespace commits unsigned | Trust toggle flipped after container creation, or sibling repo | Run the two `git config --global` lines manually, or rebuild the Codespace |
| `gpg-agent` prompts for passphrase repeatedly | Cache timeout too short | Configure `default-cache-ttl` in `~/.gnupg/gpg-agent.conf` |

## Authority

This is policy. The implementation mechanism (where the config gets written
during Codespace boot) lives in the orchestrator repos. See
`polyforge-orchestrator/Makefile` (`setup_gh_auth` target) for the durable
write that closes the trust-toggle gap.
