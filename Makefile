# Best practices for makefiles
MAKEFLAGS += --warn-undefined-variables
SHELL := bash

xdsl/.venv:
	VENV_OPTIONS="--extra bench" $(MAKE) -C xdsl .venv

.PHONY: asv
asv: xdsl/.venv
	$(MAKE) -C xdsl asv

.PHONY: asv-html
asv-html: xdsl/.venv
	$(MAKE) -C xdsl asv-html

.PHONY: asv-preview
asv-preview: xdsl/.venv
	$(MAKE) -C xdsl asv-preview

.PHONY: asv-clean
asv-clean: xdsl/.venv
	$(MAKE) -C xdsl asv-clean
