# Test and check

```sh
luajit tests/run_tests.lua           # addon tests
luacheck SideQuest tests             # lint
uv run --directory uploader pytest   # uploader tests
```

The Lua tests run outside the game, against `tests/wowstub.lua`, a stub of the WoW functions the
addon calls. They don't need the game installed.

The tests also write `tests/fixtures/export_v1.txt` and `export_v2.txt`: sample raid records that
the website's own tests import. If these change, copy them into the website repo too.

## Layout preview

`tests/preview/` draws every tab and popup as a static image, without opening the game, so you
can check a layout change without logging in. It loads the real addon code under the same stub
the unit tests use, feeds it made-up demo data, and renders the result. From the addon repo root:

```sh
uv run --with pillow tests/preview/fetch_atlases.py   # once per checkout, or when new atlas names are added
luajit tests/preview/record.lua
mise exec -C <path-to-website>/website -- node tests/preview/screenshot.mjs
```

`fetch_atlases.py` downloads WoW's own window-chrome art so the preview looks like Forever's real
window frame, not a placeholder. `screenshot.mjs` borrows Playwright from the website repo's
`node_modules`, since this repo has no JavaScript toolchain of its own; point `mise exec -C` at
the inner `website/website` package, not the outer `website/` checkout.

Output goes to `tests/preview/html/` (static pages you can open in a browser), `tests/preview/out/`
(PNG screenshots), and `tests/preview/index.html` (a gallery linking all of them). See
`tests/preview/README.md` for what this tool can and can't prove about the real game's rendering.
