# Developers

SideQuest is three repos, each deployed on its own:

- [**website**](https://github.com/SideQuest-Guild/website) — the Astro site and the Litestar
  API. Everything else talks to this API; nothing else opens its database.
- [**bot**](https://github.com/SideQuest-Guild/bot) — a discord.py bot. Calls the website's API
  with a shared key.
- [**addon**](https://github.com/SideQuest-Guild/addon) — an in-game WoW addon, plus
  `sidequest-sync`, a small uploader that watches for the addon's save file and sends it to the
  site.

```{mermaid}
flowchart LR
    Browser -->|"/ (static site)"| API
    Discord <-->|gateway + REST| Bot["bot<br/>discord.py plugins"]
    Bot -->|"/api/guilds/... + X-API-Key"| API["website: api/<br/>Litestar backend"]
    Addon["addon<br/>in game"] -->|"raid nights via /officers/sync/"| API
    Website["website: website/<br/>Astro → dist/"] -.->|built output| API
    API --> DB[(PostgreSQL)]
    Common["website: packages/sidequest-common<br/>models · schemas · leveling math"] -.-> Bot & API
```

## Running each repo

Each repo's own README has the full steps. The short version:

| Repo | Needs | Command |
|---|---|---|
| website | [uv](https://docs.astral.sh/uv/), [mise](https://mise.jdx.dev), Docker | `make install && make db-up migrate && make dev` |
| bot | [uv](https://docs.astral.sh/uv/), a Discord bot token, the website running locally | `make install && make bot` |
| addon | the game, for the addon itself; [uv](https://docs.astral.sh/uv/) for `sidequest-sync` | load the addon in game; `uvx --from "git+https://github.com/SideQuest-Guild/addon#subdirectory=uploader" sidequest-sync watch` |

Read the [website](website.md), [bot](bot.md), and [addon](addon.md) pages below for the full
setup, what each piece does, and how to deploy it.

## The sidequest-common pin

The bot doesn't copy the website's database models or API shapes. Instead, its `pyproject.toml`
pins `sidequest-common` (and, for tests, `sidequest-api`) to one commit of the website repo. A
schema or settings change on the website can break the bot without warning until that pin moves.
See "When the website changes" on the [bot page](bot.md) for how to bump it.

```{toctree}
:maxdepth: 1
:hidden:

website
bot
addon
```
