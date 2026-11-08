# How it works

## One code base, two clients

The async client in `src/wow/_async/` is the only client that a person writes. `scripts/unasync.py` makes the sync
client from it. The script removes each `async` and `await`, and changes the names, such as `AsyncClient` to
`Client`. CI fails if the two clients do not agree, so edit the async code, then run `make generate`.

Code that does no I/O is in `src/wow/_base.py`, and both clients use it. This code has the retry rules, the token
parse and the request parameters.

## Tokens

For game data, the client gets an app token from `oauth.battle.net` with the client id and the secret. It keeps the
token and gets a new one 5 minutes before the token expires. If Battle.net refuses the token, the client gets a new
token one time and sends the request again. A lock makes sure that many requests at the same time cause only one
request for a token.

For profile data, give the client a player's token. The client sends that token and never refreshes it.

The client sends a token only to its own API host. `client.get()` refuses a link to a different host, so a link in a
response cannot send your token to a different server.

## Models

Each response becomes a [msgspec](https://msgspec.dev) model. A model is immutable, and it skips each field that it
does not declare, so a new field from Blizzard never causes an error.

Blizzard does not document Forever, so each model comes from responses that Battle.net sent. A field that only some
documents have is optional in the model. Two checks keep the models complete. See {doc}`test`.

## Namespaces

Battle.net keeps Forever data in its own namespaces: `static-forever-{region}`, `dynamic-forever-{region}` and
`profile-forever-{region}`. Each resource knows its namespace, so you do not set one.

A 404 from a namespace that Battle.net knows has a `battlenet-namespace` header. A 403 for an unknown namespace does
not. The client puts this header on `NotFoundError.namespace`. Thus you can tell a document that Blizzard did not add
yet from a namespace that does not exist.

## Retries

The client retries connection errors, timeouts, and 408, 429 and 5xx responses, and obeys `Retry-After`. It never
retries the exchange of a login code, because Battle.net accepts each code one time only. The
{doc}`usage guide <usage>` gives the limits.
