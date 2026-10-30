"""Generate the bot's slash-command reference by reading its source with `ast`.

Walks every `.py` file under the bot's plugin directory (no import, so the
bot's own dependencies don't need to be installed here), finds every
`app_commands.Group(...)` assignment and every function decorated with
`<group>.command(...)` or `app_commands.command(...)`, and writes one Markdown
page listing every command's full `/...` path, its description, and whether
it needs a permission (read off `default_permissions=...`, inherited from the
nearest ancestor group when the command itself doesn't set one).
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIR = ROOT / ".sources"
OUT_FILE = ROOT / "source" / "reference" / "bot" / "_generated" / "commands.md"


def kwarg_text(call: ast.Call, name: str) -> str | None:
    for kw in call.keywords:
        if kw.arg == name:
            try:
                return str(ast.literal_eval(kw.value))
            except (ValueError, TypeError):
                return ast.unparse(kw.value)
    return None


def permission_text(call: ast.Call) -> str | None:
    """Render `default_permissions=discord.Permissions(manage_guild=True)` as "Manage Server"."""
    for kw in call.keywords:
        if kw.arg != "default_permissions":
            continue
        value = kw.value
        if isinstance(value, ast.Call):
            names = [k.arg for k in value.keywords if k.arg]
            if names:
                return ", ".join(n.replace("_", " ").title() for n in names)
        return ast.unparse(value)
    return None


class Group:
    __slots__ = ("var", "name", "description", "parent_var", "permission")

    def __init__(self, var: str, name: str, description: str | None, parent_var: str | None, permission: str | None):
        self.var = var
        self.name = name
        self.description = description
        self.parent_var = parent_var
        self.permission = permission


def collect_groups(tree: ast.AST) -> dict[str, Group]:
    groups: dict[str, Group] = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        if not isinstance(node.value, ast.Call):
            continue
        call = node.value
        func = call.func
        func_name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", None)
        if func_name != "Group":
            continue
        if len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
            continue
        var = node.targets[0].id
        name = kwarg_text(call, "name") or var
        description = kwarg_text(call, "description")
        permission = permission_text(call)
        parent_var = None
        for kw in call.keywords:
            if kw.arg == "parent" and isinstance(kw.value, ast.Name):
                parent_var = kw.value.id
        groups[var] = Group(var, name, description, parent_var, permission)
    return groups


def group_path(var: str, groups: dict[str, Group]) -> tuple[str, str | None]:
    """Full "/a b c" path and nearest-ancestor permission for a group var."""
    parts: list[str] = []
    permission: str | None = None
    current = groups.get(var)
    chain: list[Group] = []
    while current is not None:
        chain.append(current)
        current = groups.get(current.parent_var) if current.parent_var else None
    for g in reversed(chain):
        parts.append(g.name)
        if g.permission:
            permission = g.permission
    return " ".join(parts), permission


def is_command_decorator(dec: ast.expr, groups: dict[str, Group]) -> bool:
    if not isinstance(dec, ast.Call):
        return False
    func = dec.func
    if isinstance(func, ast.Attribute) and func.attr == "command":
        if isinstance(func.value, ast.Name) and (func.value.id == "app_commands" or func.value.id in groups):
            return True
    return False


def collect_commands(tree: ast.AST, groups: dict[str, Group]) -> list[dict[str, Any]]:
    commands: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        cmd_decorator: ast.Call | None = None
        group_var: str | None = None
        own_permission: str | None = None
        for dec in node.decorator_list:
            if is_command_decorator(dec, groups):
                cmd_decorator = dec  # type: ignore[assignment]
                func = dec.func  # type: ignore[union-attr]
                if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name) and func.value.id in groups:
                    group_var = func.value.id
            elif isinstance(dec, ast.Call):
                func = dec.func
                if isinstance(func, ast.Attribute) and func.attr == "default_permissions":
                    own_permission = permission_text(dec) or ", ".join(
                        kw.arg.replace("_", " ").title() for kw in dec.keywords if kw.arg
                    )
        if cmd_decorator is None:
            continue
        name = kwarg_text(cmd_decorator, "name") or node.name
        description = kwarg_text(cmd_decorator, "description") or ""
        prefix, inherited_permission = ("", None) if group_var is None else group_path(group_var, groups)
        path = f"/{(prefix + ' ' + name).strip()}" if prefix else f"/{name}"
        permission = own_permission or inherited_permission
        commands.append({"path": path, "description": description, "permission": permission})
    return commands


def main() -> int:
    data = json.loads((ROOT / "repos.json").read_text())
    bot_source = next((s for s in data["sources"] if s["id"] == "bot"), None)
    if bot_source is None:
        print("error: repos.json has no 'bot' source", file=sys.stderr)
        return 1

    src_dir = SOURCES_DIR / "bot" / bot_source["reference"]["commands"]["src_dir"]
    if not src_dir.exists():
        print(f"error: {src_dir} not found, run `make fetch` first", file=sys.stderr)
        return 1

    all_commands: list[dict[str, Any]] = []
    for py_file in sorted(src_dir.rglob("*.py")):
        try:
            tree = ast.parse(py_file.read_text(), filename=str(py_file))
        except SyntaxError as exc:
            print(f"error: could not parse {py_file}: {exc}", file=sys.stderr)
            return 1
        groups = collect_groups(tree)
        all_commands.extend(collect_commands(tree, groups))

    if not all_commands:
        print("error: found no slash commands in the bot source, refusing to write an empty reference", file=sys.stderr)
        return 1

    all_commands.sort(key=lambda c: c["path"])

    lines = [
        "# Slash commands",
        "",
        "Every `/` command Game Master registers, generated from the bot's own source so this "
        "list can't drift from what's actually deployed. \"Permission\" is the Discord server "
        "permission a member needs to run the command; a blank permission means anyone can run "
        "it.",
        "",
        "| Command | Description | Permission |",
        "|---|---|---|",
    ]
    for cmd in all_commands:
        desc = cmd["description"].replace("|", "\\|")
        perm = (cmd["permission"] or "").replace("|", "\\|")
        lines.append(f"| `{cmd['path']}` | {desc} | {perm} |")
    lines.append("")

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text("\n".join(lines))
    print(f"wrote {len(all_commands)} commands to {OUT_FILE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
