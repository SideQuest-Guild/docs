# Developers

SideQuest is five repos. Each app deploys on its own, and each one talks to the others only over
the network, never by sharing a database or a filesystem.

- [**website**](https://github.com/SideQuest-Guild/website): the Astro site and the Litestar
  API. Everything else talks to this API; nothing else opens its database.
- [**bot**](https://github.com/SideQuest-Guild/bot): a discord.py bot, Game Master. Calls the
  website's API with a shared key.
- [**addon**](https://github.com/SideQuest-Guild/addon): an in-game WoW addon, plus
  `sidequest-sync`, a small uploader that watches for the addon's save file and sends it to the
  site.
- [**companion**](https://github.com/SideQuest-Guild/companion): a native tray app for Windows,
  macOS and Linux. Syncs the addon's save file with the site and keeps the addon up to date.
- [**wow-forever-sdk**](https://github.com/SideQuest-Guild/wow-forever-sdk): a Python package for the
  World of Warcraft: Forever Battle.net API. It is a library, not an app. The website's API depends
  on it (`wow` on PyPI) for auction house prices.

```{mermaid}
flowchart LR
    Browser -->|"/ (static site)"| API
    Discord <-->|gateway + REST| Bot["bot<br/>discord.py plugins"]
    Bot -->|"/api/guilds/... + X-API-Key"| API["website: api/<br/>Litestar backend"]
    Addon["addon<br/>in game"] -->|"raid nights via /officers/sync/"| API
    Companion["companion<br/>tray app"] -->|"/api/epgp/* + sync token"| API
    Companion <-->|"reads/writes SavedVariables"| Addon
    Website["website: website/<br/>Astro → dist/"] -.->|built output| API
    API --> DB[(PostgreSQL)]
    Common["website: packages/sidequest-common<br/>models · schemas · leveling math"] -.-> Bot & API
```

## Which repo to change

| You want to... | Change this repo |
|---|---|
| Add or change a page, or anything members or officers see on the site | website (`website/`) |
| Add or change an API route, a database model, or the points/attendance rules | website (`api/`, `packages/sidequest-common/`) |
| Add or change a slash command, a Discord role rule, or anything the bot posts | bot |
| Change a tab, raid recording, or loot bidding in the in-game window | addon (`SideQuest/`) |
| Change the save-file uploader's behaviour | addon (`uploader/`) or companion |
| Change the tray app, auto-sync, or addon/self updates | companion |
| Add or change a Battle.net route, a game data model, or the Battle.net client | wow-forever-sdk |

Each repo's own developer pages go deeper: {doc}`website/index`, {doc}`bot/index`,
{doc}`addon/index`, {doc}`companion/index`, {doc}`wow-forever-sdk/index`.

## Shared rules across repos

### The sidequest-common pin

The bot doesn't copy the website's database models or API shapes. Its `pyproject.toml` pins
`sidequest-common` (and, for tests, `sidequest-api`) to one commit of the website repo. A schema
or settings change on the website can break the bot without warning until someone moves that pin
to a newer commit, runs `uv lock`, then `make ci`. See
{doc}`bot/how-it-works` for the exact steps.

### Rolling deploys mean old and new code run together

Every deploy runs the previous version and the new one side by side for about a minute, and a
database migration runs before the new API version starts. That means a new database column
needs a default or has to stay optional, so the version still running can keep writing rows
without it. The same caution applies across repos: a bot or companion update that calls a new
website route has to tolerate a `404` until the website has deployed too, since the two repos
deploy independently.

### The SQX1/SQI1 contract

The addon and the site exchange raid records as two plain-text formats: `SQX1:` is a raid
night's export, going from the addon to the site; `SQI1:` is a points-and-events import, going
back from the site to the addon. The companion app and `sidequest-sync` move these strings
automatically; an officer can also paste them by hand on `/officers/sync/`. Both formats are
defined once, on the website side, in
`packages/sidequest-common/src/sidequest_common/schemas/epgp.py` and `guild_hub.py`. A change to
either format needs matching changes in the addon's `Sync.lua` and, if it touches the
`SideQuest_Inbox/Inbox.lua` file the companion writes for the addon, the companion's `src/sync.rs`.

## How a change ships

1. Push to a branch and open a pull request. CI runs the repo's full check suite (formatting,
   lint, type or compiler checks, and tests); see each repo's own **Test and check** page for
   what that covers.
2. Once CI passes on `main`, [Cabotage](https://github.com/cabotage/cabotage-app) builds and
   deploys the website and the bot. A push only deploys if its newest commit changes an app file;
   a commit that touches only `.github/` or docs deploys nothing.
3. The addon and the companion app don't deploy on every push. They ship on a signed `v*` tag,
   which starts a release workflow that builds, signs, and publishes the build; see their own
   **Deploy** pages. The SDK ships to PyPI from a GitHub release; see its
   {doc}`wow-forever-sdk/deploy` page.
4. After a website deploy, the `Deployed` workflow clears Cloudflare's cache and runs the browser
   tests against the live site, so a broken deploy is caught within minutes.

## Read more

- {doc}`/reference/index`: every route the website's API serves, and the addon's and companion's
  own data formats.
- {doc}`/changelog/index`: what shipped in each release of every repo.

```{toctree}
:maxdepth: 1
:hidden:

website/index
bot/index
addon/index
companion/index
WoW SDK <wow-forever-sdk/index>
```
