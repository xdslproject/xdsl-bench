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
	uv run asv run

.PHONY: html
html:
	uv run asv publish

.PHONY: preview
preview: html
	uv run asv preview
