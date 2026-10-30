"""Generate one changelog page per app under source/changelog/.

Uses the repo's own `CHANGELOG.md` when it has one (the addon does, built
with its own `cliff.toml`). Otherwise runs `git-cliff` over the repo's full
Conventional Commit history with the shared `scripts/cliff.toml` (feat/fix/perf
only, grouped by release tag, "Unreleased" first). Needs each repo's full
history, so `fetch_sources.py` clones full, and CI's checkout must use
`fetch-depth: 0`.

A repo with no code yet (companion, before it ships) gets an honest "nothing
shipped yet" page instead of running git-cliff against an empty repo.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIR = ROOT / ".sources"
OUT_DIR = ROOT / "source" / "changelog" / "_generated"
CLIFF_CONFIG = ROOT / "scripts" / "cliff.toml"


def write_not_shipped(out: Path, title: str, repo: str) -> None:
    out.write_text(
        f"# {title}\n\n"
        f"The {title} repo (`{repo}`) has no code in it yet, so there is nothing to show "
        "here. Check back once it has shipped its first release.\n"
    )


def run_git_cliff(repo_dir: Path) -> str:
    result = subprocess.run(
        ["git-cliff", "--config", str(CLIFF_CONFIG), "--repository", str(repo_dir)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git-cliff failed")
    return result.stdout


def main() -> int:
    data = json.loads((ROOT / "repos.json").read_text())
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    if shutil.which("git-cliff") is None:
        print("error: 'git-cliff' not found on PATH", file=sys.stderr)
        return 1

    for source in data["sources"]:
        repo_dir = SOURCES_DIR / source["id"]
        out = OUT_DIR / f"{source['id']}.md"

        if not source.get("shipped", True) or not (repo_dir / ".git").exists():
            write_not_shipped(out, source["title"], source["repo"])
            print(f"wrote {out.relative_to(ROOT)} (placeholder, not shipped yet)")
            continue

        changelog_path = source.get("changelog", {}).get("path")
        own_changelog = repo_dir / changelog_path if changelog_path else None

        if own_changelog and own_changelog.exists():
            body = own_changelog.read_text()
            print(f"{source['id']}: using its own {changelog_path}")
        else:
            try:
                body = run_git_cliff(repo_dir)
            except RuntimeError as exc:
                print(f"error: git-cliff failed for {source['id']} ({repo_dir}): {exc}", file=sys.stderr)
                return 1
            print(f"{source['id']}: generated with git-cliff from commit history")

        releases_url = f"https://github.com/{source['repo']}/releases"
        header = (
            f"# {source['title']}\n\n"
            f"[See every release on GitHub]({releases_url}).\n\n"
        )
        # Strip the source's own leading "# Changelog" header, if any, so we don't duplicate titles.
        lines = body.splitlines()
        if lines and lines[0].lstrip("#").strip().lower() in ("changelog", "change log"):
            lines = lines[1:]
        body = "\n".join(lines).strip()

        out.write_text(header + body + "\n")
        print(f"wrote {out.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
