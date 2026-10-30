# Run it locally

The addon itself has no build step. It runs inside the game.

## Load the addon in game

1. Copy or symlink the `SideQuest/` folder into your WoW install's
   `_classic_beta_/Interface/AddOns/` folder, so you end up with
   `Interface/AddOns/SideQuest/SideQuest.toc`.
2. Start the game and type `/sq` to open the window.

For a change you're testing, reload your UI (`/reload`) instead of restarting the game.

## Run sidequest-sync

`sidequest-sync` needs [uv](https://docs.astral.sh/uv/). Get a sync token from the site's
[sync page](https://sidequest-guild.com/officers/sync/) first; the site shows it only once.

```sh
uvx --from "git+https://github.com/SideQuest-Guild/addon#subdirectory=uploader" sidequest-sync login
uvx --from "git+https://github.com/SideQuest-Guild/addon#subdirectory=uploader" sidequest-sync watch
```

`watch` finds the save file and uploads it whenever it changes. Other commands: `once` (upload a
single time) and `status` (show what it last found). Point it at a local API for testing with the
same flags the website uses; see the `uploader/README.md` for the full list.
