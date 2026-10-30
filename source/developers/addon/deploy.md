# Deploy

The addon ships as a signed zip on [CurseForge](https://www.curseforge.com/projects/1773662) and
as a [GitHub release](https://github.com/SideQuest-Guild/addon/releases). Both come from the same
build.

## Release a new version

1. Build the changelog from the commits since the last tag:

   ```sh
   git cliff --tag v0.2.0 -o CHANGELOG.md
   git commit -am "docs: changelog for v0.2.0"
   ```

2. Tag and push the signed tag:

   ```sh
   git tag -s v0.2.0 -m "SideQuest v0.2.0"
   git push origin main v0.2.0
   ```

Pushing a `v*` tag starts the release workflow. It writes that version's release notes with
[git-cliff](https://git-cliff.org/) (a tool that builds a changelog from commit messages; only
`feat`, `fix` and `perf` commits are listed), builds the zip, uploads it to CurseForge, signs
build provenance and a software bill of materials (a signed list of exactly what went into the
build) for it, and publishes it as a GitHub release.

A published release's files can't be changed, and `v*` tags can't be moved or deleted. A bad
release is fixed by shipping a new version, not by editing the old one.

## Testing the release workflow without releasing

Run the workflow by hand from the Actions tab with the tag field left blank. It builds and signs
the zip the same way, uploads nothing to CurseForge, and leaves a draft release named
`dry-run-<run id>` that you can delete afterward.

Running it by hand with an existing tag, such as `v0.1.0`, publishes that tag as a GitHub release
without uploading it to CurseForge again. This is for a version that's already on CurseForge but
has no GitHub release.

`main` only accepts signed commits, and force pushes and deleting the branch are blocked.
