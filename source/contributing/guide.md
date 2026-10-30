# Contributing guide

Thanks for taking a quest. This guide covers every SideQuest repo. A repo's own README has the
details for that repo.

## Pick a way to help

- **Report a bug.** See [Report and find issues](issues.md).
- **Suggest a feature.** Open an issue first, so we can agree on the approach before you write
  code.
- **Fix something.** Look for a
  [good first issue](https://github.com/search?q=org%3ASideQuest-Guild+label%3A%22good+first+issue%22+is%3Aopen&type=issues),
  or pick up a bug you reported yourself.

## Pick a repo

| Repo | What it is | Language |
|---|---|---|
| [website](https://github.com/SideQuest-Guild/website) | sidequest-guild.com, its API and the database | Python (Litestar), Astro |
| [bot](https://github.com/SideQuest-Guild/bot) | The Discord bot. It reaches the database only through the API | Python (discord.py) |
| [addon](https://github.com/SideQuest-Guild/addon) | The in-game addon and the `sidequest-sync` uploader | Lua, Python |
| [companion](https://github.com/SideQuest-Guild/companion) | The desktop tray app that syncs the addon with the site | Rust (GPUI) |

## Before you start

- For anything bigger than a typo, open an issue first.
- Read the [guild rules](https://sidequest-guild.com/rules/). They apply here too.
- Found a security problem? Don't open an issue. Follow the repo's `SECURITY.md`.

## Set up and run the checks

1. Fork the repo and clone your fork.
2. Follow the repo's README to install its tools.
3. Run `make install` to set up dependencies.
4. Run `make ci` to run every check CI runs: formatting, lint, type checks, and tests.

:::{note}
Each repo has its own `Makefile`. `make help` lists every command it offers.
:::

## Make your change

1. Make a branch for your change.
2. Keep the change small and about one thing.
3. Add or update a test for what you change. A test should fail before your change and pass
   after it.
4. Run `make ci` again and fix what it reports.

## Commit your change

Write each commit subject as a [Conventional Commit](https://www.conventionalcommits.org): a
type, a colon, then a plain sentence.

- `feat: add away dates to the account page`
- `fix: the raid chart keeps its groups after a reload`
- `docs: explain how attendance voice minutes work`

Common types are `feat`, `fix`, `docs`, `test`, `ci`, `chore` and `perf`.

## Open a pull request

1. Push your branch and open a pull request.
2. Title it the same way as a commit: `type: what changed`.
3. Say what you changed, why, and how you checked it. Add a screenshot for anything on the site.
4. Update the docs if your change alters what a member or officer sees.

## Review

An officer reviews every pull request. They may ask for changes before merging. Once it merges,
your change ships the next time that repo deploys.

Everyone who takes part agrees to the
[code of conduct](code-of-conduct.md).
