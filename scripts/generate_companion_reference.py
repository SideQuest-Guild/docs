"""Generate the companion app's reference.

The companion app is Rust. When its repo has code, this runs `cargo doc
--no-deps` and publishes the output under `_build/html/reference/companion/rustdoc/`
via `html_extra_path`, and writes a stub page that links to it (rustdoc's own
HTML can't be inlined into a Sphinx page). If `cargo doc` itself fails on a
repo that has code, that's a real generator failure and this exits non-zero
so CI fails loudly rather than shipping an empty reference.

If repos.json marks the companion `"shipped": false`, or its repo has no
Cargo.toml, there's no Rust source to document: this writes an honest "not
shipped yet" page and still exits 0.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIR = ROOT / ".sources"
OUT_PAGE = ROOT / "source" / "reference" / "companion" / "_generated" / "index.md"
RUSTDOC_EXTRA_PATH = ROOT / "source" / "_extra_rustdoc" / "reference" / "companion" / "rustdoc"


def write_not_shipped(title: str, repo: str) -> None:
    OUT_PAGE.parent.mkdir(parents=True, exist_ok=True)
    OUT_PAGE.write_text(
        f"# {title}\n\n"
        f"The companion app's repo (`{repo}`) has no code in it yet, so there's no Rust "
        "source to generate a reference from. This page will build itself from "
        "`cargo doc --no-deps` as soon as the repo has a crate in it; check back once "
        "the companion app has shipped.\n"
    )
    # html_extra_path must point at an existing directory even when there's no rustdoc yet.
    RUSTDOC_EXTRA_PATH.mkdir(parents=True, exist_ok=True)
    (RUSTDOC_EXTRA_PATH / ".gitkeep").touch()


def main() -> int:
    data = json.loads((ROOT / "repos.json").read_text())
    source = next((s for s in data["sources"] if s["id"] == "companion"), None)
    if source is None:
        print("error: repos.json has no 'companion' source", file=sys.stderr)
        return 1

    repo_dir = SOURCES_DIR / "companion"
    src_dir = repo_dir / source["reference"]["rust"]["src_dir"]
    cargo_toml = repo_dir / "Cargo.toml"

    if not source.get("shipped", True) or not cargo_toml.exists():
        write_not_shipped(source["title"], source["repo"])
        print(f"wrote {OUT_PAGE.relative_to(ROOT)} (placeholder, companion not shipped yet)")
        return 0

    if shutil.which("cargo") is None:
        print("error: 'cargo' not found on PATH, cannot build the companion's Rust reference", file=sys.stderr)
        return 1

    if not src_dir.exists():
        print(f"error: {src_dir} not found even though {cargo_toml} exists", file=sys.stderr)
        return 1

    result = subprocess.run(
        ["cargo", "doc", "--no-deps"],
        cwd=repo_dir,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("error: `cargo doc --no-deps` failed:", file=sys.stderr)
        print(result.stdout, file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        return 1

    target_doc = repo_dir / "target" / "doc"
    if not target_doc.exists():
        print(f"error: {target_doc} not produced by cargo doc", file=sys.stderr)
        return 1

    if RUSTDOC_EXTRA_PATH.exists():
        shutil.rmtree(RUSTDOC_EXTRA_PATH)
    RUSTDOC_EXTRA_PATH.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(target_doc, RUSTDOC_EXTRA_PATH)

    # `cargo doc --no-deps` writes no top-level index.html, only one folder per crate, named after the library.
    manifest = tomllib.loads(cargo_toml.read_text())
    crate = manifest.get("lib", {}).get("name") or manifest["package"]["name"].replace("-", "_")
    if not (target_doc / crate / "index.html").exists():
        print(f"error: cargo doc produced no {crate}/index.html in {target_doc}", file=sys.stderr)
        return 1

    OUT_PAGE.parent.mkdir(parents=True, exist_ok=True)
    # A raw link: MyST would treat a Markdown link to a path outside the Sphinx project as a missing cross-reference.
    OUT_PAGE.write_text(
        f"# {source['title']}\n\n"
        "Generated from the companion app's own doc comments with "
        "`cargo doc --no-deps`.\n\n"
        f'<p><a href="../rustdoc/{crate}/index.html">Open the Rust reference</a></p>\n'
    )
    print(f"wrote {OUT_PAGE.relative_to(ROOT)} and copied rustdoc output to {RUSTDOC_EXTRA_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
