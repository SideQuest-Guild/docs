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
2. Unzip it and open `sidequest-companion.exe`.
3. When Windows warns you, select **More info**, then **Run anyway**.
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

The app is now signed in. It finds your WoW folder on its own; if it picks the wrong one, set it
in **Settings**.

## What you get

| Feature | What it does |
|---|---|
| Addon updates | Tells you when a new SideQuest addon is out and installs it in one click. Turn on **Install updates automatically while WoW is closed** in **Settings** to skip the click. |
| Event reminders | A notification 30 minutes before raids you've signed up for. In **Settings** you can pick every scheduled event instead, and which kinds: raids, dungeons, world bosses, leveling, PvP, socials, transmog and other events. The **Events** tab lists what's coming up. |
| Sync now (officers) | Uploads any new raid night right away, and says whether it worked or that there was nothing new to send. |
| App updates | Tells you when a new version of the app is out and installs it in one click. |

Officers also get automatic sync. See [run a raid night](../officers/raid-night.md).

## Sign out

Select **Sign out** in **Settings**. You can also remove the app from the **Companion** section of
your [account page](account.md), for example if you lost the computer it was on.

## Check a download

Every file is built on GitHub from the app's public source, and GitHub keeps a signed record of
it. See [Verifying a download](https://github.com/SideQuest-Guild/companion#verifying-a-download)
to check yours. What changed in each version is in the {doc}`changelog </changelog/companion>`.
