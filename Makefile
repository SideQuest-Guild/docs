.PHONY: install fetch generate docs serve clean

install:
	uv sync

fetch:
	uv run python scripts/fetch_sources.py

generate: fetch
	uv run python scripts/generate_developer_pages.py
	uv run python scripts/generate_api_reference.py
	uv run python scripts/generate_bot_commands.py
	uv run python scripts/generate_addon_reference.py
	uv run python scripts/generate_companion_reference.py
	uv run python scripts/generate_changelogs.py

# -E: a fresh environment each build. AutoAPI rewrites its pages from scratch, so a cached
# environment can still point at a module page that a source repo has since moved or removed.
docs: generate
	uv run sphinx-build -E -b html source _build/html -W

serve: generate
	uv run sphinx-autobuild source _build/html --open-browser

clean:
	rm -rf _build .sources source/_extra_rustdoc \
		source/developers/_generated \
		source/reference/_generated \
		source/reference/website/http/_generated \
		source/reference/bot/_generated \
		source/reference/addon/_generated \
		source/reference/companion/_generated \
		source/changelog/_generated
