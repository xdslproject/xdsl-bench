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

# ======== #
# cProfile #
# ======== #

## Generate profile data from benchmarks
profiles:
	mkdir -p profiles

.PHONY: clean-profiles
clean-profiles:
	rm -rf profiles

profiles/lexer__apply_pdl_extra_file__lex_only.prof: .venv xdsl/.venv profiles
	uv run python benchmarks/lexer.py

profiles/lexer__apply_pdl_extra_file__lex_only.json: .venv xdsl/.venv profiles
	uv run python benchmarks/lexer.py

profiles/end_to_end__constant_folding.prof: .venv xdsl/.venv profiles
	uv run python benchmarks/end_to_end.py

profiles/end_to_end__constant_folding.json: .venv xdsl/.venv profiles
	uv run python benchmarks/end_to_end.py

## Visualise profile data from benchmarks
.PHONY: viztracer_lexer
viztracer_lexer: profiles/lexer__apply_pdl_extra_file__lex_only.json
	uv run vizviewer profiles/lexer__apply_pdl_extra_file__lex_only.json

.PHONY: snakeviz_lexer
snakeviz_lexer: profiles/lexer__apply_pdl_extra_file__lex_only.prof
	uv run snakeviz profiles/lexer__apply_pdl_extra_file.prof

.PHONY: flameprof_lexer
flameprof_lexer: profiles/lexer__apply_pdl_extra_file__lex_only.prof
	uv run flameprof profiles/lexer__apply_pdl_extra_file__lex_only.prof \
		> profiles/lexer__apply_pdl_extra_file__lex_only.svg

.PHONY: viztracer_end_to_end
viztracer_end_to_end: profiles/end_to_end__constant_folding.json
	uv run vizviewer profiles/end_to_end__constant_folding.json

.PHONY: snakeviz_end_to_end
snakeviz_end_to_end: profiles/end_to_end__constant_folding.prof
	uv run snakeviz profiles/end_to_end__constant_folding.prof

## Profile command line directly
.PHONY: viztracer
viztracer_xdsl_opt: .venv xdsl/.venv profiles
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
