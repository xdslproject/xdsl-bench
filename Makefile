.venv:
	uv sync

xdsl/.venv:
	cd xdsl && VENV_EXTRAS="--extra dev" make venv

.PHONY: asv-machine
asv-machine:
	.venv/bin/asv machine --yes

.PHONY: asv
asv: .venv xdsl/.venv
	.venv/bin/asv run || true
