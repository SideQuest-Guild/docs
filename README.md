# SideQuest Guild docs

The documentation site for SideQuest, an Alliance guild on World of Warcraft: Forever. It runs at
[docs.sidequest-guild.com](https://docs.sidequest-guild.com) and covers the
[website](https://github.com/SideQuest-Guild/website), the
[Discord bot](https://github.com/SideQuest-Guild/bot), the
[in-game addon](https://github.com/SideQuest-Guild/addon), and the
[companion app](https://github.com/SideQuest-Guild/companion).

This repo doesn't copy content from those repos. It pulls their READMEs in at build time and
generates every reference and changelog from the apps' own live schema, source and commit
history, so the docs can't drift out of sync with the code.

## Building it

You need [uv](https://docs.astral.sh/uv/). `git-cliff` and
`cargo` need to be on `PATH` too (installed automatically in CI).

```sh
make docs
```

This clones or updates the other repos into `.sources/` (with full history, not a shallow clone:
the changelog generator needs it), generates every developer page, reference and changelog, then
builds the site into `_build/html` with Sphinx, treating warnings as errors.

To write with live reload:

```sh
make serve
```

## Adding an app

1. Add one entry to `repos.json`: `id`, its `SideQuest-Guild/<name>` path, a `title`, a `summary`,
   `readme_path`, `shipped` (`false` if the repo has no code yet), `changelog.path` (its own
   `CHANGELOG.md`, if it keeps one), and a `reference` block describing how to generate its
   reference (`http`/`python` for a web API and Python packages, `commands` for a bot-style
   slash-command source dir, `lua` for the addon-style source dir, `rust` for a Cargo crate).
2. Add a stub page under `source/developers/<id>/index.md` with the matching
   `readme.md`/`run-locally.md`/`test.md`/`how-it-works.md`/`deploy.md` siblings, and a
   `source/reference/<id>/index.md` and `source/changelog/<id>.md`.
3. List the new pages in `source/developers/index.md`'s toctree, `source/reference/index.md`'s
   toctree, and `source/changelog/index.md`'s toctree, and add the app to the `Develop` and
   `Changelogs` nav dropdowns in `source/conf.py`.
4. If the app needs a new kind of generated reference (not HTTP/Python/Lua/Rust), add a
   `scripts/generate_<app>_reference.py` following the pattern of the existing ones: read
   `repos.json`, read from `.sources/<id>`, fail loudly (non-zero exit) if the source exists but
   can't be read, write an honest placeholder instead of failing if `shipped` is `false`.

`make docs` picks up the new repo on the next build; CI does too, since both read `repos.json`.

## Where things are

| Path | What's in it |
|---|---|
| `repos.json` | The repos this site pulls from, and how to generate each one's reference and changelog. Both `make docs` and CI read it. |
| `scripts/fetch_sources.py` | Clones or updates the repos in `repos.json` into `.sources/`, full history. |
| `scripts/generate_developer_pages.py` | Turns each repo's README into a developer page. |
| `scripts/generate_api_reference.py` | Fetches the website's live OpenAPI schema and writes its HTTP reference and data-model pages, grouped by `x-tagGroups` when present. |
| `scripts/generate_bot_commands.py` | Reads the bot's slash commands from its source with `ast` (no import needed). |
| `scripts/generate_addon_reference.py` | Reads the addon's `/sq` commands from its Lua source, and the SQX1/SQI1 formats from the website's own pydantic models. |
| `scripts/generate_companion_reference.py` | Runs `cargo doc --no-deps` over the companion app and links its Rust reference. |
| `scripts/generate_changelogs.py` | Uses a repo's own `CHANGELOG.md` if it has one, otherwise runs `git-cliff` over its commit history with `scripts/cliff.toml`. |
| `source/` | The Sphinx source: `index.md` (the landing page), `members/`, `officers/`, `developers/`, `reference/`, `changelog/`, `contributing/`. Anything under a `_generated/` folder is written by a script and gitignored; don't edit it by hand. |
| `source/conf.py` | Theme options, the nav/sidebar, and the `html-page-context` hook that sets the repo card and "Edit this page" link per page. |
| `.github/workflows/build.yml` | Builds and deploys the site to GitHub Pages. |

## Deploying

Pushing to `main` builds and deploys to GitHub Pages. The workflow also runs on a daily schedule,
on `workflow_dispatch`, and on a `repository_dispatch` of type `docs`, so another repo can trigger
a rebuild later. The build uses `-W`, so a broken link, a failed schema fetch, or a generator that
can't read a shipped app's source fails the run instead of shipping bad or empty docs.

## Writing for these docs

Every page here, and across the main site, follows the same plain-language rules: Orwell's six
rules, ASD-STE100 Simplified Technical English for instructions, no AI writing habits (no em
dashes, no "delve"/"seamless"/"robust" word-soup, no marketing). See
[`source/contributing/writing.md`](source/contributing/writing.md) for the full list.
