# Use the addon

The in-game addon, **SideQuest**, shows the roster, who can craft what, upcoming raids and your
loot points. You can also sign up for raids and ask for standby from inside the game.

## Install it

1. Install **SideQuest Guild** from [CurseForge](https://www.curseforge.com/projects/1773662)
   with the CurseForge app, or download the zip from
   [GitHub releases](https://github.com/SideQuest-Guild/addon/releases) and unzip it into
   `_classic_beta_/Interface/AddOns/`.
2. Check you have `Interface/AddOns/SideQuest/SideQuest.toc`.
3. In game, type `/sq` to open the window.

The [companion app](companion.md) can also install the addon for you and keep it up to date.

:::{note}
CurseForge and GitHub serve the same signed zip. See the addon's
[SECURITY.md](https://github.com/SideQuest-Guild/addon/blob/main/SECURITY.md) to check a
download came from the real repo.
:::

## The tabs you'll use

| Tab | What it shows |
|---|---|
| You | Your PR and where it ranks, your last four weeks of points, your next raid with Going, Maybe and Can't buttons, and who's online. |
| Guild | The roster, with alts under their main. Search it, filter by class, rank or online, and whisper or invite from it. |
| Crafters | Type a recipe or a profession to see who can make it, online people first. |
| Raids | Upcoming events, how many have signed up for each role, and your own answer. |
| Ledger | Everyone's EP, GP and PR, then your own points history and loot. |
| News | Guild announcements and recent activity. |

Your sign-ups from the addon reach the website the next time an officer syncs a raid night. You
don't need to do anything else.

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
- The guild bank log and recipe lists.

See [Understand your points](points.md) for what EP, GP and PR mean, and the
[raids page](https://sidequest-guild.com/raids/) for how a raid night runs.
:::
