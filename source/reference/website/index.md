# Website & API

The Astro site and the Litestar API that runs sidequest-guild.com.

- **[HTTP API](http/index.md)**: every route and data model, generated from the live OpenAPI
  schema.
- **Python reference**: the `sidequest-common` package, with the models, schemas and settings that
  the website and the bot share. Each module has its own page in the menu, generated from its doc
  comments. Select **[source]** beside a class or a function to read its code.

```{toctree}
:hidden:
:glob:

http/index
/reference/_generated/python/sidequest_common/*/index
```
