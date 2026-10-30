# Discord bot

Game Master is the guild's Discord bot, built with [discord.py](https://discordpy.readthedocs.io/).
It posts events and takes sign-ups, hands out roles based on the
[website](https://sidequest-guild.com), awards chat levels and badges, and moderates the server.

The bot never opens the database. It talks to the website's API only over HTTP, with a shared
key (the `X-API-Key` header). Anything it remembers lives on the website.

## Main parts

| Folder | What's in it |
|---|---|
| `src/sidequest_bot/plugins/` | One file per feature: events, roles, levels, moderation, and so on. See {doc}`how-it-works`. |
| `src/sidequest_bot/api_client.py` | The only code that calls the website's API. |
| `src/sidequest_bot/lib/roles.py` | Guards every role grant and revoke; see {doc}`how-it-works`. |
| `src/sidequest_bot/assets/role_icons/` | The badge, level and gate role images. |
| `tests/` | Boots a real copy of the website's API in-process for each test, so tests check real request and reply shapes. |

```{mermaid}
flowchart LR
    Discord <-->|gateway + REST| Bot["bot<br/>discord.py plugins"]
    Bot -->|"/api/guilds/... + X-API-Key"| API["website: api/<br/>Litestar backend"]
```

## Pages

- {doc}`run-locally`: set it up and start it
- {doc}`test`: what `make ci` runs
- {doc}`how-it-works`: plugins, the API client, role safety, and command limits
- {doc}`deploy`: what happens after you push, and the sidequest-common pin
- {doc}`readme`: the repo's own README

```{toctree}
:maxdepth: 1
:hidden:

run-locally
test
how-it-works
deploy
readme
```
