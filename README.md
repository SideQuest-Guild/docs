# SideQuest Guild docs

The documentation site for SideQuest, an Alliance guild on World of Warcraft: Forever. It runs at
[docs.sidequest-guild.com](https://docs.sidequest-guild.com) and covers the
[website](https://github.com/SideQuest-Guild/website), the
[Discord bot](https://github.com/SideQuest-Guild/bot), and the
[in-game addon](https://github.com/SideQuest-Guild/addon).

This repo doesn't copy content from those repos. It pulls their READMEs in at build time and
generates the API reference from the website's live OpenAPI schema, so the docs can't drift out
of sync with the code.

## Building it

You need [uv](https://docs.astral.sh/uv/).

```sh
make docs
```

This clones or updates the other repos into `.sources/`, generates the developer pages and API
reference, then builds the site into `_build/html` with Sphinx, treating warnings as errors.

To write with live reload:

```sh
make serve
```

## Adding a repo

Add one entry to `repos.json` with the repo's `id`, its `SideQuest-Guild/<name>` path, a title, a
short summary, and the path to its README. Then add a matching stub page under
`source/developers/<id>.md`:

```md
```{include} _generated/<id>.md
```
```

and list it in the `toctree` at the bottom of `source/developers/index.md`. `make docs` picks up
the new repo on the next build; CI does too, since both read `repos.json`.

## Where things are

| Path | What's in it |
|---|---|
| `repos.json` | The repos this site pulls from. Both `make docs` and CI read it. |
| `scripts/fetch_sources.py` | Clones or updates the repos listed in `repos.json` into `.sources/`. |
| `scripts/generate_developer_pages.py` | Turns each repo's README into a developer page, with links and images rewritten to point at GitHub. |
| `scripts/generate_api_reference.py` | Fetches the website's OpenAPI schema and writes a Markdown page per tag. |
| `source/` | The Sphinx site: `index.md` (Home), `members.md`, `officers.md`, `developers/`, `api/`. |
| `.github/workflows/build.yml` | Builds and deploys the site to GitHub Pages. |

## Deploying

Pushing to `main` builds and deploys to GitHub Pages. The workflow also runs on a daily schedule,
on `workflow_dispatch`, and on a `repository_dispatch` of type `docs`, so another repo can trigger
a rebuild later. The build uses `-W`, so a broken link or a failed schema fetch fails the run
instead of shipping bad docs.
