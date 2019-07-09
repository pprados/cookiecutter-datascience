#!/usr/bin/env make

SHELL=/bin/bash
.SHELLFLAGS = -e -c
.ONESHELL:

# Use NPROC=n
.NOTPARALLEL:
export NPROC?=$(shell nproc)
ifeq ($(shell test $(NPROC) -gt 1; echo $$?),0)
#export MAKE_PARALLEL?=-j $(NPROC)
# C'est pour lancer les tests slow en //
export PYTEST_ARGS?=-n $(NPROC)
export MAKE_PARALLEL?=
#export PYTEST_ARGS?=
else
export MAKE_PARALLEL?=
export PYTEST_ARGS?=
endif

export CONDA_ARGS=--use-index-cache --use-local --offline
export BRANCH=$(shell git rev-parse --abbrev-ref HEAD)

ifeq ($(OS),Windows_NT)
    OS := Windows
else
    OS := $(shell sh -c 'uname 2>/dev/null || echo Unknown')
endif

ifneq ($(TERM),)
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
ACTIVATE_VENV=source $(CONDA_BASE)/etc/profile.d/conda.sh && conda activate $(VENV)
DEACTIVATE_VENV=source $(CONDA_BASE)/etc/profile.d/conda.sh && conda deactivate

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

.PHONY: dump-*
dump-%:
	@if [ "${${*}}" = "" ]; then
		echo "Environment variable $* is not set";
		exit 1;
	else
		echo "$*=${${*}}";
	fi

.git:
	@git init -q

.git/hooks/pre-push: | .git
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
ACTIVATE_VENV=source $(CONDA_BASE)/etc/profile.d/conda.sh && conda activate $(VENV)
DEACTIVATE_VENV=source $(CONDA_BASE)/etc/profile.d/conda.sh && conda deactivate

VALIDATE_VENV=$(CHECK_VENV)
#VALIDATE_VENV=$(ACTIVATE_VENV)

# Toutes les dépendances du projet à regrouper ici
.PHONY: requirements
REQUIREMENTS=$(PIP_PACKAGE)
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
	conda env remove --name "$(VENV)" -y  2>/dev/null
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
	find . -type f -name ".make-*" -delete

.PHONY: clean-all
## Clean all environments
clean-all: clean remove-venv

