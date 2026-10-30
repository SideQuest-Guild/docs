# How it works

## Domain layout

Each feature of the API lives in its own folder under `api/src/sidequest_api/domain/`: for
example `events/`, `epgp/`, `attendance/`, `heroes/`, `mcp/`. Inside, a `controllers.py` defines
the routes, a `services.py` holds the logic, and a `dependencies.py` wires up anything the routes
need. With the API running, `/schema` lists every route with what it takes and returns; the
site's own {doc}`/reference/website/index` shows the same thing, styled to match.

`packages/sidequest-common/` holds the database models and the shape of every request and reply
(its *schemas*). This package is shared: the bot depends on it too, so a change here can affect
the bot. See [The sidequest-common pin](#the-sidequest-common-pin).

## Migrations and rolling deploys

A deploy runs the old and new versions of the API side by side for about a minute, and the
database migration runs before the new version starts. That means:

- A new column needs a default, or must stay optional, so the old code (which doesn't know about
  it) keeps working.
- A new migration should build on the current head; check `api/src/sidequest_api/lib/migrations/versions/`
  and `main` before writing one, since someone else may have added one already.

## Auth

The website checks who's asking in three different ways, depending on who's asking:

- **Sessions.** A member who signs in with Discord gets an encrypted session cookie
  (`WEB_SESSION_SECRET`). The site and the API share one origin, so this cookie works on both.
- **The bot's key.** The bot sends a shared secret as the `X-API-Key` header on every call. It's
  the same value as the website's `API_KEY` setting.
- **Sync tokens.** Officers make a sync token on `/officers/sync/` so `sidequest-sync` or the
  companion app can upload raid records without signing in as a person. The site shows a token
  once and keeps only a scrambled copy.
- **MCP tokens.** Officers can make a token that lets an AI tool such as Claude Code act on the
  guild's behalf, scoped to what an officer could do by hand. See the repo's README for how to
  make one and what it can't do.

## Caching

**Cloudflare** caches most pages at the edge for 60 seconds, then serves a stale copy while
refreshing it in the background. A route is only cached this way if it explicitly sends a
`Cloudflare-CDN-Cache-Control` header and skips the session middleware, so a cached response can
never carry a sign-in cookie. Everything under `/api` and `/auth` is never cached.

**The service worker** (`website/service-worker/sw.js`) precaches pages, scripts and fonts for
each build. For a page listed in `STALE_FIRST`, it shows the last copy saved on the visitor's own
device first, then replaces it once fresh data arrives through `onFreshData` (in
`website/src/scripts/api.ts`). A page you add to `STALE_FIRST` needs its own call to
`onFreshData`. Setting `SERVICE_WORKER = false` in `astro.config.mjs` turns it off.

**No full page reloads.** Astro's `ClientRouter` swaps pages in place instead of reloading the
browser, so a page's own script only runs once per visit unless you ask it to run again. Because
of that, every page script starts with `onPage(rootSelector, (signal) => …)` (in
`website/src/scripts/page.ts`) and passes that `signal` to any window or document listener, timer
or observer, so it's cleaned up when the visitor leaves the page.

## The website's own Discord calls

Most of the guild's Discord activity goes through the bot (see {doc}`/developers/bot/how-it-works`).
But the website also talks to Discord directly, over its REST API, for two things: the OAuth2
sign-in flow, and looking up a signed-in member's roles. This is a separate connection from the
bot's gateway connection; the code is in `api/src/sidequest_api/lib/discord.py`.

## The sidequest-common pin

The bot doesn't copy the website's database models or API shapes. Instead, its `pyproject.toml`
pins the `sidequest-common` package (and, for tests, `sidequest-api`) to one commit of this repo.
A change here to a schema or a setting can break the bot without warning, until someone moves
that pin. See {doc}`/developers/bot/how-it-works` for how to bump it, and deploy the website
first if the bot needs a route that doesn't exist yet.
