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
`AddOns` folder and offers to install the latest one (the same signed zip CurseForge serves), and
checks its own releases the same way to update itself.

## Tray and update check

The app lives mostly in the system tray (`src/ui/tray.rs`); the window opens on click. A
background timer in the engine checks GitHub for new addon and companion releases, and if the
player is signed up for an upcoming raid, shows an OS notification before it starts (pulled from
their private calendar feed or the site's public events).

## Settings and logs

| What | macOS | Windows | Linux |
|---|---|---|---|
| Settings | `~/Library/Application Support/com.sidequest-guild.companion/` | `%APPDATA%\SideQuest Guild\Companion\` | `~/.config/sidequest-companion/` |
| Logs | `~/Library/Logs/com.sidequest-guild.companion/` | `%LOCALAPPDATA%\SideQuest Guild\Companion\logs\` | `~/.local/state/sidequest-companion/logs/` |

The sync token and calendar URL never appear in these logs, even in a debug build. The token is
kept in the OS keyring (service `com.sidequest-guild.companion`); if the keyring isn't available,
it falls back to a `secrets.json` file locked to the current user only (mode `0600`), still never
logged.

## Tolerating an older website

The companion and the website deploy independently. The companion treats a `401` or `404` from a
route the live site hasn't shipped yet (for example, a new game-import endpoint) as expected, not
a fatal error, rather than assuming the site has already deployed.
