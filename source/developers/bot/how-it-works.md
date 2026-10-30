# How it works

## A plugin per feature

Each feature is its own file in `src/sidequest_bot/plugins/`, called a *cog* in discord.py terms:
a class that groups a feature's commands, buttons and event listeners together. For example,
`events.py` handles event threads and sign-up buttons, `leveling.py` handles chat XP, and
`moderation.py` handles warns, timeouts, kicks and bans.

## Talking to the API

`src/sidequest_bot/api_client.py` is the only code in the bot that calls the website's API. It
sends the shared `X-API-Key` header on every request. Bot code catches its `APIError`, not a raw
validation error, so a bad reply from the API fails predictably instead of crashing a plugin.

About once a minute the bot asks the API what changed (new events, sign-ups, who should hold
which role) and reports back what happened in Discord (button clicks, who's in which voice
channel, name and role changes). A change made on either side reaches the other within about a
minute.

## Role safety

`src/sidequest_bot/lib/roles.py` guards every role grant and revoke. The bot only hands out a
role if it sits below the bot's own role in the server's role list, carries no moderator or admin
permissions, and isn't managed by another app (such as a role Discord itself creates for a
booster). It checks this before every single grant, so a role that later gains permissions stops
being handed out automatically. The same rule applies to moderation commands: nobody, including
an officer, can moderate the server owner, the bot, themselves, or a member whose top role is at
or above their own.

## Slash command limits

A command name can be at most 32 characters, and a description must be 1 to 100 characters. A
command outside those limits makes the bot crash on startup in a loop. `test_app_command_limits.py`
checks every command for this before it can be merged; see {doc}`test`.

## Persistent buttons

Buttons on event threads (**Going**, **Maybe**, **Can't**) and role menus still work after the
bot restarts, because discord.py registers them as *persistent views*: a view with a fixed
`custom_id` that the bot re-attaches to on startup, instead of a one-off view tied to the message
that sent it. A new button needs a stable `custom_id` for this to keep working.

## The sidequest-common pin

The bot gets the shape of the API's requests and replies from the website's `sidequest-common`
package. It isn't published anywhere else, so `pyproject.toml` pins it (and, for tests,
`sidequest-api`) to one commit of the website repo:

```toml
[tool.uv.sources]
sidequest-common = { git = "https://github.com/SideQuest-Guild/website", rev = "<sha>", subdirectory = "packages/sidequest-common" }
sidequest-api = { git = "https://github.com/SideQuest-Guild/website", rev = "<sha>", subdirectory = "api" }
```

To move to a newer website commit: put its SHA in both `rev` fields, run `uv lock`, then `make
ci`.

## Rolling deploys

The bot and the website's API deploy independently of each other. A new bot talking to an old
API, or an old bot talking to a new API, has to tolerate the other side returning 404 for a route
it doesn't know about yet. Never assume the other side has already deployed; if the bot needs a
new route, deploy the website first.
