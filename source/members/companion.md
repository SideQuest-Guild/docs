# Use the companion app

**SideQuest Companion** is a small app for Windows, macOS and Linux. It lives in your system
tray (the menu bar on a Mac) and keeps the addon up to date, reminds you before guild events, and, for
officers, carries raid nights to the site.

## Install it

Download it from [sidequest-guild.com/companion](https://sidequest-guild.com/companion/), then
follow the steps for your computer. The app isn't signed with a paid certificate, so the first
launch shows a warning; you only get past it once.

::::{tab-set}
:sync-group: os

:::{tab-item} {iconify}`mdi:microsoft-windows` Windows
:sync: windows

1. Download the **Windows** file (**ARM** if your PC has an Arm chip, such as a Snapdragon).
2. Open the setup file you downloaded. When Windows warns you, select **More info**, then
   **Run anyway**.
3. Select **Next**, then **Finish**. Setup closes and replaces the app if an older version is
   running, and adds **SideQuest Companion** to the Start menu. To remove it later, go to
   **Settings → Apps**.
:::

:::{tab-item} {iconify}`mdi:apple` macOS
:sync: macos

1. Download the **macOS** file. It works on Apple silicon and Intel Macs.
2. Unzip it and move **SideQuest Companion** to your Applications folder.
3. Right-click the app, choose **Open**, then **Open** again. On newer macOS versions, open
   **System Settings**, go to **Privacy & Security** and select **Open Anyway**.
:::

:::{tab-item} {iconify}`mdi:linux` Linux
:sync: linux

1. Download the **Linux** file.
2. Untar it anywhere and run `sidequest-companion`.
3. To add it to your app launcher, copy `sidequest-companion.desktop` to
   `~/.local/share/applications/` and fix its `Exec=` and `Icon=` paths to where you put the
   app.
:::
::::

## Sign in

The app shows nothing until you sign in, so people outside the guild see nothing.

1. Select **Sign in with sidequest-guild.com**. Your browser opens with a short code.
2. Check the code in the browser matches the one in the app.
3. Select **Authorize**. You need to be signed in to the site with Discord first.

The app is now signed in. It finds your WoW folder on its own, wherever Battle.net installed it.
If it can't, open **Settings → WoW Folders**, choose **Add folder** and pick your
`World of Warcraft` folder.

## What you get

| Feature | What it does |
|---|---|
| Addon updates | Checks for a new SideQuest addon every hour, and every 15 minutes while WoW is running, and installs it on its own. WoW doesn't have to be closed: the game shows a popup telling you to `/reload` once the new version is in place. Turn off **Install updates automatically** in **Settings** to install updates in a click instead. **Check for updates** on the **Overview** or **Addon** tab checks right away. The chevron beside an installed version lets you pick an older release instead of the latest, for example to roll back one with a bug; installing anything but the latest pins it there until you choose **Back to latest**. |
| Auto sync | Every time WoW writes its save file (when you `/reload`, log out or close the game), the companion uploads your part right away: your sign-ups and your characters' directory entry (professions, market listings). Your sign-ups reach the site even when no officer is online. Only characters you've [linked to your account](account.md) count. Officers' raid nights upload the same way. |
| Sync now | Uploads your save right away and says whether it worked or that there was nothing new to send. |
| Standings | Your EP, GP, PR and rank, and the top 10, straight from the site. |
| Events | What's coming up on the site, with how many are going and your own answer. During a recruitment drive it shows the leaderboard (qualified, potential and invited recruits per inviter) and how your own recruits are doing. The tab also lists your reminders. |
| Guild | The guild roster, with each character's level, class and when the addon last saw them, and the latest guild news. |
| Event reminders | A notification 30 minutes before raids you've signed up for. In **Settings** you can pick every scheduled event instead, and which kinds: raids, dungeons, world bosses, leveling, PvP, socials, transmog and other events. |
| App updates | Checks for a new app version every hour and installs it on its own, then restarts into it. Turn off **Install app updates automatically** in **Settings** to be asked first instead. |

The **Standings**, **Events** and **Guild** tabs refresh every 2 minutes and right after each upload.

Officers also get the site's newest import back in game: see
[run a raid night](../officers/raid-night.md).

## Check your accounts

The **Overview** tab lists each WoW account's save file and what's waiting to sync.
**Couldn't read the save: <reason>** means the companion couldn't make sense of `SideQuest.lua`.
Type `/reload` in game so WoW rewrites the file, then select **Sync now** again. If it keeps
happening, copy the exact reason shown and send it to an officer.

## Sign out

Select **Sign out** in **Settings**. You can also remove the app from the **Companion** section of
your [account page](account.md), for example if you lost the computer it was on.

## Check a download

Every file is built on GitHub from the app's public source, and GitHub keeps a signed record of
it. See [Verifying a download](https://github.com/SideQuest-Guild/companion#verifying-a-download)
to check yours. What changed in each version is in the {doc}`changelog </changelog/companion>`.
