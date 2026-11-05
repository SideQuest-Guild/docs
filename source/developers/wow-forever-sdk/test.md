# Test and check

```sh
make ci
```

This runs each check that GitHub runs. `make fmt` fixes the format for you.

| Check | Command | What it covers |
|---|---|---|
| Lint and format | `make check` | ruff, pyproject-fmt, codespell, and zizmor for the GitHub workflows |
| Sync client | `make check` | Fails if `src/wow/_sync` does not agree with `src/wow/_async`. Run `make generate` to fix it. |
| Types | `make check` | pyrefly in strict mode. It fails only on errors that are not in `pyrefly-baseline.json`. |
| Tests | `make test` | pytest. It fails if coverage goes below 100%. |
| Docs | `make docs` | Sphinx. A warning stops the build. |
| Build | `make build` | The sdist and the wheel. |

## Each test runs 3 times

Most tests run 3 times: against the sync client, and against the async client under asyncio and under trio. Thus the
two clients cannot do different things.

## Live check of the models

A model skips a field that it does not declare. Thus a new field from Blizzard can go missing without an error. Two
checks find it:

- `tests/test_models.py` decodes each recorded response, encodes it again, and fails on a field that went missing.
- `make audit-models` does the same check on each document that it can get from the live API. It needs the
  credentials from {doc}`run-locally`, and it takes about 4 minutes.

Run `make audit-models` after a game patch. The
[development guide](https://github.com/SideQuest-Guild/wow-forever-sdk/blob/main/docs/development.md) gives the steps
to fix a model.
