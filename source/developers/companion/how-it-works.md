# How it works

## What it syncs

The companion watches the addon's save file (`SideQuest.lua`) for a new `SQX1:` export, written
whenever WoW logs out or the player types `/reload`. Within a few seconds of a new export
appearing, it uploads it to the website and shows the result (new sessions, boss kills, loot,
point awards) in its History tab.

After a successful upload, it asks the website for the matching `SQI1:` import and writes it back
into `SideQuest.lua` as a staged entry, but only while WoW is closed. The addon applies that entry
automatically the next time an officer logs in, then clears it, so nobody has to copy and paste an
import string by hand. The exact write format (marker lines, the Lua table shape, writing to a
temporary file then renaming it so the game never reads a half-written file, keeping a
`.companion-bak` backup, never writing while WoW is running) is a contract with the addon; a
change to it needs a matching change on the addon side too.

It also checks the addon's GitHub releases against the version installed in the player's
`AddOns` folder every hour, and every 15 minutes while WoW is running, and installs a new one on
its own by default (the same signed zip CurseForge serves). WoW doesn't have to be closed: it
swaps the files in place, and the addon shows an in-game popup telling the player to `/reload`.
`Settings → Install updates automatically` turns that off in favor of a one-click install, and a
chevron next to an installed version offers a rollback to any released version, which pins that
flavor until the player picks the latest again. It checks its own releases the same way, hourly,
to update itself.

## Tray and update check

The app lives mostly in the system tray (`src/ui/tray.rs`); the window opens on click. A
background timer in the engine checks GitHub for new addon and companion releases, and if the
player is signed up for an upcoming raid, shows an OS notification before it starts (pulled from
their private calendar feed or the site's public events).

## Settings and logs

`src/paths.rs` takes these from the `directories` crate. `settings.json` is in the settings
folder; `state.json`, `history.json` and the daily logs are in the data folder.

::::{tab-set}
:sync-group: os

:::{tab-item} {iconify}`mdi:microsoft-windows` Windows
:sync: windows

- Settings: `%APPDATA%\SideQuest Guild\SideQuest Companion\config\`
- Data: `%APPDATA%\SideQuest Guild\SideQuest Companion\data\`
- Logs: `%APPDATA%\SideQuest Guild\SideQuest Companion\data\logs\`
:::

:::{tab-item} {iconify}`mdi:apple` macOS
:sync: macos

- Settings and data: `~/Library/Application Support/com.SideQuest-Guild.SideQuest-Companion/`
- Logs: `~/Library/Application Support/com.SideQuest-Guild.SideQuest-Companion/logs/`
:::

:::{tab-item} {iconify}`mdi:linux` Linux
:sync: linux

- Settings: `~/.config/sidequestcompanion/`
- Data: `~/.local/share/sidequestcompanion/`
- Logs: `~/.local/share/sidequestcompanion/logs/`
:::
::::

The sync token and calendar URL never appear in these logs, even in a debug build. The token is
kept in the OS keyring (service `com.sidequest-guild.companion`); if the keyring isn't available,
it falls back to a `secrets.json` file locked to the current user only (mode `0600`), still never
logged.

## Tolerating an older website

The companion and the website deploy independently. The companion treats a `401` or `404` from a
route the live site hasn't shipped yet (for example, a new game-import endpoint) as expected, not
a fatal error, rather than assuming the site has already deployed.
