# How it works

## Tabs

The window has one tab per task: You (your own points and next raid), Guild (the roster),
Crafters (who can make what), Market (who sells, buys and holds what), Events (sign-ups and the
last 30 days' past events), Ledger (everyone's EP, GP and PR), and News.
Officers also get a gold **Console** tab with its own sub-tabs for running a raid night. See the
[addon's own README](https://github.com/SideQuest-Guild/addon#for-members) for what each tab
shows.

## Raid recording

An officer starts recording from the Console's Raid Night tab. `Recorder.lua` then tracks who's
present, boss kills, and wipes, and awards EP for each: 5 for being there at the start, 5 for
staying to the end, 10 per boss kill, and 10 for the first wipe of the night on a boss the guild
hasn't killed yet. Standby raiders (added with `/sq standby`, approved by an officer) earn the
same. Every award can be undone from the Raid Night tab or with `/sq undo <id>`.

## Loot bidding

`Loot.lua` opens bidding when the master looter's loot window appears. Raiders get a popup with
the item, its GP price, their own PR, and Main, Off and Pass buttons. Bids are ranked by the same
rule the site uses: main spec by PR, then off spec, then alts, then disenchant. Chase items,
legendaries and crafted tier pieces are left out of automatic bidding for the loot council to
decide by hand.

## Guild directory

Every member's addon keeps a record of its own character in five sections (professions, character
basics, craft cooldowns, market, materials) and shares it on the guild channel. `Directory.lua`
hashes each section, announces the hashes after a change (`DIR_V`), and answers requests for a
newer section (`DIR_Q`, `DIR_R`); any client that holds a section can answer for an offline
owner. A client that logs in asks for everyone's hashes (`DIR_LQ`, `DIR_L`) and catches up ten
characters at a time. Newest wins everywhere, by the owner's timestamp. The Crafters and Market
tabs and the item tooltip read from this store, and officers' exports carry all of it to the
site. The full contract is the addon's
[docs/directory.md](https://github.com/SideQuest-Guild/addon/blob/main/docs/directory.md).

## Guild roster

`Roster.lua`'s sweep (`/sq roster` or the Console's **Roster** tab) reads `GetGuildRosterInfo`
for every member, including hours since last online from `GetGuildRosterLastOnline`, and the
guild's ranks from `GuildControlGetRankName`/`GuildControlGetRankFlags`, marking which ranks
carry officer privileges (the Guild Master's rank always does; every other rank's officer flag
comes from a `pcall`'d read, so a client that can't read it sends "unknown" rather than a guess).
An officer's next export carries the snapshot to the site, which is how the public roster and
officers list stay current without a manual list.

## Export and import

`Sync.lua` builds the `SQX1:` export string: the night's record, ready to send to the website.
An officer sends it with `/sq export` (copy and paste), by uploading the save file, or
automatically through `sidequest-sync` or the companion app. The website replies with an `SQI1:`
import string that brings updated points and events back into the addon with `/sq import`.
`Standings.BroadcastAfterImport` (`Standings.lua`) then sends the new EP/GP standings over the
guild channel as a `STANDINGS` message, with that import's events and past events riding along,
so members never need to import anything themselves; a client that logs in later asks any
officer online for a fresher copy with `STANDINGS_REQ`. Both string formats are defined in the
website repo, in `packages/sidequest-common/src/sidequest_common/schemas/epgp.py` and
`guild_hub.py`.

## Guild calendar

`Calendar.lua` puts the imported events on the in-game calendar as guild announcements (not
sign-up events, so sign-ups stay on the site). `C_Calendar.AddEvent` only runs inside a click, so
the Sync tab's **Update calendar** button and `/sq calendar` make one change per press: removals
first, then additions by start time. Calendar events can't hold a site id, so an announcement
matches a site event by title (cut to 31 bytes) and start in realm time, converted from the
site's UTC using the realm clock's offset. `SideQuestDB.calendarLinks` remembers where each event
was last seen, which is how a moved or cancelled event's old announcement is found and removed,
including one another officer added.

## Updates

The game only reloads addon files at login or `/reload`, so when SideQuest Companion installs a
newer SideQuest while WoW is still running, the old version keeps running until then.
`Updates.lua` works around having no file-read API: Companion leaves a font file named after the
version it just replaced at `Media\Updates\<version>.ttf`, and every 15 seconds the running
addon tries to load a font named after itself at that path. Once that load succeeds, the still-
running old version knows a newer SideQuest is already installed, so it prints a message and
shows a **Reload now** popup.

## What isn't tested on Forever yet

Nobody has run the addon on a live Forever server yet. These parts may not work there, and the
addon tells the officer running it when one of them fails:

- Addon messages sent inside a raid group (used for the bidding popup).
- Master looter, which arrives with the raids on December 9, 2026.
- The guild bank log and recipe lists, read through WoW's own API.
- The save file itself, which was unreliable during the beta; officers are told to export more
  than once during a long raid night instead of only at the end.
- Adding and removing guild calendar events (`C_Calendar.AddEvent` and the context-menu remove).

If one of these fails in game, the Console's Loot tab still lets an officer record who got an
item by hand, and points can be read out in voice chat.
