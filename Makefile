.venv:
	uv sync

xdsl/.venv:
	cd xdsl && VENV_EXTRAS="--extra dev" make venv

.PHONY: xdsl-local
xdsl-local: xdsl/.venv
	cd xdsl && .venv/bin/asv run

.PHONY: xdsl-submodule
xdsl-submodule: .venv xdsl/.venv
	.venv/bin/asv run
