"""Fetch the live OpenAPI schema and write one Markdown page per tag.

The API reference is generated at build time from the running site's schema,
never hand copied, so it can't drift. If the fetch fails this exits non-zero,
which fails the CI build loudly instead of shipping a stale or empty page.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Any

import httpx

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "source" / "api" / "_generated"
DEFAULT_URL = "https://sidequest-guild.com/schema/openapi.json"
METHODS = ("get", "post", "put", "patch", "delete")


def slugify(tag: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", tag.lower()).strip("-")


def resolve_ref(ref: str, schemas: dict[str, Any]) -> tuple[str, dict[str, Any]] | None:
    if not ref.startswith("#/components/schemas/"):
        return None
    name = ref.removeprefix("#/components/schemas/")
    schema = schemas.get(name)
    if schema is None:
        return None
    return name, schema


def type_label(schema: dict[str, Any], schemas: dict[str, Any]) -> str:
    if "$ref" in schema:
        resolved = resolve_ref(schema["$ref"], schemas)
        return resolved[0] if resolved else schema["$ref"]
    if "allOf" in schema and len(schema["allOf"]) == 1:
        return type_label(schema["allOf"][0], schemas)
    for key in ("oneOf", "anyOf"):
        if key in schema:
            return " \\| ".join(type_label(s, schemas) for s in schema[key])
    t = schema.get("type")
    if isinstance(t, list):
        t = " \\| ".join(str(x) for x in t)
    if t == "array":
        items = schema.get("items", {})
        return f"array of {type_label(items, schemas)}"
    if t is None:
        return "any"
    fmt = schema.get("format")
    return f"{t} ({fmt})" if fmt else str(t)


def properties_table(schema: dict[str, Any], schemas: dict[str, Any], depth: int = 0) -> list[str]:
    """Render an object schema's fields as a Markdown table. Follows one $ref level."""
    if "$ref" in schema:
        resolved = resolve_ref(schema["$ref"], schemas)
        if resolved is None:
            return []
        _, schema = resolved
    if "allOf" in schema:
        lines: list[str] = []
        for sub in schema["allOf"]:
            lines.extend(properties_table(sub, schemas, depth))
        return lines

    props = schema.get("properties")
    if not props:
        return []
    required = set(schema.get("required", []))
    lines = ["| Field | Type | Required | Description |", "|---|---|---|---|"]
    for name, prop in props.items():
        desc = (prop.get("description") or "").replace("\n", " ").replace("|", "\\|")
        lines.append(f"| `{name}` | {type_label(prop, schemas)} | {'yes' if name in required else 'no'} | {desc} |")
    return lines


def render_operation(path: str, method: str, op: dict[str, Any], schemas: dict[str, Any]) -> list[str]:
    lines = [f"## `{method.upper()} {path}`", ""]
    summary = op.get("summary")
    if summary:
        lines.append(f"**{summary}**")
        lines.append("")
    description = op.get("description")
    if description:
        lines.append(description)
        lines.append("")

    params = op.get("parameters", [])
    if params:
        lines.append("**Parameters**")
        lines.append("")
        lines.append("| Name | In | Type | Required | Description |")
        lines.append("|---|---|---|---|---|")
        for p in params:
            schema = p.get("schema", {})
            desc = (p.get("description") or "").replace("\n", " ").replace("|", "\\|")
            lines.append(
                f"| `{p['name']}` | {p.get('in', '')} | {type_label(schema, schemas)} | "
                f"{'yes' if p.get('required') else 'no'} | {desc} |"
            )
        lines.append("")

    body = op.get("requestBody")
    if body:
        content = body.get("content", {})
        json_body = content.get("application/json")
        if json_body:
            lines.append("**Request body**")
            lines.append("")
            table = properties_table(json_body.get("schema", {}), schemas)
            lines.extend(table if table else [f"Type: {type_label(json_body.get('schema', {}), schemas)}"])
            lines.append("")

    responses = op.get("responses", {})
    success = {code: r for code, r in responses.items() if code.startswith("2")}
    for code, resp in success.items():
        content = resp.get("content", {})
        json_resp = content.get("application/json")
        lines.append(f"**Response `{code}`** — {resp.get('description', '')}")
        lines.append("")
        if json_resp:
            table = properties_table(json_resp.get("schema", {}), schemas)
            if table:
                lines.extend(table)
                lines.append("")
            else:
                lines.append(f"Type: {type_label(json_resp.get('schema', {}), schemas)}")
                lines.append("")

    lines.append("")
    return lines


def main() -> int:
    url = os.environ.get("OPENAPI_URL", DEFAULT_URL)
    try:
        resp = httpx.get(url, timeout=30, follow_redirects=True)
        resp.raise_for_status()
        spec = resp.json()
    except Exception as exc:  # noqa: BLE001 - must fail loudly, any error is fatal
        print(f"error: could not fetch OpenAPI schema from {url}: {exc}", file=sys.stderr)
        return 1

    schemas = spec.get("components", {}).get("schemas", {})
    by_tag: dict[str, list[tuple[str, str, dict[str, Any]]]] = {}
    for path, methods in spec.get("paths", {}).items():
        for method in METHODS:
            op = methods.get(method)
            if not op:
                continue
            for tag in op.get("tags") or ["Untagged"]:
                by_tag.setdefault(tag, []).append((path, method, op))

    if not by_tag:
        print("error: OpenAPI schema had no operations, refusing to write an empty reference", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_DIR.glob("*.md"):
        old.unlink()

    tag_slugs: list[tuple[str, str]] = []
    for tag in sorted(by_tag):
        slug = slugify(tag)
        tag_slugs.append((tag, slug))
        lines = [f"# {tag}", ""]
        for path, method, op in sorted(by_tag[tag], key=lambda x: (x[0], x[1])):
            lines.extend(render_operation(path, method, op, schemas))
        (OUT_DIR / f"{slug}.md").write_text("\n".join(lines))

    toctree = ["```{toctree}", ":maxdepth: 1", ":hidden:", ""]
    toctree += [f"_generated/{slug}" for _, slug in tag_slugs]
    toctree.append("```")
    toctree.append("")
    (OUT_DIR / "toctree.md").write_text("\n".join(toctree))

    print(f"wrote {len(tag_slugs)} API reference pages from {url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
