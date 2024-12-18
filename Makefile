MAKEFLAGS += --warn-undefined-variables
SHELL := bash

# ============ #
# Installation #
# ============ #

.PHONY: install
install: .venv xdsl/.venv

.venv:
	uv sync

xdsl/.venv:
	cd xdsl && VENV_EXTRAS="--extra dev" make venv

# ===== #
#  ASV  #
# ===== #

.PHONY: asv
asv: .venv xdsl/.venv
	uv run asv run

.PHONY: html
html:
	uv run asv publish

.PHONY: preview
preview: html
	uv run asv preview

# ======== #
# cProfile #
# ======== #

.PHONY: bench
bench: .venv xdsl/.venv
	cd xdsl && uv run python3 ../benchmarks/import_xdsl_opt.py

# ========= #
# Developer #
# ========= #

.PHONY: lint
lint: .venv
	uv run ruff check benchmarks/ --fix --show-fixes --exit-non-zero-on-fix

.PHONY: format
format:
	uv run ruff format benchmarks/

.PHONY: type
types:
	uv run mypy benchmarks --scripts-are-modules

.PHONY: check
check: lint format type
