# SideQuest Guild docs

A Sphinx site, built with the Shibuya theme and MyST Markdown, managed with uv. It pulls content
from `SideQuest-Guild/website`, `bot`, `addon` and `companion` at build time instead of copying
it; see `README.md` for how. `README.md` explains the repo to people; keep it current and in
plain words.

## Layout

- `repos.json`: the source repos this site pulls from, and how to generate each one's reference
  and changelog. One config, read by `fetch_sources.py`, every `generate_*.py` script, and CI.
- `scripts/`: `fetch_sources.py` clones/updates the repos in `repos.json` into `.sources/` (full
  history); `generate_developer_pages.py` turns their READMEs into developer pages;
  `generate_api_reference.py` fetches the website's live OpenAPI schema and writes its HTTP
  reference and data-model pages; `generate_bot_commands.py` reads the bot's slash commands with
  `ast`; `generate_addon_reference.py` reads the addon's `/sq` commands from its Lua source and
  the SQX1/SQI1 formats from the website's own pydantic models; `generate_companion_reference.py`
  runs `cargo doc --no-deps` over the companion app; `generate_changelogs.py` uses a repo's
  own `CHANGELOG.md` or runs `git-cliff` over its commit history with `scripts/cliff.toml`.
- `source/`: the Sphinx source. `conf.py` (theme options, nav, the per-page repo-card/edit-link
  hook), `index.md` (the landing page), `members/`, `officers/`, `developers/`, `reference/`,
  `changelog/`, `contributing/`. Anything under a `_generated/` folder is written by a script and
  gitignored; don't edit it by hand. `reference/_generated/python/` is written by
  `sphinx-autoapi`, configured in `conf.py`, not a standalone script.
- `source/_templates/sidebars/edit-this-page.html` overrides Shibuya's built-in version: Shibuya's
  own "Edit this page" link is baked once from the static `html_context` and can't vary per page,
  so `conf.py`'s `html-page-context` hook sets `sq_edit_url`/`sq_edit_label` per page instead
  (handwritten pages point here, generated README pages point at the source repo's README,
  generated reference pages get no link).

## Working

- `make install`, then `make docs` (clones/updates sources, generates every page, builds with
  `-W` so warnings fail the build). `make serve` for live reload while writing. Needs `uv`,
  `git-cliff`, and `cargo` on `PATH`.
- Dependency versions in `pyproject.toml` are pinned exactly (`==`), not ranged; `astroid` is
  pinned below 4 because `sphinx-autoapi==3.6.0` doesn't support astroid 4's `AstroidBuilder` API
  change yet. Bump both together, deliberately, after checking `sphinx-autoapi`'s changelog.
- Commits are SSH-signed via 1Password. If signing fails, stop and report it; never disable
  signing.
- Conventional-commit subjects, written as plain-English sentences.
- This repo's `AGENTS.md` is covered by the global gitignore (it ignores `AGENTS.md`
  everywhere), so add it with `git add -f AGENTS.md`.

## Releases

This repo has no releases: every push to `main` publishes the site. The changelog pages come
from each app's `CHANGELOG.md`, which that app writes when it tags a release (see its
`AGENTS.md`). If an app's changelog shows everything under "Unreleased", that app needs a
release, not a fix here. After an app releases, `gh workflow run build.yml` shows it now
instead of at the daily 06:17 UTC build.

## Writing guides

- Plain words, short sentences, active voice, no jargon a common word would do instead, and no
  em dashes. Follow Orwell's six rules and ASD-STE100 Simplified Technical English for
  instructions; see `source/contributing/writing.md` for the full house style.
- Don't repeat facts, numbers, or rules that live on the main site or in a repo's README; link to
  them instead. They drift; a link doesn't.
- SQL is the loot system's name, SideQuest Loot, pronounced "squeel". Link the word "squeel" to
  <https://www.youtube.com/shorts/z5p-aMyfT98> the one time it appears, and don't repeat the link.
- Renown is the site's participation points; the EP/GP/PR system from the addon is SQL. Don't
  confuse the two.
- Never name the guild's leaders.

## Rules that bite

- The developer pages for website/bot/addon/companion are generated from those repos' own
  READMEs. Don't hand-edit `source/developers/_generated/*.md`; it's overwritten on every build.
  Fix the source repo's README instead, or fix the rewriting rules in
  `generate_developer_pages.py`.
- Every `_generated/` folder under `source/reference/` and `source/changelog/` is overwritten on
  every build by the matching `scripts/generate_*.py`. Don't hand-edit anything in one; fix the
  generator, or fix the app's own source/schema/docstrings.
- The HTTP API reference is generated from `https://sidequest-guild.com/schema/openapi.json` at
  build time. If that fetch fails, or the schema has no operations, the build must fail too
  (`generate_api_reference.py` exits non-zero) rather than shipping a stale or empty reference.
  The same "fail loudly, never ship empty" rule applies to every other generator for a `shipped:
  true` app; `shipped: false` (an app whose repo has no code yet) is the one case that gets an
  honest placeholder instead of a failure.
- The changelog generator needs each repo's full git history (`git-cliff` walks commit tags), so
  `fetch_sources.py` clones full and CI's `actions/checkout` for each source uses
  `fetch-depth: 0`. Don't reintroduce a shallow clone without also dropping changelog generation.
- Internal reference cross-links (operation pages linking to the HTTP API's Models page) use the
  MyST `` {ref}`text <label>` `` role, not a plain `[text](file.md#anchor)` link: a plain link's
  "local id" check runs before the whole document is parsed, so it false-positives on any forward
  reference (a model that links to one defined later in the same page). `{ref}` resolves after
  the full build, so order doesn't matter.
- Adding a future app is one entry in `repos.json` plus the stub pages described in `README.md`'s
  "Adding an app" section; don't add a placeholder page for one before its repo exists.
