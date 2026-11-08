# WoW Forever SDK

The SDK is a Python package for the World of Warcraft: Forever Battle.net API. It gives typed models for game data,
such as classes, items, mounts and quests. It also gets tokens, retries failed requests and reads search results.
You import it as `wow`.

The SDK is a library, not a service. The website's API depends on it, and it is on PyPI as
[`wow`](https://pypi.org/project/wow/).

## Main parts

| Folder | What's in it |
|---|---|
| `src/wow/_async/` | The client and one resource for each Battle.net API, written as async code. Edit this code. |
| `src/wow/_sync/` | The sync client. A script writes it from `_async`. Do not edit it. |
| `src/wow/models/` | The models. See {doc}`how-it-works`. |
| `tests/fixtures/` | Responses recorded from the live API. The tests send them from a mock Battle.net. |
| `scripts/` | The scripts that write the sync client, record the fixtures and check the models against the live API. |

## Pages

- {doc}`usage`: install it and call the API
- {doc}`models`: how to read a model
- {doc}`run-locally`: set it up to develop it
- {doc}`test`: what `make ci` runs, and the live check of the models
- {doc}`how-it-works`: the two clients, tokens, models, and the namespaces
- {doc}`deploy`: how a release gets to PyPI
- {doc}`readme`: the repo's own README

```{toctree}
:maxdepth: 1
:hidden:

usage
models
run-locally
test
how-it-works
deploy
readme
```
