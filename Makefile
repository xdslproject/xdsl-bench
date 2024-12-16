MAKEFLAGS += --warn-undefined-variables
SHELL := bash

.PHONY: install
install: .venv xdsl/.venv

.venv:
	uv sync

xdsl/.venv:
	cd xdsl && VENV_EXTRAS="--extra dev" make venv

.PHONY: asv
asv: .venv xdsl/.venv
	uv run asv run \
		-E existing:./xdsl/.venv/bin/python3

.PHONY: site
site:
	uv run asv publish

.PHONY: preview
preview: site
	uv run asv preview
