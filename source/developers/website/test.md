# Test and check

```sh
make ci
```

This runs every check GitHub runs on a pull request: formatting, lint, type checks, the Python
tests, the website's own checks, a production build, and the browser tests. `make fmt` fixes
formatting for you.

| Check | Command | What it covers |
|---|---|---|
| Formatting | `make fmt-check` | Python (ruff) and the website (oxfmt). |
| Lint | `make ruff-check`, `make web-lint` | Python and website code style. |
| Types | `make type-check` | Python types (pyrefly). Fails only on *new* errors; known ones are listed in `pyrefly-baseline.json`. |
| Python tests | `make test` | Starts a real API with a fresh database for each test, so no separate Postgres is needed. |
| Website checks | `make web-check` | Astro type checks, the end-to-end tests' own types, and the website's unit tests. |
| Browser tests | `make web-e2e` | See below. |

## Browser tests

```sh
make web-e2e-install   # once, to download the browsers
make web-e2e
```

This opens every page in desktop Chrome, on a simulated iPhone, an Android phone and a 320px
phone. The API is faked from `website/e2e/data.ts`, so these tests check layout and behaviour,
not real data. A test fails if a page scrolls sideways, falls off the screen, doesn't load, or
logs an error.

Read the results with:

```sh
npx playwright show-report
```

run from `website/`. It opens a report with screenshots for anything that failed.

A new page needs an entry in `PAGES` in `website/e2e/layout.spec.ts`. A new API call the page
makes needs a matching handler in `website/e2e/fixtures.ts`; an unhandled call fails the test.

## Type check baseline

Type checks only fail on errors that aren't already known. After you fix some of the known
errors, record the smaller baseline:

```sh
make type-baseline
```

## Database migrations

`make migration MSG="add away dates"` writes a new migration from your model changes; `make
migrate` applies it. See {doc}`how-it-works` for why a migration also has to work with the code
that was running before it.
