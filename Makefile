.PHONY: xdsl
xdsl:
	cd xdsl && .venv/bin/asv run

.PHONY: xdsl-asv
xdsl-asv:
	.venv/bin/asv run
