# Run it locally

## Prerequisites

| Tool | Why |
|---|---|
| [uv](https://docs.astral.sh/uv/) | Installs the right Python and manages the API's dependencies. |
| [mise](https://mise.jdx.dev) | Installs the right Node version for the site, pinned in `website/mise.toml`. |
| Docker | Runs a local Postgres database. |

## Steps

1. Copy the example environment file and set an API key:

   ```sh
   cp .env.example .env
   ```

   Open `.env` and set `API_KEY` to any long random string. This is the shared key the bot would
   use to call your local API.

2. Install the Python and Node dependencies:

   ```sh
   make install
   ```

3. Start Postgres in Docker and create the database tables:

   ```sh
   make db-up migrate
   ```

4. Start the site and the API together, with hot reload:

   ```sh
   make dev
   ```

   Open <http://localhost:8000>. The site and the API share this one port, so the sign-in cookie
   works on both.

`make help` lists every command.

## Sign-in needs a Discord app

The sign-in button needs a Discord OAuth app and its own client ID and secret
(`WEB_DISCORD_CLIENT_ID`, `WEB_DISCORD_CLIENT_SECRET`). Without one, the public pages still work
and the sign-in button returns an error. See the repo's `.env.example` for how to set one up, and
`WEB_SESSION_SECRET` for the session cookie.

## Running the bot against your local API

Clone the [bot repo](https://github.com/SideQuest-Guild/bot) and set its `API_URL` to
`http://localhost:8000` and its `API_KEY` to the same value you set here. See
{doc}`../bot/run-locally`.

## Database changes

After you change a database model, write and apply a migration:

```sh
make migration MSG="add away dates"
make migrate
```

See {doc}`how-it-works` for the rule that keeps migrations safe during a deploy.
