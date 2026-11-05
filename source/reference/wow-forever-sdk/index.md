# WoW Forever SDK

The typed Python client for the World of Warcraft: Forever Battle.net API. Each page is generated from one module of
the `wow` package. Select **[source]** beside a class or a function to read its code.

| Module | What it holds |
| --- | --- |
| {doc}`wow </reference/_generated/python/wow/index>` | `Client` and `AsyncClient`, the errors, `Region`, `Locale`, `OAuthToken` and `APIResponse`. |
| {doc}`wow.models </reference/_generated/python/wow/models/index>` | The shared reference types, and one page for each group of models, such as items or quests. |
| {doc}`wow.resources </reference/_generated/python/wow/resources/index>` | One class for each client attribute, such as `client.items`. |
| {doc}`wow.search </reference/_generated/python/wow/search/index>` | The search filters `Range` and `Not`, and the largest page size. |

```{toctree}
:hidden:
:glob:

/reference/_generated/python/wow/index
/reference/_generated/python/wow/*/index
```
