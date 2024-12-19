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

profiles/lexer__apply_pdl_extra_file__lex_only.prof: profiles
	uv run python benchmarks/lexer.py

profiles/lexer__apply_pdl_extra_file__lex_only.json: profiles
	uv run python benchmarks/lexer.py

.PHONY: viztracer_lexer
viztracer_lexer: profiles/lexer__apply_pdl_extra_file__lex_only.json
	uv run vizviewer profiles/lexer__apply_pdl_extra_file__lex_only.json

.PHONY: snakeviz_lexer
snakeviz_lexer: profiles/lexer__apply_pdl_extra_file__lex_only.prof
	uv run snakeviz profiles/lexer__apply_pdl_extra_file.prof

.PHONY: viztracer
viztracer_end_to_end: .venv xdsl/.venv profiles
	uv run viztracer -o profiles/empty_program.json \
		xdsl-opt xdsl/tests/xdsl_opt/empty_program.mlir
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
