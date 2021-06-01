SHELL := /usr/bin/env bash

PYTHON ?= python
VENV_DIR ?= .venv

# .SUFFIXES:
# .SUFFIXES: .yaml .preseed .vagrant .json .iso .ova .box

# .PRECIOUS: .yaml .preseed .vagrant

.PHONY: all
all: build

ACTIVATE = $(VENV_DIR)/bin/activate
.PHONY: requirements
requirements:
	@test -d $(VENV_DIR) || $(PYTHON) -m venv $(VENV_DIR) && \
    source $(ACTIVATE) && \
    pip install --requirement requirements_bare.txt && \
    pip freeze > requirements.txt && \
    rm -rf $(VENV_DIR)
