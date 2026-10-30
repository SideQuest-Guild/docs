"""Clone or update the repos listed in repos.json into .sources/<id>.

Used by `make docs` and `make serve` for local builds. CI uses actions/checkout
into the same .sources/<id> layout instead, so the scripts that read from
.sources/ work the same way in both places.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIR = ROOT / ".sources"


def load_repos() -> list[dict]:
    data = json.loads((ROOT / "repos.json").read_text())
    return data["sources"]


def fetch_one(source: dict) -> None:
    dest = SOURCES_DIR / source["id"]
    url = f"https://github.com/{source['repo']}.git"
    if dest.exists():
        print(f"updating {source['id']} ({source['repo']})")
        subprocess.run(["git", "-C", str(dest), "fetch", "--depth", "1", "origin"], check=True)
        subprocess.run(["git", "-C", str(dest), "reset", "--hard", "FETCH_HEAD"], check=True)
    else:
        print(f"cloning {source['id']} ({source['repo']})")
        SOURCES_DIR.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", "--depth", "1", url, str(dest)], check=True)


def main() -> int:
    for source in load_repos():
        fetch_one(source)
    return 0


if __name__ == "__main__":
    sys.exit(main())
