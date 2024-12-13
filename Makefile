.venv:
	uv sync

xdsl/.venv:
	cd xdsl && VENV_EXTRAS="--extra dev" make venv

.PHONY: asv
asv: .venv xdsl/.venv
	.venv/bin/asv run || true
