# Best practices for makefiles
MAKEFLAGS += --warn-undefined-variables
SHELL := bash

# Allow overriding which extras are installed (defaults to none)
VENV_ARGS ?=

# ============ #
# Installation #
# ============ #

.PHONY: install
install: .venv xdsl/.venv

.venv:
	uv sync ${VENV_ARGS}

xdsl/.venv:
	cd xdsl && VENV_EXTRAS="" make venv

# ===== #
#  ASV  #
# ===== #

.PHONY: asv
asv: .venv xdsl/.venv
	uv run asv run --show-stderr

.PHONY: history
history: .venv xdsl/.venv
	uv run asv run main~5..main

.PHONY: html
html:
	uv run asv publish

.PHONY: preview
preview: html
	uv run asv preview

.PHONY: clean-local-asv
clean-local-asv: .asv
	rm -rf .asv/html .asv/results/$(shell hostname)

.PHONY: clean-asv
clean-asv: clean-local-asv
	rm -rf .asv/results/github-action

# ========= #
# Developer #
# ========= #

.PHONY: lint
lint: .venv
	uv run ruff check benchmarks/ --fix --show-fixes --exit-non-zero-on-fix

.PHONY: format
format:
	uv run ruff format benchmarks/

.PHONY: types
types:
	uv run mypy src
	uv run mypy benchmarks --scripts-are-modules

.PHONY: check
check: lint format types
