# Deploy

Push to `main`. [Cabotage](https://github.com/cabotage/cabotage-app) builds the `Dockerfile` and
runs the one process in the `Procfile`: `worker: sidequest-bot`. It serves no web traffic.

## Run exactly one worker

Run only one copy of the bot. Two bots signed in with the same token would both answer every
button press and post everything twice.

## Settings

| Setting | Value on the live site |
|---|---|
| `DISCORD_TOKEN` | The bot's token. Never log or print it. |
| `API_KEY` | The same value as the website's `API_KEY`. |
| `API_URL` | `https://sidequest-guild.com` |
| `WEB_BASE_URL` | `https://sidequest-guild.com` |
| `DISCORD_GUILD_ID` | Optional; set it if you want slash commands to update at once instead of waiting for Discord's global rollout. |