.PHONY: test
.make-test: $(REQUIREMENTS) tests/*.py Makefile-TU
ifeq ($(OFFLINE),True)
	@python -m pytest -s tests $(PYTEST_ARGS) -m "not online"
else
	@python -m pytest -s tests $(PYTEST_ARGS)
endif
	@date >.make-test
## Run all tests
test: .make-test

# Create a default generated Makefile for GIT
Makefile.snippet: $(REQUIREMENTS)
	cookiecutter -f -o try --no-input .
	cp try/$(BRANCH)/bda_project/Makefile Makefile.snippet
	git add Makefile.snippet

.PHONY: try
try/$(BRANCH):
	mkdir -p try/$(BRANCH)

try_jupyter: $(REQUIREMENTS) try/$(BRANCH)
	$(VALIDATE_VENV)
	python tests/try_cookiecutter.py --output_dir try/$(BRANCH) use_jupyter=y
	ln -f Makefile-TU try/$(BRANCH)/bda_project/Makefile-TU

try_text_processing: $(REQUIREMENTS) try/$(BRANCH)
	$(VALIDATE_VENV)
	python tests/try_cookiecutter.py --output_dir try/$(BRANCH) use_text_processing=y
	ln -f Makefile-TU try/$(BRANCH)/bda_project/Makefile-TU

try_DVC: $(REQUIREMENTS) try/$(BRANCH)
	$(VALIDATE_VENV)
	python tests/try_cookiecutter.py --output_dir try/$(BRANCH) use_DVC=y
	ln -f Makefile-TU try/$(BRANCH)/bda_project/Makefile-TU

try_aws: $(REQUIREMENTS) try/$(BRANCH)
	$(VALIDATE_VENV)
	python tests/try_cookiecutter.py --output_dir try/$(BRANCH) use_aws=y use_s3=y
	ln -f Makefile-TU try/$(BRANCH)/bda_project/Makefile-TU

try_opensource: $(REQUIREMENTS) try/$(BRANCH)
	$(VALIDATE_VENV)
	python tests/try_cookiecutter.py --output_dir try/$(BRANCH) open_source_software=y
	ln -f Makefile-TU try/$(BRANCH)/bda_project/Makefile-TU

try_default: $(REQUIREMENTS) try/$(BRANCH)
	$(VALIDATE_VENV)
	python tests/try_cookiecutter.py --output_dir try/$(BRANCH)
	ln -f Makefile-TU try/$(BRANCH)/bda_project/Makefile-TU

try: $(REQUIREMENTS) try/$(BRANCH)
	$(VALIDATE_VENV)
	# PPR DVC=n
	python tests/try_cookiecutter.py --output_dir try/$(BRANCH) use_DVC=n use_text_processing=y use_aws=y use_s3=y open_source_software=y
	ln -f Makefile-TU try/$(BRANCH)/bda_project/Makefile-TU

_make-%:
	$(MAKE) try
	@pushd tmp/bda_project
	@source $(CONDA_BASE)/bin/activate bda_project
	@$(MAKE) $(*:_make-%=%)
	popd

# Check all version of documentations
.make-check-docs: {{\ cookiecutter.project_slug\ }}/Makefile {{\ cookiecutter.project_slug\ }}/docs
	$(MAKE) try
	@source $(CONDA_BASE)/etc/profile.d/conda.sh && conda activate bda_project
	@pushd tmp/bda_project
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
	@$(MAKE) build/linkcheck
	@$(MAKE) build/man
	@$(MAKE) build/pickle
	@$(MAKE) build/pseudoxml
	@$(MAKE) build/qthelp
	@$(MAKE) build/singlehtml
	@$(MAKE) build/text
	@$(MAKE) build/texinfo
	@$(MAKE) build/xml
	popd
	@date >.make-check-docs

.PHONY: check-docs
check-docs: .make-check-docs

# Il faut probablement lancer des builds avants, pour remetre l'état valide
.make-check-makefile: Makefile-TU {{\ cookiecutter.project_slug\ }}/Makefile
	@$(MAKE) try
	pushd try/$(BRANCH)/bda_project
	export VENV=$(BRANCH)
	source $(CONDA_BASE)/etc/profile.d/conda.sh && conda activate $$VENV
	# Check double make validate
	make clean-build
	make validate
	LANG="en_US.UTF-8" make validate | grep 'Nothing' || ( echo "Error in double make validate" ; exit -1 )
	$(DEACTIVATE_VENV)
	popd
	@date >.make-check-makefile
.PHONY: check-makefile
## Check all generated rules
check-makefile: .make-check-makefile

## Check empty configure
.make-check-configure:
	@conda env remove -n $(BRANCH) 2>/dev/null
	pushd try/$(BRANCH)/bda_project
	export VENV=$(BRANCH)
	$(MAKE) configure
	popd
	@date >.make-check-configure

.PHONY: check-configure
check-configure: .make-check-configure

# PPR .make-check-all-make: $(REQUIREMENTS) .make-check-configure .make-check-makefile .make-check-docs
.make-check-all-make: $(REQUIREMENTS) .make-test .make-check-makefile
	@date >.make-check-all-make

.PHONY: check-all-make
## Try all major make target
check-all-make: .make-check-all-make

.PHONY: validate
.make-validate: Makefile Makefile.snippet .make-test .make-check-all-make
	@date >.make-validate
## Validate all before commit
validate: .make-validate

~/.mypypi: try
	pip download setuptools_scm --dest ~/.mypypi
	cd try/$(BRANCH)/bda_project
	make offline
offline: ~/.mypypi

.PHONY: clean-test
clean-test:
	rm -Rf /tmp/CC_temp* /tmp/make-* /tmp/ssh-ec2-* /tmp/tmp*.sh /tmp/temp*.sh /tmp/ssh-ec2* \
	~/.local/share/jupyter/kernels/cc_temp* $(CONDA_BASE)/envs/CC_*


# ---- Generate differents forms of samples
# $1 mode (normal, dvc, ...)
# $2 project_name
# $3 flags
define generate_example
	mkdir -p examples/$1
	python tests/try_cookiecutter.py --output_dir examples/$1 \
		project_Name=$2 \
		project_slug=$2 \
		$3
	rm -Rf examples/$1/$2/$2/
	cp -Rf \
		examples.template/$2/$2 \
		examples.template/$2/tests \
		examples.template/$2/Project_$1.mak \
		examples/$1/$2/
	sed -i '1,/^#####*$$/!d' examples/$1/$2/Makefile
	sed -i 's/^#####*$$/rexamples.template/$2/Project_$1.mak/' examples/$1/$2/Makefile
	sed -i '/^requirements: .*$$/rexamples.template/$2/setup.inc' examples/$1/$2/setup.py
	cp examples.template/flower_classifier/flower_photos.tgz examples/$1/$2/data/raw
endef

examples.template/flower_classifier/flower_photos.tgz:
	wget -P examples.template/flower_classifier/ 'http://download.tensorflow.org/example_images/flower_photos.tgz'

# PPR gérer les dépendences
examples/normal/flower_classifier: Makefile examples.template/flower_classifier/flower_photos.tgz
	$(call generate_example,normal,flower_classifier,use_DVC=n use_tensorflow=y use_aws=y)
	cp examples.template/flower_classifier/flower_photos.tgz examples/normal/flower_classifier/data/raw

examples/dvc/flower_classifier: Makefile examples.template/flower_classifier/flower_photos.tgz
	$(call generate_example,dvc,flower_classifier,use_DVC=y use_tensorflow=y use_aws=y)
	cp examples.template/flower_classifier/flower_photos.tgz examples/dvc/flower_classifier/data/raw

.PHONY: examples
examples: examples/normal/flower_classifier examples/dvc/flower_classifier