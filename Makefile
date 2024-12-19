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

.PHONY: html
html:
	uv run asv publish

.PHONY: preview
preview: html
	uv run asv preview

# ======== #
# cProfile #
# ======== #

profiles:
	mkdir -p profiles

.PHONY: snakeviz
snakeviz: .venv xdsl/.venv profiles
	uv run python benchmarks/lexer.py
	uv run snakeviz profiles/lexer__apply_pdl_extra_file.prof

.PHONY: viztracer
viztracer: .venv xdsl/.venv profiles
	uv run viztracer \
		-o profiles/empty_program.json \
		xdsl/xdsl/tools/xdsl_opt.py \
		xdsl/tests/xdsl_opt/empty_program.mlir
		--output-file profiles/empty_program.json
	uv run vizviewer profiles/empty_program.json

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
