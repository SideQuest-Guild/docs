"""Generate the addon's reference: its `/sq` slash commands and the SQX1/SQI1
export/import formats.

Slash commands are read from the addon's own Lua source with a small
block-depth scanner (no Lua parser dependency): every
`SideQuest.RegisterSlash("word", function(...) ... end[, "help text"])` call
becomes one row. The SQX1/SQI1 field tables are read from the website's own
pydantic models in `packages/sidequest-common` with `ast` (the formats are
defined once there, per the contract; the addon side only encodes/decodes
them), so these pages can't drift from the real contract on either side.
"""

from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIR = ROOT / ".sources"
OUT_DIR = ROOT / "source" / "reference" / "addon" / "_generated"

OPENERS = re.compile(r"\b(function|if|for|while|do|repeat)\b")
CLOSERS = re.compile(r"\b(end|until)\b")
REGISTER_RE = re.compile(r'SideQuest\.RegisterSlash\(\s*"([%\w_-]+)"\s*,\s*function')
TRAILING_HELP_RE = re.compile(r'"([^"]*)"\s*\)')


def net_depth_change(line: str) -> int:
    # Strip comments and string literals roughly, to avoid counting keywords inside them.
    line = re.sub(r"--.*$", "", line)
    line = re.sub(r'"[^"]*"', '""', line)
    opens = len(OPENERS.findall(line))
    closes = len(CLOSERS.findall(line))
    return opens - closes


def find_slash_commands(text: str) -> list[dict[str, str]]:
    lines = text.splitlines()
    commands: list[dict[str, str]] = []
    i = 0
    while i < len(lines):
        m = REGISTER_RE.search(lines[i])
        if not m:
            i += 1
            continue
        keyword = m.group(1)
        # The `function` keyword on this line opens one block; scan forward until it closes.
        depth = net_depth_change(lines[i][m.end() - len("function") :])
        j = i
        while depth > 0 and j + 1 < len(lines):
            j += 1
            depth += net_depth_change(lines[j])
        # Help text, if any, is a quoted string after the closing `end` on line j (or soon after).
        help_text = ""
        for k in (j, j + 1):
            if k >= len(lines):
                break
            hm = TRAILING_HELP_RE.search(lines[k])
            if hm and "end" in lines[k]:
                help_text = hm.group(1)
                break
        commands.append({"keyword": keyword, "help": help_text})
        i = j + 1
    return commands


# --- SQX1/SQI1 field tables, read from the website's pydantic models ------------------------


def annotation_text(node: ast.expr | None) -> str:
    if node is None:
        return "any"
    return ast.unparse(node).replace("sidequest_common.schemas.", "")


def field_default_and_description(value: ast.expr | None) -> tuple[bool, str]:
    """Returns (has_explicit_default, description)."""
    if value is None:
        return False, ""
    if isinstance(value, ast.Call) and isinstance(value.func, ast.Name) and value.func.id == "Field":
        desc = ""
        has_default = False
        for kw in value.keywords:
            if kw.arg == "description":
                try:
                    desc = ast.literal_eval(kw.value)
                except (ValueError, TypeError):
                    pass
            if kw.arg in ("default", "default_factory"):
                has_default = True
        for arg in value.args:
            has_default = True
        return has_default, desc
    return True, ""


def collect_models(tree: ast.Module) -> dict[str, ast.ClassDef]:
    return {
        node.name: node
        for node in ast.walk(tree)
        if isinstance(node, ast.ClassDef) and any(isinstance(b, ast.Name) and b.id == "BaseModel" for b in node.bases)
    }


def referenced_model_names(annotation: ast.expr, known: set[str]) -> set[str]:
    return {n for n in known if re.search(rf"\b{re.escape(n)}\b", ast.unparse(annotation))}


def render_model(name: str, models: dict[str, ast.ClassDef], rendered: set[str], lines: list[str]) -> None:
    if name in rendered or name not in models:
        return
    rendered.add(name)
    cls = models[name]
    lines.append(f"## `{name}`")
    lines.append("")
    doc = ast.get_docstring(cls)
    if doc:
        lines.append(doc.strip().splitlines()[0])
        lines.append("")
    fields: list[tuple[str, str, bool, str]] = []
    nested: set[str] = set()
    known = set(models)
    for stmt in cls.body:
        if not isinstance(stmt, ast.AnnAssign) or not isinstance(stmt.target, ast.Name):
            continue
        field_name = stmt.target.id
        if field_name == "model_config":
            continue
        ann_text = annotation_text(stmt.annotation)
        has_default, desc = field_default_and_description(stmt.value)
        optional = has_default or "| None" in ann_text or ann_text.startswith("Optional[")
        fields.append((field_name, ann_text, not optional, desc))
        nested |= referenced_model_names(stmt.annotation, known)
    if fields:
        lines.append("| Field | Type | Required | Description |")
        lines.append("|---|---|---|---|")
        for field_name, ann_text, required, desc in fields:
            safe_type = ann_text.replace("|", "\\|")
            safe_desc = desc.replace("|", "\\|")
            lines.append(f"| `{field_name}` | `{safe_type}` | {'yes' if required else 'no'} | {safe_desc} |")
        lines.append("")
    for n in sorted(nested - rendered):
        render_model(n, models, rendered, lines)


