# Deploy

SideQuest Companion ships as a [GitHub release](https://github.com/SideQuest-Guild/companion/releases)
with one build per supported system.

## Release a new version

1. Build the changelog from the commits since the last tag:

   ```sh
   git cliff --tag v0.2.0 -o CHANGELOG.md
   git commit -am "docs: changelog for v0.2.0"
   ```

2. Tag and push the signed tag:

   ```sh
   git tag -s v0.2.0 -m "SideQuest Companion v0.2.0"
   git push origin main v0.2.0
   ```

Pushing a `v*` tag builds every platform's asset (Windows x86_64 and ARM, macOS universal, Linux
x86_64), writes that version's release notes with git-cliff, signs build provenance and a
software bill of materials (a signed list of exactly what went into the build) for each asset,
and publishes them as a GitHub release.

A published release's files can't be changed, and `v*` tags can't be moved or deleted. A bad
release is fixed by shipping a new version, not by editing the old one.

## Testing the release workflow without releasing

Run the workflow by hand from the Actions tab with the tag field left blank. It builds and signs
every asset using the version in the current `Cargo.toml`, and leaves a draft release named
`dry-run-<run id>` that you can delete afterward.

Running it by hand with an existing tag, such as `v0.1.0`, rebuilds and republishes that tag's
assets.

`main` only accepts signed commits, and force pushes and deleting the branch are blocked.

## Verifying a download

Anyone can check that a release asset really came from this repo:

```sh
gh attestation verify sidequest-companion-0.2.0-macos-universal.zip --repo SideQuest-Guild/companion
```

or against the published checksums:

```sh
sha256sum -c SHA256SUMS.txt
```

See the repo's `SECURITY.md` for what's in scope and how to report a problem privately.
