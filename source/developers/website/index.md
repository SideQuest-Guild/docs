# Website & API

The website is the Astro site at [sidequest-guild.com](https://sidequest-guild.com) and the
Litestar API behind it. Everything else in the guild (the bot, the addon, the companion app)
talks to this API over HTTP. Nothing else opens the database.

Astro is a tool that builds plain HTML, CSS and JavaScript from component files. Litestar is a
Python web framework; it's what the API is written with.

## Main parts

| Folder | What's in it |
|---|---|
| `api/` | The API. Each feature has its own folder under `api/src/sidequest_api/domain/`, holding a controller (routes), a service (the logic) and, where needed, dependencies (shared setup). |
| `website/` | The site, built with Astro. Pages are in `src/pages/`, page scripts in `src/scripts/`, images in `assets/`. |
| `packages/sidequest-common/` | The database models, the shape of every API request and reply, and the SQL loot math. The bot depends on this package too; see [How it works](how-it-works.md#the-sidequest-common-pin). |
| `tests/` | Python tests. |
| `website/e2e/` | Browser tests (Playwright). |

```{mermaid}
flowchart LR
    Browser -->|"/ (static site)"| API["api/<br/>Litestar backend"]
    Website["website/<br/>Astro → dist/"] -.->|built output| API
    API --> DB[(PostgreSQL)]
    Common["packages/sidequest-common<br/>models · schemas · loot math"] -.-> API
```

The API serves the built site's files directly, so the site and the API share one origin and one
port in every environment, including your computer.

## Pages

- {doc}`run-locally`: set it up and start it
- {doc}`test`: what `make ci` runs, and how to read the results
- {doc}`how-it-works`: domain layout, migrations, auth, caching, and the website's own Discord calls
- {doc}`deploy`: what happens after you push
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
