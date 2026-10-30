# Run it locally

## Prerequisites

- [uv](https://docs.astral.sh/uv/)
- A bot token from the Discord Developer Portal (the Game Master app, then its Bot page)
- The {doc}`website's API </developers/website/run-locally>` running on your computer

In the Developer Portal, turn on the **Server Members** and **Message Content** intents (these
let the bot read who's in the server and read message text for chat leveling). In your test
server, give the bot **Manage Events**, and for the events forum also **Manage Channels**, **Send
Messages in Threads** and **Create Posts**.

## Steps

1. Set these in a `.env` file or your shell:

   ```sh
   DISCORD_TOKEN=...                   # from the Developer Portal
   API_KEY=...                         # the same value as the website's API_KEY
   API_URL=http://localhost:8000
   WEB_BASE_URL=http://localhost:8000  # used in links the bot posts
   DISCORD_GUILD_ID=...                # optional: your test server, so slash commands show up at once
   ```

2. Install and run:

   ```sh
   make install
   make bot
   ```

Without `DISCORD_GUILD_ID`, new or changed slash commands can take up to an hour to show up
everywhere, since Discord registers global commands slowly; a guild-scoped command shows up at
once.
