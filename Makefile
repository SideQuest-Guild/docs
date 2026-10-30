.PHONY: install fetch generate docs serve clean

install:
	uv sync

fetch:
	uv run python scripts/fetch_sources.py

generate: fetch
	uv run python scripts/generate_developer_pages.py
	uv run python scripts/generate_api_reference.py

docs: generate
	uv run sphinx-build -b html source _build/html -W

serve: generate
	uv run sphinx-autobuild source _build/html --open-browser

clean:
	rm -rf _build .sources source/developers/_generated source/api/_generated
