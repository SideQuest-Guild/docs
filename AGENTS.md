# SideQuest Guild docs

A Sphinx site, built with the Shibuya theme and MyST Markdown, managed with uv. It pulls content
from `SideQuest-Guild/website`, `bot`, and `addon` at build time instead of copying it; see
`README.md` for how. `README.md` explains the repo to people; keep it current and in plain words.

## Layout

- `repos.json` — the source repos this site pulls from. One config, read by both
  `scripts/fetch_sources.py` and the CI workflow.
- `scripts/` — `fetch_sources.py` clones/updates the repos in `repos.json` into `.sources/`;
  `generate_developer_pages.py` turns their READMEs into developer pages; `generate_api_reference.py`
  fetches the live OpenAPI schema and writes a page per tag.
- `source/` — the Sphinx source. `conf.py`, `index.md` (Home), `members.md`, `officers.md`,
  `developers/`, `api/`. Anything under a `_generated/` folder is written by a script and
  gitignored; don't edit it by hand.

## Working

- `make install`, then `make docs` (clones/updates sources, generates pages, builds with `-W` so
  warnings fail the build). `make serve` for live reload while writing.
- Commits are SSH-signed via 1Password. If signing fails, stop and report it; never disable
  signing.
- Conventional-commit subjects, written as plain-English sentences.
- This repo's `AGENTS.md` is covered by the global gitignore (it ignores `AGENTS.md`
  everywhere), so add it with `git add -f AGENTS.md`.

## Writing guides

- Plain words, short sentences, active voice, no jargon a common word would do instead, and no
  em dashes. Follow Orwell's six rules.
- Don't repeat facts, numbers, or rules that live on the main site or in a repo's README; link to
  them instead. They drift; a link doesn't.
- SQL is the loot system's name, SideQuest Loot, pronounced "squeel". Link the word "squeel" to
  <https://www.youtube.com/shorts/z5p-aMyfT98> the one time it appears, and don't repeat the link.
- Renown is the site's participation points; the EP/GP/PR system from the addon is SQL. Don't
  confuse the two.

## Rules that bite

- The developer pages for website/bot/addon are generated from those repos' own READMEs. Don't
  hand-edit `source/developers/_generated/*.md`; it's overwritten on every build. Fix the source
  repo's README instead, or fix the rewriting rules in `generate_developer_pages.py`.
- The API reference is generated from `https://sidequest-guild.com/schema/openapi.json` at build
  time. If that fetch fails, the build must fail too (`generate_api_reference.py` exits non-zero)
  rather than shipping a stale or empty reference.
- Adding a future repo (the Rust sync app) is one entry in `repos.json` plus one stub page under
  `source/developers/`; don't add a placeholder page for it before the repo exists.
