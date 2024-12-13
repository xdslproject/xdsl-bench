.venv:
	uv sync

xdsl/.venv:
	cd xdsl && make venv

.PHONY: xdsl-local
xdsl-local: xdsl/.venv
	cd xdsl && .venv/bin/asv run

.PHONY: xdsl-submodule
xdsl-submodule: .venv xdsl/.venv
	.venv/bin/asv run
