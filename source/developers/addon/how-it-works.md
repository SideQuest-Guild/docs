# How it works

## Tabs

The window has one tab per task: You (your own points and next raid), Guild (the roster),
Crafters (who can make what), Raids (sign-ups), Ledger (everyone's EP, GP and PR), and News.
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

## Export and import

`Sync.lua` builds the `SQX1:` export string: the night's record, ready to send to the website.
An officer sends it with `/sq export` (copy and paste), by uploading the save file, or
automatically through `sidequest-sync` or the companion app. The website replies with an `SQI1:`
import string that brings updated points and events back into the addon with `/sq import`. Once
one officer imports, every member online shares the new points at once. Both string formats are
defined in the website repo, in `packages/sidequest-common/src/sidequest_common/schemas/epgp.py`
and `guild_hub.py`.

## What isn't tested on Forever yet

Nobody has run the addon on a live Forever server yet. These parts may not work there, and the
addon tells the officer running it when one of them fails:

- Addon messages sent inside a raid group (used for the bidding popup).
- Master looter, which arrives with the raids on December 9, 2026.
- The guild bank log and recipe lists, read through WoW's own API.
- The save file itself, which was unreliable during the beta; officers are told to export more
  than once during a long raid night instead of only at the end.

If one of these fails in game, the Console's Loot tab still lets an officer record who got an
item by hand, and points can be read out in voice chat.
