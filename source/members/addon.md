# Use the addon

The in-game addon, **SideQuest**, shows the roster, who can craft what, upcoming events and your
loot points. You can also sign up for events and ask for standby from inside the game.

## Install it

1. Install **SideQuest Guild** from [CurseForge](https://www.curseforge.com/projects/1773662)
   with the CurseForge app, or download the zip from
   [GitHub releases](https://github.com/SideQuest-Guild/addon/releases) and unzip it into
   `_forever_/Interface/AddOns/`.
2. Check you have `Interface/AddOns/SideQuest/SideQuest.toc`.
3. In game, click the crest on the minimap or type `/sq` to open the window. Drag the crest
   round the minimap to move it, or type `/sq minimap` to hide it.

The [companion app](companion.md) can also install the addon for you and keep it up to date.

:::{note}
CurseForge and GitHub serve the same signed zip. See the addon's
[SECURITY.md](https://github.com/SideQuest-Guild/addon/blob/main/SECURITY.md) to check a
download came from the real repo.
:::

## The tabs you'll use

| Tab | What it shows |
|---|---|
| You | Your PR and where it ranks, your last four weeks of points, your next event with Going, Maybe and Can't buttons, and who's online. |
| Guild | The roster, with alts under their main. Search it, filter by class, rank or online, and whisper or invite from it. |
| Crafters | Search a recipe or profession to see who can make it, online people first. Pick a profession to see every member who has it and their skill, or check who has Transmute, Mooncloth and other craft cooldowns ready. |
| Market | What guildmates sell and want to buy, open requests for materials, and who holds an item. **Mine** lists and edits your own. |
| Events | Upcoming events, how many have signed up for each role, and your own answer. |
| Ledger | Everyone's EP, GP and PR, then your own points history and loot. |
| News | Guild announcements and recent activity. |

Click someone on the Guild tab to see their level, spec, item level, professions, Onyxia
attunement, tracked reputations and cooldowns. Hover any item to see which guildmates craft,
sell, buy or hold it.

Your sign-ups from the addon reach the website the next time an officer syncs a raid night. You
don't need to do anything else.

## What the addon shares

The addon keeps a record of your character and shares it with the guild by itself. Guildmates see
it in game even while you're offline, and officers' syncs bring it to the
[Guild page](https://sidequest-guild.com/guild/), where only signed-in members see it.

| Part | What it shares |
|---|---|
| Professions | Each profession and its skill, and the recipes you know. |
| Character | Level, class, race, spec, item level, Onyxia attunement and the few reputations the guild tracks. |
| Cooldowns | When your Transmute, Mooncloth and other craft cooldowns are ready. |
| Market | What you sell and want to buy, and your requests for materials. |
| Materials | Trade goods and reagents in your bags and bank. Never gold or gear. |

Skill levels update by themselves. Open each profession window once so the guild learns your
recipes, and open your bank once so it counts your materials there.

To stop sharing a part, untick it under **Sharing** on the You tab, or type
`/sq share <prof|char|cd|market|stock> off`. What the guild already had for that part is removed
at the next sync.

## Sell, buy and ask for materials

Open **Market**, then **Mine**, and fill in the item, a price and how many. Shift-click an item
from your bags into the item box, or type its name or ID. With Auctionator or TradeSkillMaster
installed, the addon suggests a price.

Or type a command. Prices look like `1g20s`, `35s`, `80c`, or a plain number of gold such as `1.5`.
Leave the price off and buyers whisper you.

| Command | What it does |
|---|---|
| `/sq sell <item> <price> [qty]` | List something you sell. |
| `/sq buy <item> <price>` | Put up a standing offer to buy a material. |
| `/sq request <item> <qty> [price] [note]` | Ask the guild for materials you need. |
| `/sq unrequest <item>` | Take a request down. |

An `<item>` is a shift-clicked link, an item ID, or a name in quotes, such as
`/sq sell "Bolt of Runecloth" 1g20s 20`.

## Ask for standby

If you can come to a raid but the group is already full:

1. Type `/sq standby`.
2. Wait for an officer in the raid to add you.

Standby earns the same points as being in the raid.

:::{dropdown} Which parts aren't tested on Forever yet?
Nobody has run the addon on a live Forever server yet. The addon tells you when one of these
fails:

- Addon messages inside a raid. If the loot popup can't reach you, ask an officer to award loot
  by hand and read points out in voice chat.
- Master loot, which arrives with the raids on December 9.
- The guild bank log.
- Reading professions, recipes, cooldowns, attunements and bag contents. Each of these uses a
  part of the game that changed for Forever; a part that fails just stays empty.

See [Understand your points](points.md) for what EP, GP and PR mean, and the
[raids page](https://sidequest-guild.com/raids/) for how a raid night runs.
:::
