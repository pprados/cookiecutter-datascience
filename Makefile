#!/usr/bin/env make

SHELL=/bin/bash
.SHELLFLAGS = -e -c
.ONESHELL:
.NOTPARALLEL:

# ---------------------------------------------------------------------------------------
# SNIPPET pour détecter l'OS d'exécution.
ifeq ($(OS),Windows_NT)
    OS := Windows
else
    OS := $(shell sh -c 'uname 2>/dev/null || echo Unknown')
endif

# ---------------------------------------------------------------------------------------
# SNIPPET pour récupérer les séquences de caractères pour les couleurs
# A utiliser avec un
# echo -e "Use '$(cyan)make$(normal)' ..."
# Si vous n'utilisez pas ce snippet, les variables de couleurs non initialisés
# sont simplement ignorées.
ifdef TERM
normal:=$(shell tput sgr0)
bold:=$(shell tput bold)
red:=$(shell tput setaf 1)
green:=$(shell tput setaf 2)
yellow:=$(shell tput setaf 3)
blue:=$(shell tput setaf 4)
purple:=$(shell tput setaf 5)
cyan:=$(shell tput setaf 6)
white:=$(shell tput setaf 7)
gray:=$(shell tput setaf 8)
endif

PRJ:=$(shell basename $(shell pwd))
VENV ?= $(PRJ)
KERNEL ?=$(VENV)
PRJ_PACKAGE:=$(PRJ)$(USE_GPU)
PYTHON_VERSION:=3.6

CONDA_BASE=$(shell conda info --base)
CONDA_PACKAGE:=$(CONDA_PREFIX)/lib/python$(PYTHON_VERSION)/site-packages
CONDA_PYTHON:=$(CONDA_PREFIX)/bin/python
PIP_PACKAGE:=$(CONDA_PACKAGE)/$(PRJ_PACKAGE).egg-link

.PHONY: help
.DEFAULT: help

## Print all majors target
help:
	@echo "$(bold)Available rules:$(normal)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=20 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')

	echo -e "Use '$(cyan)make -jn ...$(normal)' for Parallel run"
	echo -e "Use '$(cyan)make -B ...$(normal)' to force the target"
	echo -e "Use '$(cyan)make -n ...$(normal)' to simulate the build"

.git:
	@git init -q

# Initialiser la configuration de Git
.gitattributes: | .git  # Configure git
	@git config --local core.autocrlf input
	# Set tabulation to 4 when use 'git diff'
	@git config --local core.page 'less -x4'

CHECK_VENV=@if [[ "base" == "$(CONDA_DEFAULT_ENV)" ]] || [[ -z "$(CONDA_DEFAULT_ENV)" ]] ; \
  then ( echo -e "$(green)Use: $(cyan)conda activate $(VENV)$(green) before using 'make'$(normal)"; exit 1 ) ; fi

ACTIVATE_VENV=source $(CONDA_BASE)/bin/activate $(VENV)
DEACTIVATE_VENV=source $(CONDA_BASE)/bin/deactivate $(VENV)

VALIDATE_VENV=$(CHECK_VENV)
#VALIDATE_VENV=$(ACTIVATE_VENV)


# Toutes les dépendances du projet à regrouper ici
.PHONY: requirements
REQUIREMENTS=$(PIP_PACKAGE) \
		.gitattributes
requirements: $(REQUIREMENTS)

# Règle de vérification de la bonne installation de la version de python dans l'environnement Conda
$(CONDA_PYTHON):
	$(VALIDATE_VENV)
	conda install "python=$(PYTHON_VERSION).*" -y -q

# Règle de mise à jour de l'environnement actif à partir
# des dépendances décrites dans `setup.py`
$(PIP_PACKAGE): $(CONDA_PYTHON) setup.py | .git # Install pip dependencies
	$(VALIDATE_VENV)
	pip install $(EXTRA_INDEX) -e '.[tests]' | grep -v 'already satisfied' || true
	@touch $(PIP_PACKAGE)

