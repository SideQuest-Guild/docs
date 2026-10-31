from __future__ import annotations

import functools
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / ".sources"
REPOS = json.loads((ROOT / "repos.json").read_text())["sources"]
REPO_BY_ID = {s["id"]: s for s in REPOS}

project = "SideQuest Guild"
copyright = "SideQuest Guild"
author = "SideQuest Guild"

extensions = [
    "myst_parser",
    "sphinxcontrib.mermaid",
    "sphinx_design",
    # A [source] link on every class and function in the Python reference, opening the highlighted module as it
    # was when the site was built. autoapi feeds viewcode the source it already parsed, so nothing is imported, but
    # only if viewcode loads first: autoapi checks for viewcode's events when it is set up.
    "sphinx.ext.viewcode",
    "autoapi.extension",
]
viewcode_line_numbers = True

source_suffix = {
    ".md": "markdown",
    ".rst": "restructuredtext",
}

myst_enable_extensions = [
    "colon_fence",
    "deflist",
]
myst_fence_as_directive = ["mermaid"]
myst_heading_anchors = 3

root_doc = "index"

exclude_patterns = [
    "developers/_generated/*.md",
    "reference/website/http/_generated/toctree.md",
    "_build",
]

templates_path = ["_templates"]

html_theme = "shibuya"
html_static_path = ["_static"]
html_extra_path = ["_extra", "_extra_rustdoc"]
html_css_files = ["custom.css"]
html_title = "SideQuest Guild Docs"
html_baseurl = "https://docs.sidequest-guild.com/"
html_favicon = "_static/logo.png"

# -- Edit this page / repo card -----------------------------------------------
# Shibuya's built-in "Edit this page" link is baked once from the static
# html_context at builder-inited time, which can't vary per page. We don't use
# it: _templates/sidebars/edit-this-page.html reads `sq_edit_url`/`sq_edit_label`
# from the page context instead, set per page below. The repo-stats sidebar
# *does* read source_type/source_user/source_repo straight from the page
# context on every page, so that one just needs those three set per page.

DOCS_REPO = "SideQuest-Guild/docs"

html_context = {
    "source_type": "github",
    "source_user": "SideQuest-Guild",
    "source_repo": "docs",
    "source_version": "main",
    "source_docs_path": "/source/",
}


def _app_id_for_docname(docname: str) -> str | None:
    for app_id in ("website", "bot", "addon", "companion"):
        if docname == f"developers/{app_id}" or docname.startswith(f"developers/{app_id}/"):
            return app_id
        if docname == f"reference/{app_id}" or docname.startswith(f"reference/{app_id}/"):
            return app_id
        if docname == f"changelog/{app_id}":
            return app_id
    return None


# Where the Python reference's source lives: (app id, folder inside that repo). autoapi documents these folders, and
# the [source] pages viewcode writes for them (docnames under _modules/) link back to the file on GitHub.
PYTHON_SOURCE_DIRS = [("website", "packages/sidequest-common/src"), ("bot", "src")]


