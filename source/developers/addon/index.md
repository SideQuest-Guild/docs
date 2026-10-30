# WoW addon

The SideQuest addon runs inside World of Warcraft: Forever. Members use it to see the roster,
find crafters, sign up for raids and check their loot points. Officers use it to run raid nights,
award loot, and send the night's record to
[sidequest-guild.com](https://sidequest-guild.com).

The `uploader/` folder holds `sidequest-sync`, a small separate Python program that watches for
the addon's save file and uploads it automatically. {doc}`SideQuest Companion </developers/companion/index>`
does the same job with a tray app instead of a command line.

## Main parts

| Folder | What's in it |
|---|---|
| `SideQuest/` | The addon itself: Lua files for each tab and feature (`Roster.lua`, `Loot.lua`, `Recorder.lua`, …), plus `SideQuest.toc`, the file WoW reads to load it. |
| `uploader/` | `sidequest-sync`, the save-file uploader. |
| `tests/` | Lua unit tests, run outside the game against a stub of WoW's own functions, plus the layout preview tool. |

```{mermaid}
flowchart LR
    Addon["addon<br/>in game"] -->|"raid nights via /officers/sync/"| API["website: api/<br/>Litestar backend"]
    Companion["companion<br/>tray app"] <-->|"reads/writes SavedVariables"| Addon
```

## Points

Raid loot goes by points: EP (effort points), GP (gear points) and PR (priority, EP divided by
GP). This is SQL, SideQuest Loot. The exact rules and prices are on the site's
[Ledger page](https://sidequest-guild.com/ledger/); the addon's code computes them the same way
the site displays them.

## Pages

- {doc}`run-locally`: load the addon and run `sidequest-sync`
- {doc}`test`: the Lua tests and the layout preview tool
- {doc}`how-it-works`: tabs, raid recording, loot bidding, export and import
- {doc}`deploy`: tagging a release and what ships where
- {doc}`readme`: the repo's own README

```{toctree}
:maxdepth: 1
:hidden:

run-locally
test
how-it-works
deploy
readme
```
