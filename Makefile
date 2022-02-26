SHELL := /usr/bin/env bash

PYTHON ?= python
VENV ?= .venv

GENERATED_FILES =

.SUFFIXES:
.SUFFIXES: .py
.PRECIOUS: .py

.PHONY: all
all: venv

ACTIVATE_SCRIPT = $(VENV)/bin/activate
.PHONY: venv
venv: $(ACTIVATE_SCRIPT)
$(ACTIVATE_SCRIPT): requirements.txt
	@test -d $(VENV) || $(PYTHON) -m venv $(VENV) && \
  source $(ACTIVATE_SCRIPT) && \
  pip install --upgrade pip setuptools && \
  pip install --requirement $< && \
  touch $(ACTIVATE_SCRIPT)

.PHONY: venv_upgrade
venv_upgrade:
	@rm -rf $(VENV) && \
  $(PYTHON) -m venv $(VENV) && \
  source $(ACTIVATE_SCRIPT) && \
  pip install --upgrade pip setuptools && \
  pip install --requirement requirements_bare.txt && \
  pip freeze > requirements.txt && \
  touch $(ACTIVATE_SCRIPT)

# moo:
#   @source $(ACTIVATE_SCRIPT) && \
#   ./moo.py > $@

.PHONY: clean
clean:
	@rm -rf $(GENERATED_FILES)

.PHONY: reallyclean
reallyclean: clean
	@rm -rf $(VENV)