# ---------------------------------------------------------------------------------------
.PHONY: configure
## Prepare the environment (conda venv, kernel, ...)
configure:
	@conda create --name "$(VENV)" python=$(PYTHON_VERSION) -y
	@if [[ "base" == "$(CONDA_DEFAULT_ENV)" ]] || [[ -z "$(CONDA_DEFAULT_ENV)" ]] ; \
	then echo -e "Use: $(cyan)conda activate $(VENV)$(normal)" ; fi

# ---------------------------------------------------------------------------------------
.PHONY: remove-venv
remove-venv remove-$(VENV):
	@$(DEACTIVATE_VENV)
	conda env remove --name "$(VENV)" -y
	echo -e "Use: $(cyan)conda deactivate$(normal)"
# Remove venv
remove-venv : remove-$(VENV)

# ---------------------------------------------------------------------------------------
.PHONY: clean-pyc
clean-pyc: # Clean pre-compiled files
	-/usr/bin/find . -type f -name "*.py[co]" -delete
	-/usr/bin/find . -type d -name "__pycache__" -delete

.PHONY: clean-pip
## Remove all the pip package
clean-pip:
	$(VALIDATE_VENV)
	pip freeze | grep -v "^-e" | xargs pip uninstall -y

.PHONY: clean-venv
clean-venv clean-$(VENV): remove-venv
	@echo -e "$(cyan)Re-create virtualenv $(VENV)...$(normal)"
	conda create -y -q -n $(VENV)
	touch setup.py
	echo -e "$(yellow)Warning: Conda virtualenv $(VENV) is empty.$(normal)"
.PHONY: clean
clean: clean-pyc

.PHONY: clean-all
## Clean all environments
clean-all: clean remove-venv

.PHONY: test
## Run all tests
test: $(REQUIREMENTS)
	$(VALIDATE_VENV)
	python -m pytest -s tests

# Create a default generated Makefile for GIT
Makefile.snippet: {{\ cookiecutter.project_slug\ }} $(REQUIREMENTS)
	cookiecutter -f -o ~/workspace.bda/cookiecutter-bda/tmp --no-input .
	cp tmp/bdaproject/Makefile Makefile.snippet
	git add Makefile.snippet

# Install a default sample in ./tmp/bda_project
try: $(REQUIREMENTS)
	cookiecutter -f -o tmp --no-input .
	cp Makefile-TU tmp/bda_project

_make-%: try
	@cd tmp/bda_project
	@source $(CONDA_BASE)/bin/activate bda_project
	@make $(*:_make-%=%)

# Check all version of documentations
check-docs: try
	@cd tmp/bdaproject
	@source $(CONDA_BASE)/bin/activate bdaproject
	#@make build/applehelp # https://github.com/miyakogi/m2r/issues/34
	@make build/changes
	@make build/devhelp
	@make build/dirhtml
	@make build/dummy
	@make build/epub # Error with KeyErro 'ids' in _epub_base.py
	@make build/gettext
	@make build/html
	@make build/htmlhelp
	@make build/json
	@make build/latex
	@make build/linkcheck
	@make build/man
	@make build/pickle
	@make build/pseudoxml
	@make build/qthelp
	@make build/singlehtml
	@make build/text
	@make build/texinfo
	@make build/xml

## Check all generated rules
check-makefile: try
	JOBS="-j 20"
	cd tmp/bda_project
	make $(JOBS) -f Makefile-TU DEFAULT
	#[ '"y"' = $$(jq '.["open_source_software"]' ../../cookiecutter.json) ] && make $(JOBS) -f Makefile-TU OPENSOURCE
	#[ '"y"' = $$(jq '.["use_jupyter"]' ../../cookiecutter.json) ] && make $(JOBS) -f Makefile-TU JUPYTER

## Check empty configure
check-configure:
	conda env remove -n bda_project
	cd tmp/bda_project
	make configure

## Try all major make target
check-all-make: check-configure check-makefile check-docs

## Validate all before commit
validate: Makefile.snippet test check-all-make