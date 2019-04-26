#!/usr/bin/env make

SHELL=/bin/bash
.SHELLFLAGS = -e -c
.ONESHELL:

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
	echo -e "Use: $(cyan)conda activate $(VENV)$(normal)"


# ---------------------------------------------------------------------------------------
.PHONY: remove-venv
remove-venv remove-$(VENV):
	@$(DEACTIVATE_VENV)
	conda env remove --name "$(VENV)" -y
	echo -e "Use: $(cyan)conda deactivate$(normal)"
## Remove venv
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

# Hack pour contourner l'impossibilité d'ajouter les paramètres Jinja trim_blocks et lstrip_blocks
# à Cookiecutter. J'applique alors des transformations à partir de Makefile.template
# Avant l'ajout à Git.
{{\ cookiecutter.project_slug\ }}/Makefile : Makefile.template
	sed -e ':a' -e 'N' -e '$$!ba' -e 's/%} *\n/%}/g' Makefile.template >{{\ cookiecutter.project_slug\ }}/Makefile
	sed -i -e ':a' -e 'N' -e '$$!ba' -e 's/\n\n *{%/{%/g' {{\ cookiecutter.project_slug\ }}/Makefile


.PHONY: test
## Run all tests
test: $(REQUIREMENTS) {{\ cookiecutter.project_slug\ }}/Makefile
	$(VALIDATE_VENV)
	python -m unittest discover -s tests -b

try: {{\ cookiecutter.project_slug\ }}/Makefile
	cookiecutter -f -o ~/workspace.bda/cookiecutter-bda/tmp --no-input .
