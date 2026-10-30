# Companion app

SideQuest Companion is a native tray app for Windows, macOS and Linux that syncs the
{doc}`WoW addon </developers/addon/index>`'s save file with
[sidequest-guild.com](https://sidequest-guild.com). It's built with
[GPUI](https://www.gpui.rs/), a Rust UI toolkit: no browser or webview, just a window that draws
itself.

## Main parts

| File | What's in it |
|---|---|
| `src/engine.rs` | The background engine. Owns the watch/sync/update loop and talks to the UI only through `Snapshot` (what the UI reads) and `Command` (what the UI sends). |
| `src/api.rs`, `src/sync.rs`, `src/history.rs` | The website client, upload/stage logic, and sync history. |
| `src/config.rs`, `src/secrets.rs` | Settings, and keyring access for the sync token. |
| `src/wow/` | SavedVariables reading and WoW-install discovery. |
| `src/release.rs`, `src/addon_install.rs`, `src/self_update.rs` | GitHub release checks, installing addon updates, and updating the companion itself. |
| `src/reminders.rs`, `src/notifications.rs`, `src/autostart.rs` | Raid reminders, OS notifications, and launch-at-login. |
| `src/main.rs`, `src/ui/` | The GPUI app, window and tray icon. |

```{mermaid}
flowchart LR
    Companion["companion<br/>tray app"] -->|"/api/epgp/* + sync token"| API["website: api/<br/>Litestar backend"]
    Companion <-->|"reads/writes SavedVariables"| Addon["addon<br/>in game"]
```

## The engine-UI contract

The UI never touches the filesystem, network, or keyring directly. It only calls
`EngineHandle::snapshot()`, sends a `Command`, or calls `shutdown_blocking()`, and redraws when a
`Repaint` event fires. See {doc}`how-it-works` for what it syncs.

## Pages

- {doc}`run-locally`: build and run it
- {doc}`test`: `cargo test` and the other checks in `make ci`
- {doc}`how-it-works`: what it syncs, the tray, update checks, and where settings live
- {doc}`deploy`: tagging a release and what it builds
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
