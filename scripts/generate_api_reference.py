"""Fetch the live OpenAPI schema and write the website's HTTP API reference.

Writes one Markdown page per operation tag plus one Models page (one entry per
component schema, with a field table), grouped in the sidebar by the schema's
`x-tagGroups` extension when present (Scalar's convention, same one the
site's own /api-reference/ page groups by). Falls back to one flat group
("API") when `x-tagGroups` is absent, so this keeps working before and after
that extension is added to the schema.

If the fetch fails or the schema has no operations, this exits non-zero: the
build must fail loudly rather than ship a stale or empty reference.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Any

import httpx

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "source" / "reference" / "website" / "http" / "_generated"
MODELS_FILE = OUT_DIR / "models.md"
DEFAULT_URL = "https://sidequest-guild.com/schema/openapi.json"
METHODS = ("get", "post", "put", "patch", "delete")


def slugify(tag: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", tag.lower()).strip("-")


def model_anchor(name: str) -> str:
    return f"model-{slugify(name)}"


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
        if resolved is None:
            return schema["$ref"]
        name, _ = resolved
        return f"{{ref}}`{name} <{model_anchor(name)}>`"
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


def properties_table(schema: dict[str, Any], schemas: dict[str, Any]) -> list[str]:
    """Render an object schema's fields as a Markdown table. Follows one $ref level."""
    if "$ref" in schema:
        resolved = resolve_ref(schema["$ref"], schemas)
        if resolved is None:
            return []
        _, schema = resolved
    if "allOf" in schema:
        lines: list[str] = []
        for sub in schema["allOf"]:
            lines.extend(properties_table(sub, schemas))
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


def model_link(schema: dict[str, Any], schemas: dict[str, Any]) -> str | None:
    """If schema resolves to a named component (directly or via a single allOf), link it."""
    if "$ref" in schema:
        resolved = resolve_ref(schema["$ref"], schemas)
        if resolved:
            name, _ = resolved
            return f"Model: {{ref}}`{name} <{model_anchor(name)}>`"
    if "allOf" in schema and len(schema["allOf"]) == 1:
        return model_link(schema["allOf"][0], schemas)
    if schema.get("type") == "array" and "$ref" in schema.get("items", {}):
        resolved = resolve_ref(schema["items"]["$ref"], schemas)
        if resolved:
            name, _ = resolved
            return f"Model: array of {{ref}}`{name} <{model_anchor(name)}>`"
    return None


def render_body_block(label: str, schema: dict[str, Any], schemas: dict[str, Any]) -> list[str]:
    lines = [f"**{label}**", ""]
    link = model_link(schema, schemas)
    if link:
        lines.append(link)
        lines.append("")
    table = properties_table(schema, schemas)
    lines.extend(table if table else [f"Type: {type_label(schema, schemas)}"])
    lines.append("")
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
            lines.extend(render_body_block("Request body", json_body.get("schema", {}), schemas))

    responses = op.get("responses", {})
    success = {code: r for code, r in responses.items() if code.startswith("2")}
    for code, resp in success.items():
        content = resp.get("content", {})
        json_resp = content.get("application/json")
        if json_resp:
            lines.extend(render_body_block(f"Response `{code}` \u2014 {resp.get('description', '')}", json_resp.get("schema", {}), schemas))
        else:
            lines.append(f"**Response `{code}`** \u2014 {resp.get('description', '')}")
            lines.append("")

    lines.append("")
    return lines


def render_models(schemas: dict[str, Any]) -> str:
    lines = [
        "# Models",
        "",
        "Every data shape the website's API sends or accepts, generated from the OpenAPI "
        "schema's `components/schemas`. Operation pages link to these entries instead of "
        "repeating field tables.",
        "",
    ]
    for name in sorted(schemas):
        schema = schemas[name]
        lines.append(f"({model_anchor(name)})=")
        lines.append(f"## `{name}`")
        lines.append("")
        description = schema.get("description")
        if description:
            lines.append(description)
            lines.append("")
        table = properties_table(schema, schemas)
        if table:
            lines.extend(table)
        else:
            lines.append(f"Type: {type_label(schema, schemas)}")
        lines.append("")
    return "\n".join(lines)


def build_tag_groups(spec: dict[str, Any], tags_present: set[str]) -> list[tuple[str, list[str]]]:
    """Return [(group name, [tag, ...]), ...] from x-tagGroups, falling back to one flat group."""
    raw_groups = spec.get("x-tagGroups")
    if not raw_groups:
        return [("API", sorted(tags_present))]
    groups: list[tuple[str, list[str]]] = []
    grouped_tags: set[str] = set()
    for group in raw_groups:
        tags = [t for t in group.get("tags", []) if t in tags_present]
        if not tags:
            continue
        groups.append((group["name"], tags))
        grouped_tags.update(tags)
    leftover = sorted(tags_present - grouped_tags)
    if leftover:
        groups.append(("Other", leftover))
    return groups


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

    if OUT_DIR.exists():
        for old in OUT_DIR.glob("*.md"):
            old.unlink()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    tag_slugs: dict[str, str] = {}
    for tag in sorted(by_tag):
        slug = slugify(tag)
        tag_slugs[tag] = slug
        lines = [f"# {tag}", ""]
        for path, method, op in sorted(by_tag[tag], key=lambda x: (x[0], x[1])):
            lines.extend(render_operation(path, method, op, schemas))
        (OUT_DIR / f"{slug}.md").write_text("\n".join(lines))

    groups = build_tag_groups(spec, set(by_tag))

    toctree: list[str] = []
    for group_name, tags in groups:
        toctree.append("```{toctree}")
        toctree.append(f":caption: {group_name}")
        toctree.append(":maxdepth: 1")
        toctree.append("")
        for tag in tags:
            toctree.append(f"_generated/{tag_slugs[tag]}")
        toctree.append("```")
        toctree.append("")
    toctree.append("```{toctree}")
    toctree.append(":caption: Reference")
    toctree.append(":maxdepth: 1")
    toctree.append("")
    toctree.append("_generated/models")
    toctree.append("```")
    toctree.append("")
    (OUT_DIR / "toctree.md").write_text("\n".join(toctree))

    MODELS_FILE.write_text(render_models(schemas))

    grouped_note = "x-tagGroups" if spec.get("x-tagGroups") else "flat (no x-tagGroups yet)"
    print(f"wrote {len(tag_slugs)} operation pages + {len(schemas)} models from {url} ({grouped_note})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
