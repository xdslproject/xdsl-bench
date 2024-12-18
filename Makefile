# Best practices for makefiles
MAKEFLAGS += --warn-undefined-variables
SHELL := bash

# Allow overriding which extras are installed (defaults to none)
VENV_EXTRAS ?=

# ============ #
# Installation #
# ============ #

.PHONY: install
install: .venv xdsl/.venv

.venv:
	uv sync ${VENV_EXTRAS}

xdsl/.venv:
	cd xdsl && VENV_EXTRAS="" make venv

# ===== #
#  ASV  #
# ===== #

.PHONY: asv
asv: .venv xdsl/.venv
	uv run asv run --show-stderr

.PHONY: html
html:
	uv run asv publish

.PHONY: preview
preview: html
	uv run asv preview

# ======== #
# cProfile #
# ======== #

.PHONY: bench_lexer
bench_lexer: .venv xdsl/.venv
	uv run python benchmarks/lexer.py
	uv run snakeviz profiles/lexer__apply_pdl_extra_file.prof

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
