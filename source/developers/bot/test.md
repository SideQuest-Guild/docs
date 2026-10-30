# Test and check

```sh
make ci
```

This runs every check GitHub runs: formatting, lint, type checks and the test suite. `make fmt`
fixes formatting for you.

| Check | Command | What it covers |
|---|---|---|
| Formatting | `make fmt-check` | ruff |
| Lint | `make lint` | ruff |
| Types | `make type-check` | pyrefly. Fails only on *new* errors; known ones are listed in `pyrefly-baseline.json`. After fixing some, run `make type-baseline` to shrink it. |
| Tests | `make test` | Starts a real copy of the website's API in-process, inside the test run, so tests catch a change in what the API sends back. |

## Command limits

`test_app_command_limits.py` checks that every slash command's name is 32 characters or fewer and
its description is between 1 and 100. A command over these limits crashes the live bot in a loop,
so this test has to pass before you push.
