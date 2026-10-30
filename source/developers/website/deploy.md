# Deploy

Push to `main`. Once CI passes, [Cabotage](https://github.com/cabotage/cabotage-app) (the
guild's deploy platform, built on Kubernetes) builds the Docker image, runs the database
migrations, then starts the new version. The whole deploy takes about 13 minutes.

Two things to know:

- **Only app changes deploy.** A push deploys only if its newest commit changes an app file. A
  commit that touches only `.github/` or docs deploys nothing, even if an earlier, undeployed
  commit underneath it changed app code.
- **Old and new code run together.** For about a minute, the previous version keeps serving
  traffic while the new one starts, and the migration runs first. See
  {doc}`how-it-works` for what that means for a migration.

## Settings

Settings are passed as environment variables, grouped by prefix: `API_` for the API itself,
`DB_` for the database, and `WEB_` for the site and sign-in. The repo's `.env.example` lists
every one with what it's for; never put a real value in a doc or a commit.

## After a deploy

The `Deployed` GitHub Actions workflow runs once the new version is live: it clears Cloudflare's
cache (so visitors don't keep seeing the old build's files) and runs the browser tests against
the live site.

```sh
gh run list --workflow deployed.yml
```

Each deploy starts two or three runs that skip themselves; look for the one that actually ran.
