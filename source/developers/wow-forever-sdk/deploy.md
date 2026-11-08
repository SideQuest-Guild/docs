# Release

The SDK is a package, so a release puts it on PyPI as [`wow`](https://pypi.org/project/wow/).

## Steps

1. Change `version` in `pyproject.toml`.
2. Move the Unreleased entries in `CHANGELOG.md` under the new version.
3. Merge to `main`. CI builds the package, checks it, and keeps it as an artifact with the name of the commit.
4. On that commit, publish a GitHub release with the tag `v<version>`.

`publish.yml` then downloads the artifact that CI built for that commit and checks its checksums. It publishes the
artifact to PyPI through Trusted Publishing. It does not build the package again, so PyPI gets the files that CI
tested.
