# Run a raid night

The addon's Console walks you through a raid night step by step. Boss kills and points are
recorded as the raid goes.

## Before the raid

1. Open the addon's **Console** tab in game. The addon treats you as an officer if your guild
   rank can edit officer notes.
2. Go to **Raid Night**.
3. Select **Prep** to ask the raid to report food, flasks and repairs.

## Run the raid

1. Select **Invite** to invite everyone who signed up on the website.
2. Select **Start raid** to begin recording. This gives everyone present 5 EP for being on time,
   and tells the raid you're recording so a second officer doesn't record the same night.
3. Let boss kills and wipes record on their own: a kill gives 10 EP, and the first wipe of the
   night on a boss the guild hasn't killed gives 10 EP, once per boss per night.
4. When loot drops, select **Loot** to open bidding. Raiders get a popup with the item, its GP
   price, their PR and Main, Off and Pass buttons. Chase items, legendaries and crafted tier are
   left for the loot council to decide.
5. Select **End raid** to give 5 EP to everyone still there and stop recording.

:::{note}
Every award prints a chat line with an undo command, and the Raid Night tab has an **Undo**
button next to each one.
:::

See [Understand your points](../members/points.md) for what EP, GP and PR mean, and the addon's
[developer page](../developers/addon/index.md) for the full tab list and bidding order.

## Send the night to the website

After the raid, the record has to reach the site. Pick whichever is easiest:

1. **SideQuest Companion** (recommended): once an officer is signed in, it uploads a new export
   within seconds of the addon writing it, and stages the site's reply back into the save file
   for the addon to pick up automatically.
2. Type `/sq export`, copy the text, and paste it on the
   [sync page](https://sidequest-guild.com/officers/sync/).
3. Upload the addon's save file on the same page.
4. Run `sidequest-sync` to upload it for you automatically.

## Import points back

1. On the [sync page](https://sidequest-guild.com/officers/sync/), confirm the import.
2. Copy the **game import string** it gives you.
3. Type `/sq import` in game and paste it.
4. Type `/sq export clear` so the next night starts empty.

SideQuest Companion does this automatically for a signed-in officer: it stages the import so the
next login picks it up with nothing to copy or paste. Once one officer imports, every member
online gets the new points.

See the [addon's developer page](../developers/addon/index.md) for the full raid night walkthrough and
loot bidding rules, and [use the companion app](../members/companion.md) to set it up.
