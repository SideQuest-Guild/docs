# Run it locally

## Prerequisites

- [uv](https://docs.astral.sh/uv/). uv installs Python 3.14 for you.
- An API client from <https://develop.battle.net/access/clients>. You need it only to call the live API. The tests do
  not need it.

## Steps

1. Clone the repo and install it:

   ```sh
   git clone https://github.com/SideQuest-Guild/wow-forever-sdk
   cd wow-forever-sdk
   make install
   ```

2. Run the tests. They use recorded responses, so they need no credentials:

   ```sh
   make test
   ```

3. To call the live API, set the id and the secret of your API client:

   ```sh
   export BATTLENET_CLIENT_ID=...
   export BATTLENET_CLIENT_SECRET=...
   ```

4. Call the API:

   ```sh
   uv run python -c "from wow import Client; print(Client().playable_classes.get(1).name)"
   ```

The [usage guide](https://github.com/SideQuest-Guild/wow-forever-sdk/blob/main/docs/usage.md) shows each part of the
client: regions, search, errors and raw access.