def render_format(title: str, prefix: str, root_class: str, models: dict[str, ast.ClassDef], intro: str) -> str:
    lines = [f"# {title}", "", intro, ""]
    rendered: set[str] = set()
    render_model(root_class, models, rendered, lines)
    return "\n".join(lines)


def main() -> int:
    data = json.loads((ROOT / "repos.json").read_text())
    addon_source = next((s for s in data["sources"] if s["id"] == "addon"), None)
    if addon_source is None:
        print("error: repos.json has no 'addon' source", file=sys.stderr)
        return 1

    addon_dir = SOURCES_DIR / "addon" / addon_source["reference"]["lua"]["src_dir"]
    if not addon_dir.exists():
        print(f"error: {addon_dir} not found, run `make fetch` first", file=sys.stderr)
        return 1

    all_commands: list[dict[str, str]] = []
    for lua_file in sorted(addon_dir.glob("*.lua")):
        all_commands.extend(find_slash_commands(lua_file.read_text()))

    if not all_commands:
        print("error: found no /sq slash commands in the addon source, refusing to write an empty reference", file=sys.stderr)
        return 1

    schemas_dir = SOURCES_DIR / "website" / "packages" / "sidequest-common" / "src" / "sidequest_common" / "schemas"
    epgp_file = schemas_dir / "epgp.py"
    if not epgp_file.exists():
        print(f"error: {epgp_file} not found, run `make fetch` first", file=sys.stderr)
        return 1
    tree = ast.parse(epgp_file.read_text(), filename=str(epgp_file))
    models = collect_models(tree)
    if "ExportPayload" not in models or "GameImportPayload" not in models:
        print("error: ExportPayload/GameImportPayload not found in the website's epgp schema module", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    commands_lines = [
        "# Slash commands",
        "",
        "Every `/sq` subcommand, generated from the addon's own `SideQuest.RegisterSlash` calls.",
        "",
        "| Command | What it does |",
        "|---|---|",
    ]
    all_commands.sort(key=lambda c: c["keyword"])
    for cmd in all_commands:
        commands_lines.append(f"| `/sq {cmd['keyword']}` | {cmd['help']} |")
    commands_lines.append("")
    (OUT_DIR / "commands.md").write_text("\n".join(commands_lines))

    sqx1 = render_format(
        "SQX1: raid export format",
        "SQX1:",
        "ExportPayload",
        models,
        "The addon builds this payload, JSON-encodes it, base64s it, and prefixes it with "
        "`SQX1:` to make one paste-able string. An officer sends it to the site with "
        "`/sq export`, through the companion app, or by pasting it on `/officers/sync/`. "
        "Defined once in the website's `packages/sidequest-common`, so this table always "
        "matches what the site actually accepts.",
    )
    (OUT_DIR / "sqx1.md").write_text(sqx1)

    sqi1 = render_format(
        "SQI1: game import format",
        "SQI1:",
        "GameImportPayload",
        models,
        "The site builds this payload from `GET /api/epgp/game-import`, JSON-encodes it, "
        "base64s it, and prefixes it with `SQI1:` to make one paste-able string. The addon "
        "decodes it with `/sq import`, or receives it automatically through the companion app. "
        "Defined once in the website's `packages/sidequest-common`, so this table always "
        "matches what the addon actually receives.",
    )
    (OUT_DIR / "sqi1.md").write_text(sqi1)

    print(
        f"wrote {len(all_commands)} slash commands, SQX1 ({len(_models_rendered('ExportPayload', models))} models), "
        f"SQI1 ({len(_models_rendered('GameImportPayload', models))} models)"
    )
    return 0


def _models_rendered(root: str, models: dict[str, ast.ClassDef]) -> set[str]:
    rendered: set[str] = set()
    render_model(root, models, rendered, [])
    return rendered


if __name__ == "__main__":
    sys.exit(main())
