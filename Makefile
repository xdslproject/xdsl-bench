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
# Profiling #
# ========= #

## Generate profile data from benchmarks
profiles:
	mkdir -p profiles

.PHONY: clean-profiles
clean-profiles:
	rm -rf profiles

.PHONY: timeit_end_to_end
timeit_end_to_end:
	uv run python3 benchmarks/end_to_end.py timeit

.PHONY: snakeviz_end_to_end
snakeviz_end_to_end:
	uv run python3 benchmarks/end_to_end.py -t time_end_to_end_opt__constant_folding snakeviz

.PHONY: flameprof_end_to_end
flameprof_end_to_end:
	uv run python3 benchmarks/end_to_end.py -t time_end_to_end_opt__constant_folding flameprof

.PHONY: viztracer_end_to_end
viztracer_end_to_end:
	uv run python3 benchmarks/end_to_end.py -t time_end_to_end_opt__constant_folding viztracer

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

.PHONY: types
types:
	uv run mypy src
	uv run mypy benchmarks --scripts-are-modules

.PHONY: check
check: lint format types
