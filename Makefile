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

.git/hooks/pre-push:
	@cat >>.git/hooks/pre-push <<PRE-PUSH
	#!/usr/bin/env sh
	# Validate the project before a push
	remote="$$1"
	url="$$2"
	branch="$$(git branch | grep \* | cut -d ' ' -f2)"
	echo "REMOTE=$$remote"
	echo "URL=$$url"
	if test -t 1; then
		ncolors=$$(tput colors)
		if test -n "\$$ncolors" && test \$$ncolors -ge 8; then
			normal="\$$(tput sgr0)"
			red="\$$(tput setaf 1)"
	        green="\$$(tput setaf 2)"
			yellow="\$$(tput setaf 3)"
		fi
	fi
	if [ "\$$branch" == "master" ] && [ "\$${FORCE}" != y ] ; then
		printf "\$${green}Validate the project before push the commit... (\$${yellow}make validate\$${green})\$${normal}\n"
		make validate
		ERR=\$$?
		if [ \$${ERR} -ne 0 ] ; then
			printf "\$${red}'\$${yellow}make validate\$${red}' failed before git push.\$${normal}\n"
			printf "Use \$${yellow}FORCE=y git push\$${normal} to force.\n"
			exit \$${ERR}
		fi
	fi
	PRE-PUSH
	chmod +x .git/hooks/pre-push

# Initialiser la configuration de Git
.gitattributes: | .git .git/hooks/pre-push # Configure git
	@git config --local core.autocrlf input
	# Set tabulation to 4 when use 'git diff'
	@git config --local core.page 'less -x4'

CHECK_VENV=@if [[ "base" == "$(CONDA_DEFAULT_ENV)" ]] || [[ -z "$(CONDA_DEFAULT_ENV)" ]] ; \
  then ( echo -e "$(green)Use: $(cyan)conda activate $(VENV)$(green) before using 'make'$(normal)"; exit 1 ) ; fi
CONDA_BASE:=$(shell conda info --base)
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

.PHONY: clean_check-makefile
clean_check-makefile:
	rm -Rf /tmp/CC_*
	rm -Rf $(CONDA_BASE)/envs/CC_*

.PHONY: clean
clean: clean-pyc

.PHONY: clean-all
## Clean all environments
clean-all: clean remove-venv

.PHONY: test
.make-test: $(REQUIREMENTS) tests/*
	$(VALIDATE_VENV)
	python -m pytest -s tests
	touch .make-test
## Run all tests
test: .make-test

# Create a default generated Makefile for GIT
Makefile.snippet: {{\ cookiecutter.project_slug\ }} $(REQUIREMENTS)
	cookiecutter -f -o ~/workspace.bda/cookiecutter-bda/tmp --no-input .
	cp tmp/bda_project/Makefile Makefile.snippet
	git add Makefile.snippet

# Install a default sample in ./tmp/bda_project
try: $(REQUIREMENTS)
	$(VALIDATE_VENV)
	cookiecutter -f -o tmp --no-input .
	ln -f Makefile-TU tmp/bda_project/Makefile-TU

_make-%: try
	@cd tmp/bda_project
	@source $(CONDA_BASE)/bin/activate bda_project
	@$(MAKE) $(*:_make-%=%)

# Check all version of documentations
.make-check-docs: try {{\ cookiecutter.project_slug\ }}/Makefile {{\ cookiecutter.project_slug\ }}/docs
	@cd tmp/bda_project
	source $(CONDA_BASE)/bin/activate bda_project
#@$(MAKE) build/applehelp # https://github.com/miyakogi/m2r/issues/34
	@$(MAKE) build/changes
	@$(MAKE) build/devhelp
	@$(MAKE) build/dirhtml
	@$(MAKE) build/dummy
#@$(MAKE) build/epub # Error with KeyErro 'ids' in _epub_base.py
	@$(MAKE) build/gettext
	@$(MAKE) build/html
	@$(MAKE) build/htmlhelp
	@$(MAKE) build/json
	@$(MAKE) build/latex
#@$(MAKE) build/linkcheck
	@$(MAKE) build/man
	@$(MAKE) build/pickle
	@$(MAKE) build/pseudoxml
	@$(MAKE) build/qthelp
	@$(MAKE) build/singlehtml
	@$(MAKE) build/text
	@$(MAKE) build/texinfo
	@$(MAKE) build/xml
	touch .make-check-docs

check-docs: .make-check-docs

# PPR: verifier en code clean total du projet bda_project.
# Il faut probablement lancer des builds avants, pour remetre l'état valide
## Check all generated rules
OPT=-j -O
check-makefile: clean_check-makefile try Makefile-TU {{\ cookiecutter.project_slug\ }}/Makefile
	@pushd tmp/bda_project
	source $(CONDA_BASE)/bin/activate bda_project
	# Check double make validate
	make clean-build
	make validate
	LANG="en_US.UTF-8" make validate | grep 'Nothing' || ( echo "Error in double make validate" ; exit -1 )
	source $(CONDA_BASE)/bin/deactivate
	popd

	make $(OPT) -f Makefile-TU DEFAULT DOCS
	[ '"y"' = $$(jq '.["open_source_software"]' cookiecutter.json) ] && make $(OPT) -f Makefile-TU OPENSOURCE
	[ '"y"' = $$(jq '.["use_jupyter"]' cookiecutter.json) ] && make $(OPT) -f Makefile-TU JUPYTER

## Check empty configure
check-configure:
	conda env remove -n bda_project
	cd tmp/bda_project
	$(MAKE) configure

# PPR .make-check-all-make: check-configure check-makefile check-docs
.make-check-all-make: check-configure check-makefile
	touch .make-check-all-make
## Try all major make target
check-all-make: .make-check-all-make

## Validate all before commit
validate: try Makefile.snippet test check-all-make
