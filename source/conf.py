project = "SideQuest Guild"
copyright = "SideQuest Guild"
author = "SideQuest Guild"

extensions = [
    "myst_parser",
    "sphinxcontrib.mermaid",
]

source_suffix = {
    ".md": "markdown",
}

myst_enable_extensions = [
    "colon_fence",
    "deflist",
]
myst_fence_as_directive = ["mermaid"]

root_doc = "index"

exclude_patterns = [
    "developers/_generated/*.md",
    "api/_generated/toctree.md",
    "_build",
]

html_theme = "shibuya"
html_static_path = ["_static"]
html_extra_path = ["_extra"]
html_css_files = ["custom.css"]
html_title = "SideQuest Guild Docs"
html_baseurl = "https://docs.sidequest-guild.com/"
html_favicon = "_static/logo.png"

html_theme_options = {
    "accent_color": "gold",
    "color_mode": "auto",
    "light_logo": "_static/logo.png",
    "dark_logo": "_static/logo.png",
    "github_url": "https://github.com/SideQuest-Guild",
    "discord_url": "https://discord.gg/nwncP7H9Hh",
    "nav_links": [
        {"title": "Site", "url": "https://sidequest-guild.com"},
    ],
}

myst_heading_anchors = 3
