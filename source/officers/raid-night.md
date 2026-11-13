# Run a raid night

The addon's Console walks you through a raid night step by step. Boss kills and points are
recorded as the raid goes.

## Before the raid

1. Open the addon's **Console** tab in game. The addon treats you as an officer if your guild
   rank can edit officer notes.
2. Go to **Raid Night**.
3. Zone into the raid and select **Start recording**. The **Who can record** list shows every
   officer SideQuest has heard from recently and whether they're already recording, so two
   officers don't record the same night by accident; clicking **Start recording** again when
   someone else is already recording asks you to confirm first.
4. Select **Prep** to ask the raid to report food, flasks and repairs.

## Run the raid

1. Select **Invite** to invite everyone who signed up on the website.
2. Select **Start raid** to give everyone present 5 EP for being on time. It only unlocks once
   you've selected **Start recording** above.
3. Let boss kills and wipes record on their own: a kill gives 10 EP, and the first wipe of the
   night on a boss the guild hasn't killed gives 10 EP, once per boss per night.
4. When loot drops, select **Loot** to open bidding. Raiders get a popup with the item, its GP
   price, their PR and Main, Off and Pass buttons. Chase items, legendary or special items and
   crafted tier are left for the loot council to decide. Record the council's pick in the
   **Council award** form on the Console's **Loot** tab: the item, the winner, the kind (Chase,
   Legendary or Tier, with the slot for tier) and a one-line reason. **Award by council** stays
   off until all of them are set. The reason is posted in #loot-log after the night syncs.
5. Select **End raid** to give 5 EP to everyone still there. It unlocks once you're recording,
   but doesn't stop recording by itself. Select **Stop recording** (or type `/sq record`)
   when the night is over.

:::{note}
Every award prints a chat line with an undo command, and the Raid Night tab has an **Undo**
button next to each one.
:::

See [Understand your points](../members/points.md) for what EP, GP and PR mean, and the addon's
[developer page](../developers/addon/index.md) for the full tab list and bidding order.

## Send the night to the website

After the raid, the record has to reach the site. Pick whichever is easiest:

1. **SideQuest Companion** (recommended): once an officer is signed in, it uploads a new export
   within seconds of the addon writing it, and keeps the site's reply ready for the addon, so
   your next `/reload` picks it up.
2. Type `/sq export`, copy the text, and paste it on the
   [sync page](https://sidequest-guild.com/officers/sync/).
3. Upload the addon's save file on the same page.
4. Run `sidequest-sync` to upload it for you automatically.

## Import points back

1. On the [sync page](https://sidequest-guild.com/officers/sync/), confirm the import.
2. Copy the **game import string** it gives you.
3. Type `/sq import` in game and paste it.
4. Type `/sq export clear` so the next night starts empty.

SideQuest Companion does this automatically for a signed-in officer: it keeps the site's newest
import in its own small `SideQuest_Inbox` addon, so your next `/reload` or login picks it up
with nothing to copy or paste, even mid-session. The first time, restart WoW once so the game
notices `SideQuest_Inbox`. Once one officer imports, every member online gets the new points.

## Put events on the in-game calendar

After an import, the addon's Console **Sync** tab says how many of the site's upcoming events
aren't on the guild calendar yet.

1. Click **Update calendar**, or type `/sq calendar`.
2. Repeat until it says the calendar matches. The game allows one new calendar event per click.

Events go on as guild events at realm time (WoW: Forever has no guild announcements), with a link
to the sign-up page. Signing up on the calendar itself doesn't reach the site. If the site moves an
event, it takes two clicks: the first opens the event and the second saves the new time. The game
doesn't let addons delete guild events, so when the site cancels one, the addon names it in chat
and you delete it by hand (right-click it on the calendar, then **Delete**). Your guild rank needs
the right to add guild events.

See the [addon's developer page](../developers/addon/index.md) for the full raid night walkthrough and
loot bidding rules, and [use the companion app](../members/companion.md) to set it up.