@functools.cache
def _source_commit(app_id: str) -> str:
    """The commit .sources/<app_id> is checked out at, so a GitHub link shows the code this build documented."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=SOURCES / app_id, capture_output=True, text=True, check=True
        )
    except (OSError, subprocess.CalledProcessError):
        return "main"
    return result.stdout.strip()


def _module_source(docname: str) -> tuple[str, str] | None:
    """(app id, file path in its repo) for a viewcode page such as ``_modules/sidequest_bot/api_client``."""
    if not docname.startswith("_modules/"):
        return None
    parts = docname.removeprefix("_modules/").split("/")
    for app_id, folder in PYTHON_SOURCE_DIRS:
        base = SOURCES / app_id / folder / Path(*parts)
        for candidate in (base.with_suffix(".py"), base / "__init__.py"):
            if candidate.is_file():
                return app_id, candidate.relative_to(SOURCES / app_id).as_posix()
    return None


def _page_repo_context(docname: str) -> dict:
    """source_type/source_user/source_repo for the repo-stats card on this page."""
    module = _module_source(docname)
    app_id = module[0] if module else _app_id_for_docname(docname)
    if app_id is None:
        return {"source_type": "github", "source_user": "SideQuest-Guild", "source_repo": "docs"}
    owner, name = REPO_BY_ID[app_id]["repo"].split("/")
    return {"source_type": "github", "source_user": owner, "source_repo": name}


def _edit_context(docname: str) -> dict:
    """sq_edit_url/sq_edit_label for the Edit this page sidebar link, or neither for generated pages."""
    app_id = _app_id_for_docname(docname)

    # A highlighted source page links to the same file on GitHub, at the commit this build documented.
    if docname.startswith("_modules/"):
        if (module := _module_source(docname)) is None:
            return {}
        app_id, path = module
        return {
            "sq_edit_url": f"https://github.com/{REPO_BY_ID[app_id]['repo']}/blob/{_source_commit(app_id)}/{path}",
            "sq_edit_label": "View on GitHub",
        }

    # Generated reference pages: no edit link, there's nothing to hand-edit.
    if docname.startswith("reference/") and "_generated" in docname:
        return {}
    if re.match(r"^reference/(website|bot)/python/", docname):
        return {}
    if docname.startswith("changelog/") and docname != "changelog/index":
        return {}

    # Generated README includes: edit link points at the source repo's own README.
    if app_id and docname == f"developers/{app_id}/readme":
        repo = REPO_BY_ID[app_id]["repo"]
        readme_path = REPO_BY_ID[app_id]["readme_path"]
        return {
            "sq_edit_url": f"https://github.com/{repo}/blob/main/{readme_path}",
            "sq_edit_label": "Edit on the source repo",
        }

    # Everything else is handwritten in this repo.
    return {
        "sq_edit_url": f"https://github.com/{DOCS_REPO}/blob/main/source/{docname}.md",
        "sq_edit_label": "Edit this page",
    }


def _install_changelog_pills(pathto, original_toctree):
    """Wrap Shibuya's `toctree()` jinja global to add a small Changelog pill
    after each app's Develop entry in the left sidebar, styled by custom.css
    (not the theme's red/danger color)."""

    def wrapped(*args, **kwargs):
        html = original_toctree(*args, **kwargs)
        if not html:
            return html
        for app_id in ("website", "bot", "addon", "companion"):
            pattern = re.compile(
                r'(<a class="[^"]*" href="([^"]*developers/' + app_id + r'/index\.html)">.*?</a>)'
            )
            changelog_href = pathto(f"changelog/{app_id}")
            html = pattern.sub(
                lambda m: m.group(1) + f'<a class="sq-changelog-pill" href="{changelog_href}">Changelog</a>',
                html,
                count=1,
            )
        return html

    return wrapped


def _html_page_context(app, pagename, templatename, context, doctree):
    context.update(_page_repo_context(pagename))
    context.update(_edit_context(pagename))
    pathto = context.get("pathto")
    original_toctree = context.get("toctree")
    if pathto is not None and callable(original_toctree):
        context["toctree"] = _install_changelog_pills(pathto, original_toctree)


def setup(app):
    app.connect("html-page-context", _html_page_context)


html_theme_options = {
    "accent_color": "gold",
    "color_mode": "auto",
    "light_logo": "_static/logo.png",
    "dark_logo": "_static/logo.png",
    "page_layout": "default",
    "github_url": "https://github.com/SideQuest-Guild",
    "discord_url": "https://discord.gg/nwncP7H9Hh",
    "nav_links": [
        {
            "title": "Guides",
            "children": [
                {"title": "Members", "url": "members/index", "summary": "Join, sign up for events, and track your points."},
                {"title": "Officers", "url": "officers/index", "summary": "Run events and raid nights, confirm members."},
            ],
        },
        {
            "title": "Develop",
            "children": [
                {"title": "Website & API", "url": "developers/website/index", "summary": "The Astro site and the Litestar API."},
                {"title": "Discord bot", "url": "developers/bot/index", "summary": "Game Master, the discord.py bot."},
                {"title": "Addon", "url": "developers/addon/index", "summary": "The in-game WoW addon and sidequest-sync."},
                {"title": "Companion", "url": "developers/companion/index", "summary": "The native tray sync app."},
                {"title": "API reference", "url": "reference/website/http/index", "summary": "Every HTTP route and data model."},
            ],
        },
        {
            "title": "Community",
            "children": [
                {"title": "Discord", "url": "https://discord.gg/nwncP7H9Hh"},
                {"title": "GitHub org", "url": "https://github.com/SideQuest-Guild"},
                {"title": "Contributing", "url": "contributing/index"},
                {"title": "Code of conduct", "url": "contributing/code-of-conduct"},
                {"title": "Open issues", "url": "https://github.com/issues?q=is%3Aopen+is%3Aissue+org%3ASideQuest-Guild"},
            ],
        },
        {
            "title": "Changelogs",
            "children": [
                {"title": "Website & API", "url": "changelog/website"},
                {"title": "Discord bot", "url": "changelog/bot"},
                {"title": "Addon", "url": "changelog/addon"},
                {"title": "Companion", "url": "changelog/companion"},
            ],
        },
        {"title": "Site", "url": "https://sidequest-guild.com", "external": True},
    ],
    "toctree_titles_only": True,
    "globaltoc_expand_depth": 1,
}

html_sidebars = {
    "**": [
        "sidebars/localtoc.html",
        "sidebars/repo-stats.html",
        "sidebars/edit-this-page.html",
    ],
}

# -- Python reference (sphinx-autoapi) ----------------------------------------
# One combined autoapi root; each app's reference page builds its own toctree
# into the relevant subtree instead of using autoapi's own auto-inserted one,
# so the website's and the bot's Python references can live on separate pages.

autoapi_type = "python"
autoapi_root = "reference/_generated/python"
autoapi_dirs = [str(SOURCES / app_id / folder) for app_id, folder in PYTHON_SOURCE_DIRS]
autoapi_add_toctree_entry = False
autoapi_keep_files = False
autoapi_member_order = "groupwise"
autoapi_python_class_content = "both"
# No "imported-members": with it every module page repeated each name it imports, which tripled the
# page count and the build time. The API's own package and the bot plugins are left out on purpose: the HTTP
# reference and the slash command page describe them better than their Python signatures do.
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
]
autoapi_ignore = [
    "*/migrations/*",
    "*/tests/*",
    "*/test_*.py",
    "*conftest.py",
    "*/__pycache__/*",
    "*/sidequest_bot/plugins/*",
]
suppress_warnings = ["autoapi.python_import_resolution"]
