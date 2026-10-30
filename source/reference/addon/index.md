# Addon

The in-game addon for the roster, raid sign-ups, loot points and raid nights, plus the
`sidequest-sync` uploader.

- **[Slash commands](_generated/commands.md)**: every `/sq` subcommand, generated from the
  addon's own source.
- **[SQX1: raid export format](_generated/sqx1.md)**: the string an officer sends from the game
  to the site.
- **[SQI1: game import format](_generated/sqi1.md)**: the string the site sends back to the game.

Both formats are defined once, on the website's side, in `packages/sidequest-common`; these pages
are generated from that source so they can't drift from what the addon and the site actually
exchange.

```{toctree}
:maxdepth: 1
:hidden:

_generated/commands
_generated/sqx1
_generated/sqi1
```
