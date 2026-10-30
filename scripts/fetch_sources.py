"""Clone or update the repos listed in repos.json into .sources/<id>.

Used by `make docs` and `make serve` for local builds. CI uses actions/checkout
into the same .sources/<id> layout instead, so the scripts that read from
.sources/ work the same way in both places. Clones are full (no --depth), not
shallow: the changelog generator runs `git log`/git-cliff over each repo's
full history, which a shallow clone can't give it.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIR = ROOT / ".sources"


# The repos are public, so fetch them over plain HTTPS and skip the user's global git config: a
# `url.git@github.com:.insteadOf https://github.com/` rule there would route these through SSH and
# fail whenever the SSH agent is locked.
GIT_ENV = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_TERMINAL_PROMPT": "0"}


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], check=check, env=GIT_ENV, capture_output=not check)

def load_repos() -> list[dict]:
    data = json.loads((ROOT / "repos.json").read_text())
    return data["sources"]


def fetch_one(source: dict) -> None:
    dest = SOURCES_DIR / source["id"]
    url = f"https://github.com/{source['repo']}.git"
    if dest.exists():
        print(f"updating {source['id']} ({source['repo']})")
        git("-C", str(dest), "remote", "set-url", "origin", url)
        git("-C", str(dest), "fetch", "origin")
        if git("-C", str(dest), "rev-parse", "--verify", "--quiet", "FETCH_HEAD", check=False).returncode != 0:
            # A repo with nothing pushed yet (the generators treat an empty checkout as "no code yet").
            print(f"  {source['repo']} has no commits yet; nothing to update")
            return
        git("-C", str(dest), "reset", "--hard", "FETCH_HEAD")
    else:
        print(f"cloning {source['id']} ({source['repo']})")
        SOURCES_DIR.mkdir(parents=True, exist_ok=True)
        git("clone", url, str(dest))


def main() -> int:
    for source in load_repos():
        fetch_one(source)
    return 0


if __name__ == "__main__":
    sys.exit(main())
