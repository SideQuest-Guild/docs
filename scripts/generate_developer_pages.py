"""Turn each source repo's README, and any docs guides it lists, into developer pages.

Reads repos.json, pulls the README out of .sources/<id> (populated by
fetch_sources.py locally, or by actions/checkout in CI), rewrites relative
links and images so they point at GitHub instead of a path that only exists
in the cloned checkout, and writes the result to
source/developers/_generated/<id>.md. The checked-in page at
source/developers/<id>.md pulls this file in with a MyST `include` directive.

A source can also list `guides`: paths (relative to its repo root) of other
Markdown pages to publish the same way, such as the WoW Forever SDK's usage
and models guides. Each one is rewritten the same way and written to
source/developers/_generated/<id>-<stem>.md, where a checked-in wrapper page
includes it.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIR = ROOT / ".sources"
OUT_DIR = ROOT / "source" / "developers" / "_generated"

# Markdown image: ![alt](path "title")
MD_IMAGE = re.compile(r'(!\[[^\]]*\]\()([^)\s]+)((?:\s+"[^"]*")?\))')
# Markdown link (not image, so no leading !): [text](path "title")
MD_LINK = re.compile(r'(?<!!)(\[[^\]]*\]\()([^)\s]+)((?:\s+"[^"]*")?\))')
# HTML attributes: src="path" or href="path"
HTML_ATTR = re.compile(r'((?:src|href)=")([^"]+)(")')


def is_absolute(path: str) -> bool:
    return path.startswith(("http://", "https://", "mailto:", "#"))


def rewrite_path(path: str, repo: str, kind: str) -> str:
    """kind is 'image' (raw content) or 'link' (blob view)."""
    if is_absolute(path):
        return path
    anchor = ""
    clean = path
    if "#" in path:
        clean, _, anchor = path.partition("#")
        anchor = f"#{anchor}"
    if clean.startswith("./"):
        clean = clean[2:]
    if not clean:
        return path
    if kind == "image":
        return f"https://raw.githubusercontent.com/{repo}/main/{clean}{anchor}"
    return f"https://github.com/{repo}/blob/main/{clean}{anchor}"


def rewrite_readme(text: str, repo: str) -> str:
    text = MD_IMAGE.sub(lambda m: m.group(1) + rewrite_path(m.group(2), repo, "image") + m.group(3), text)
    text = MD_LINK.sub(lambda m: m.group(1) + rewrite_path(m.group(2), repo, "link") + m.group(3), text)

    def html_sub(m: re.Match[str]) -> str:
        attr, path, close = m.group(1), m.group(2), m.group(3)
        kind = "image" if attr.startswith("src") else "link"
        return attr + rewrite_path(path, repo, kind) + close

    text = HTML_ATTR.sub(html_sub, text)
    return text


def main() -> int:
    data = json.loads((ROOT / "repos.json").read_text())
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for source in data["sources"]:
        readme = SOURCES_DIR / source["id"] / source["readme_path"]
        if not readme.exists():
            if source.get("shipped", True):
                print(f"error: {readme} not found, run `make fetch` first", file=sys.stderr)
                return 1
            out = OUT_DIR / f"{source['id']}.md"
            out.write_text(
                f"The **{source['title']}** repo (`{source['repo']}`) has no code in it yet, "
                "so there's no README to show here. Check the repo directly for its current "
                "state.\n"
            )
            print(f"wrote {out.relative_to(ROOT)} (placeholder, repo not shipped yet)")
            continue
        rewritten = rewrite_readme(readme.read_text(), source["repo"])
        out = OUT_DIR / f"{source['id']}.md"
        out.write_text(rewritten)
        print(f"wrote {out.relative_to(ROOT)}")

        for guide_path in source.get("guides", []):
            guide = SOURCES_DIR / source["id"] / guide_path
            stem = Path(guide_path).stem
            if not guide.exists():
                print(f"error: {guide} not found, run `make fetch` first", file=sys.stderr)
                return 1
            rewritten_guide = rewrite_readme(guide.read_text(), source["repo"])
            guide_out = OUT_DIR / f"{source['id']}-{stem}.md"
            guide_out.write_text(rewritten_guide)
            print(f"wrote {guide_out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
