#!/usr/bin/env make
{% if cookiecutter.add_makefile_comments == 'y' %}
# SNIPPET Le shebang précédant permet de creer des alias des cibles du Makefile.
# Il faut que le Makefile soit executable
# 	chmod u+x Makefile
# 	git update-index --chmod=+x Makefile
# Puis, par exemple
# 	ln -s Makefile configure
# 	ln -s Makefile test
# 	ln -s Makefile train
# 	./configure		# Execute make configure
# 	./test 			# Execute make test
#   ./train 		# Train the model
# Attention, il n'est pas possible de passer les paramètres aux scripts
{% endif %}{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour vérifier la version du programme `make`.
{% endif %}# WARNING: Use make >4.0
ifeq ($(shell echo "$(shell echo $(MAKE_VERSION) | sed 's@^[^0-9]*\([0-9]\+\).*@\1@' ) >= 4" | bc -l),0)
$(error Bad make version, please install make >= 4)
endif{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour changer le mode de gestion du Makefile.
# Avec ces trois paramètres, toutes les lignes d'une recette sont invoquées dans le même shell.
# Ainsi, il n'est pas nécessaire d'ajouter des '&&' ou des '\' pour regrouper les lignes.
# Comme Make affiche l'intégralité du block de la recette avant de l'exécuter, il n'est
# pas toujours facile de savoir quel est la ligne en échec.
# Je vous conseille dans ce cas d'ajouter au début de la recette 'set -x'
# Attention : il faut une version > 4 de  `make` (`make -v`).
# Les versions CentOS d'Amazone ont une version 3.82.
# Utilisez `conda install -n $(VENV_AWS) make>=4 -y`{% endif %}
# WARNING: Use make >4.0
SHELL=/bin/bash
.SHELLFLAGS = -e -c
.ONESHELL:

{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour injecter les variables de .env.{% endif %}
ifneq (,$(wildcard .env))
include .env
endif

{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour détecter l'OS d'exécution.{% endif %}
ifeq ($(OS),Windows_NT)
    OS := Windows
    EXE:=.exe
    SUDO?=
else
    OS := $(shell sh -c 'uname 2>/dev/null || echo Unknown')
    EXE:=
    SUDO?=
endif

{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour détecter la présence d'un GPU afin de modifier le nom du projet
# et ses dépendances si nécessaire.{% endif %}
ifndef USE_GPU
ifneq ("$(wildcard /proc/driver/nvidia)","")
USE_GPU:=-gpu
else ifdef CUDA_HOME
USE_GPU:=-gpu
endif
endif

ifdef USE_GPU
CUDA_VER=$(shell nvidia-smi | awk -F"CUDA Version:" 'NR==3{split($$2,a," ");print a[1]}')
endif
{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour identifier le nombre de processeur{% endif %}
NPROC?=$(shell nproc)
{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour pouvoir lancer un browser avec un fichier local{% endif %}
define BROWSER
	python $(PYTHON_ARGS) -c '
	import os, sys, webbrowser
	from urllib.request import pathname2url

	webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])), autoraise=True)
	sys.exit(0)
	'
endef
{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour supprimer le parallelisme pour certaines cibles
# par exemple pour release
ifneq ($(filter configure release clean functional-test% upgrade-%,$(MAKECMDGOALS)),)
.NOTPARALLEL:
endif
#{% endif %}
{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour récupérer les séquences de caractères pour les couleurs
# A utiliser avec un
# echo -e "Use '$(cyan)make$(normal)' ..."
# Si vous n'utilisez pas ce snippet, les variables de couleurs non initialisés
# sont simplement ignorées.{% endif %}
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
{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour gérer le projet, le virtualenv conda{% if cookiecutter.use_jupyter == 'y' %} et le kernel{% endif %}.
# Par convention, les noms du projet, de l'environnement Conda{% if cookiecutter.use_jupyter == 'y' %} ou le Kernel Jupyter{% endif %}
# correspondent au nom du répertoire du projet.
# Il est possible de modifier cela en valorisant les variables VENV,{% if cookiecutter.use_jupyter == 'y' %} KERNEL,{% endif %} et/ou PRJ.
# avant le lancement du Makefile (`VENV=cntk_p36 make`){% endif %}
PRJ:=$(shell basename $(shell pwd))
VENV ?= $(PRJ)
{% if cookiecutter.use_jupyter == 'y' %}KERNEL ?=$(VENV){% endif %}
PRJ_PACKAGE:=$(PRJ)$(USE_GPU)
PYTHON_VERSION:={{ cookiecutter.python_version }}
PYTHON_ARGS:=
PYTHON_SRC=$(shell find -L "$(PRJ)" -type f -iname '*.py' | grep -v __pycache__)
PYTHON_TST=$(shell find -L tests -type f -iname '*.py' | grep -v __pycache__)
{% if cookiecutter.use_aws == 'y' %}S3_BUCKET?=s3://$(subst _,-,$(PRJ))
PROFILE = default{% endif %}
DOCKER_REPOSITORY = $(USER)
# Data directory (can be in other place, in VM or Docker for example)
export DATA?=data
{% if cookiecutter.use_DVC == 'y' %}
# Use DVC bucket.
# TODO: select DVC_BUCKET with make dvc-external-...
# May be :
# DVC_BUCKET?=s3://$(PRJ)
# DVC_BUCKET?=gs://$(PRJ)
# DVC_BUCKET?=ssh://user@example.com:
# DVC_BUCKET?=hdfs://user@example.com
DVC_BUCKET?={% if cookiecutter.use_s3 == 'y' %}$(S3_BUCKET){% else %}~/.dvc{% endif %}
# List of source and tests files
{% if cookiecutter.use_tensorflow == "y" %}TENSORFLOW_LOGDIR?=./logdir{% endif %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour reconstruire tous les chemins importants permettant
# de gérer correctement les dépendances des modules sous Conda.
# Cela sert à gérer automatiquement les environnements.
# Pour que cela fonctionne, il faut avoir un environement Conda actif,
# identifié par la variable CONDA_PREFIX (c'est généralement le cas).{% endif %}
# Conda environment
CONDA_BASE:=$(shell AWS_DEFAULT_PROFILE=default conda info --base)
CONDA_PACKAGE:=$(CONDA_PREFIX)/lib/python$(PYTHON_VERSION)/site-packages
CONDA_PYTHON:=$(CONDA_PREFIX)/bin/python
CONDA_ARGS?=-c conda-forge
export VIRTUAL_ENV=$(CONDA_PREFIX)
{# PIP_INDEX_URL?=https://pypi.org/simple #}
PIP_PACKAGE:=$(CONDA_PACKAGE)/$(PRJ_PACKAGE).egg-link
PIP_ARGS?=
{% if cookiecutter.use_jupyter == 'y' %}# Add lab extensions here
JUPYTER_LABEXTENSIONS?=
JUPYTER_DATA_DIR:=$(shell jupyter --data-dir 2>/dev/null || echo "~/.local/share/jupyter")
JUPYTER_LABEXTENSIONS_DIR:=$(CONDA_PREFIX)/share/jupyter/labextensions
_JUPYTER_LABEXTENSIONS:=$(foreach ext,$(JUPYTER_LABEXTENSIONS),$(JUPYTER_LABEXTENSIONS_DIR)/$(ext))
{% endif %}
{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour ajouter des repositories complémentaires à PIP.
# A utiliser avec par exemple
# pip $(EXTRA_INDEX) install ...{% endif %}
EXTRA_INDEX:=--extra-index-url=https://pypi.anaconda.org/octo
{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour gérer permettre d'invoquer une cible make avec des paramètres.
# Pour cela, toutes les cibles inconnues, sont considérées comme des paramètres
# et se retrouvent dans la variables ARGS. Pour que ces cibles ne génères pas d'erreurs
# on ajoute une règle pour ignorer toutes les cibles inconnes.
# Cela est en commentaire et doit être activé spécifiquement.{% endif %}
# Calculate the make extended parameter
# Keep only the unknown target
#ARGS = `ARGS="$(filter-out $@,$(MAKECMDGOALS))" && echo $${ARGS:-${1}}`
# Hack to ignore unknown target. May be used to calculate parameters
#%:
#	@:
{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour gérer automatiquement l'aide du Makefile.
# Il faut utiliser des commentaires commençant par '##' précédant la ligne des recettes,
# pour une production automatique de l'aide.{% endif %}
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
{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour affichier la valeur d'une variable d'environnement
# tel quelle est vue par le Makefile. Par exemple `make dump-CONDA_PACKAGE`{% endif %}
.PHONY: dump-*
dump-%:
	@if [ "${${*}}" = "" ]; then
		echo "Environment variable $* is not set";
		exit 1;
	else
		echo "$*=${${*}}";
	fi
{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour invoker un shell dans le context du Makefile{% endif %}
.PHONY: shell
## Run shell in Makefile context
shell:
	$(SHELL)

{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour gérer les Notebooks avec GIT.
# Les recettes suivantes s'assure que git est bien initialisé
# et ajoute des recettes {% if cookiecutter.use_jupyter == 'y' %}pour les fichiers *.ipynb
# et eventuellement {% endif %}pour les fichiers *.csv.
#
# Pour cela, un fichier .gitattribute est maintenu à jour.
{% if cookiecutter.use_jupyter == 'y' %}# Les recettes pour les notebooks se chargent de les nettoyer avant de les commiter.
# Pour cela, elles appliquent `jupyter nb-convert` à la volée. Ainsi, les comparaisons
# de version ne sont plus parasités par les data.
#{% endif %}
# Les scripts pour les CSV utilisent le composant `daff` (pip install daff)
# pour comparer plus efficacement les évolutions des fichiers csv.
# Un `git diff toto.csv` est plus clair.

# S'assure de la présence de git (util en cas de synchronisation sur le cloud par exemple,
# après avoir exclus le répertoire .git (cf. ssh-ec2){% endif %}
.git:
	@if [[ ! -d .git ]]; then
		@git init -q
		git commit --allow-empty -m "Create project $(PRJ)"
	fi
{% if cookiecutter.use_jupyter == 'y' %}{% if cookiecutter.add_makefile_comments == 'y' %}
# Règle technique importante, invoquées lors du `git commit` d'un fichier *.ipynb via
# le paramètrage de `.gitattributes`.{% endif %}
.PHONY: pipe_clear_jupyter_output
pipe_clear_jupyter_output:
	jupyter nb-convert --to notebook --ClearOutputPreprocessor.enabled=True <(cat <&0) --stdout 2>/dev/null{% endif %}
{% if cookiecutter.use_git_LFS == 'y' %}{% if cookiecutter.use_DVC != 'y' %}{% if cookiecutter.add_makefile_comments == 'y' %}
# Règle qit install git lfs si nécessaire{% endif %}
.git/hooks/post-checkout:
ifeq ($(shell which git-lfs >/dev/null ; echo "$$?"),0)
	# Add git lfs if possible
	@git lfs install >/dev/null
	# Add some extensions in lfs
	@git lfs track "*.pkl" --lockable  >/dev/null
	@git lfs track "*.bin" --lockable  >/dev/null
	@git lfs track "*.jpg" --lockable  >/dev/null
	@git lfs track "*.jpeg" --lockable >/dev/null
	@git lfs track "*.gif" --lockable  >/dev/null
	@git lfs track "*.png" --lockable  >/dev/null
endif{% endif %}{% endif %}
{% if cookiecutter.add_makefile_comments == 'y' %}
# Règle qui ajoute la validation du project avant un push sur la branche master.
# Elle ajoute un hook git pour invoquer `make validate` avant de pusher. En cas
# d'erreur, le push n'est pas possible.
# Pour forcer le push, malgres des erreurs lors de l'exécution de 'make validate'
# utilisez 'FORCE=y git push'.
# Pour supprimer ce comportement, il faut modifier le fichier .git/hooks/pre-push
# et supprimer la règle du Makefile, ou bien,
# utiliser un fichier vide 'echo ''> .git/hooks/pre-push'{% endif %}
.git/hooks/pre-push:{% if cookiecutter.use_git_LFS == 'y' %}{% if cookiecutter.use_DVC != 'y' %}.git/hooks/post-checkout{% endif %}{% endif %} | .git
	@# Add a hook to validate the project before a git push
	cat >>.git/hooks/pre-push <<PRE-PUSH
	#!/usr/bin/env sh
	# Validate the project before a push
	if test -t 1; then
		ncolors=$$(tput colors)
		if test -n "\$$ncolors" && test \$$ncolors -ge 8; then
			normal="\$$(tput sgr0)"
			red="\$$(tput setaf 1)"
	        green="\$$(tput setaf 2)"
			yellow="\$$(tput setaf 3)"
		fi
	fi
	branch="\$$(git branch | grep \* | cut -d ' ' -f2)"
	if [ "\$${branch}" = "master" ] && [ "\$${FORCE}" != y ] ; then
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

# Init git configuration
.gitattribute: | .git .git/hooks/pre-push{% if cookiecutter.use_DVC == 'y' %} .dvc{% endif %}  # Configure git
	@git config --local core.autocrlf input
	# Set tabulation to 4 when use 'git diff'
	@git config --local core.page 'less -x4'

{% if cookiecutter.use_jupyter == 'y' %}ifeq ($(shell which jupyter >/dev/null ; echo "$$?"),0)
	# Add rules to manage the output data of notebooks
	@git config --local filter.dropoutput_jupyter.clean "make --silent pipe_clear_jupyter_output"
	@git config --local filter.dropoutput_jupyter.smudge cat
	@[ -e .gitattributes ] && grep -v dropoutput_jupyter .gitattributes >.gitattributes.new 2>/dev/null || true
	@[ -e .gitattributes.new ] && mv .gitattributes.new .gitattributes || true
	@echo "*.ipynb filter=dropoutput_jupyter diff=dropoutput_jupyter -text" >>.gitattributes
endif
{% endif %}
ifeq ($(shell which daff >/dev/null ; echo "$$?"),0)
	# Add rules to manage diff with daff for CSV file
	@git config --local diff.daff-csv.command "daff.py diff --git"
	@git config --local merge.daff-csv.name "daff.py tabular merge"
	@git config --local merge.daff-csv.driver "daff.py merge --output %A %O %A %B"
	@[ -e .gitattributes ] && grep -v daff-csv .gitattributes >.gitattributes.new 2>/dev/null
	@[ -e .gitattributes.new ] && mv .gitattributes.new .gitattributes
	@echo "*.[tc]sv diff=daff-csv merge=daff-csv -text" >>.gitattributes
endif
{% if cookiecutter.use_DVC == 'y' %}
ifeq ($(shell which dvc >/dev/null ; echo "$$?"),0)
	# Add DVC/Git integration
	@dvc install
endif{% endif %}
{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour vérifier la présence d'un environnement Conda conforme
# avant le lancement d'un traitement.
# Il faut ajouter $(VALIDATE_VENV) dans les recettes
# et choisir la version à appliquer.
# Soit :
# - CHECK_VENV pour vérifier l'activation d'un VENV avant de commencer
# - ACTIVATE_VENV pour activer le VENV avant le traitement
# Pour cela, sélectionnez la version de VALIDATE_VENV qui vous convient.
# Attention, toute les règles proposées ne sont pas compatible avec le mode ACTIVATE_VENV{% endif %}
CHECK_VENV=@if [[ "$(VENV)" != "$(CONDA_DEFAULT_ENV)" ]] ; \
  then echo -e "$(green)Use: $(cyan)conda activate $(VENV)$(green) before using 'make'$(normal)"; exit 1 ; fi

ACTIVATE_VENV=source $(CONDA_BASE)/etc/profile.d/conda.sh && conda activate $(VENV) $(CONDA_ARGS)
DEACTIVATE_VENV=source $(CONDA_BASE)/etc/profile.d/conda.sh && conda deactivate

VALIDATE_VENV=$(CHECK_VENV)
#VALIDATE_VENV=$(ACTIVATE_VENV)
{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour gérer correctement toute les dépendences python du projet.
# La cible `requirements` se charge de gérer toutes les dépendences
# d'un projet Python. Dans le SNIPPET présenté, il y a de quoi gérer :
# - les dépendances PIP{% if cookiecutter.use_text_processing == 'y' %}
# - l'import de données pour spacy
# - l'import de données pour nltk{% endif %}{% if cookiecutter.use_jupyter == 'y' %}
# - la gestion d'un kernel pour Jupyter{% endif %}
#
# Il suffit, dans les autres de règles, d'ajouter la dépendances sur `$(REQUIREMENTS)`
# pour qu'un simple `make test` garantie la mise à jour de l'environnement avant
# le lancement des tests par exemple.
#
# Pour cela, il faut indiquer dans le fichier 'setup.py', toutes les dépendances
# de run et de test (voir le modèle de `setup.py` proposé)
{% endif %}
# All dependencies of the project must be here
.PHONY: requirements dependencies
{% if cookiecutter.use_rapids == 'y' %}
REQUIREMENTS=$(RAPIDS) $(PIP_PACKAGE) \{% else %}
REQUIREMENTS=$(PIP_PACKAGE) \{% endif %}
{% if cookiecutter.use_text_processing == 'y' %}	$(NLTK_DATABASE) $(SPACY_DATABASE) \
{% endif %}	.gitattributes
requirements: $(REQUIREMENTS)
dependencies: requirements

{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour gérer le mode offline.
# La cible `offline` permet de télécharger toutes les dépendences, pour pouvoir les utiliser
# ensuite sans connexion. Ensuite, il faut valoriser la variable d'environnement OFFLINE
# à True avant le lancement du make pour une utilisation sans réseau.
# `export OFFLINE=True
# make ...
# unset OFFLINE`{% endif %}

# TODO: faire une regle ~/.offline et un variable qui s'ajuste pour tirer la dépendances ?
# ou bien le faire à la main ?
# Download dependencies for offline usage
~/.mypypi: setup.py
	pip download '.[dev,test]' --dest ~/.mypypi
# Download modules and packages before going offline
offline: ~/.mypypi
ifeq ($(OFFLINE),True)
CONDA_ARGS+=--use-index-cache --use-local --offline
PIP_ARGS+=--no-index --find-links ~/.mypypi
endif

# Rule to check the good installation of python in Conda venv
$(CONDA_PYTHON):
	@$(VALIDATE_VENV)
	conda install -q "python=$(PYTHON_VERSION).*" -y $(CONDA_ARGS)

{% if cookiecutter.use_rapids == 'y' %}
# Rule to install NVIDIA Rapid
RAPIDS=$(CONDA_PACKAGE)/cuda
.PHONY: install-rapids
## Install NVidia rapids framework
install-rapids: $(RAPIDS)
$(RAPIDS):
ifeq ($(USE_GPU),-gpu)
	@echo "$(green)  Install NVidia Rapids...$(normal)"
	conda install -q -y $(CONDA_ARGS) \
		cudf==$(CUDF_VER) \
		cudatoolkit==$(CUDA_VER) \
		dask-cuda \
		dask-cudf \
		dask-labextension
else
	conda install -q -y $(CONDA_ARGS) \
		dask-labextension
endif
	touch $(RAPIDS)
%{ endif %}
# Rule to update the current venv, with the dependencies describe in `setup.py`
$(PIP_PACKAGE): $(CONDA_PYTHON) setup.py | .git # Install pip dependencies
	@$(VALIDATE_VENV)
	echo -e "$(cyan)Install setup.py dependencies ... (may take minutes)$(normal)"
	pip install $(PIP_ARGS) $(EXTRA_INDEX) -e '.[dev,test]' | grep -v 'already satisfied' || true
	echo -e "$(cyan)setup.py dependencies updated$(normal)"
	@touch $(PIP_PACKAGE)
{% if cookiecutter.use_jupyter == 'y' %}{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour gérer les kernels Jupyter{% endif %}
# Intall a Jupyter kernel
$(JUPYTER_DATA_DIR)/kernels/$(KERNEL): $(REQUIREMENTS)
	@$(VALIDATE_VENV)
	python $(PYTHON_ARGS) -O -m ipykernel install --user --name $(KERNEL)
	echo -e "$(cyan)Kernel $(KERNEL) installed$(normal)"

# Remove the Jupyter kernel
.PHONY: remove-kernel
remove-kernel: $(REQUIREMENTS)
	@echo y | jupyter kernelspec uninstall $(KERNEL) 2>/dev/null || true
	echo -e "$(yellow)Warning: Kernel $(KERNEL) uninstalled$(normal)"

{% if cookiecutter.add_makefile_comments == 'y' %}# ---------------------------------------------------------------------------------------
# SNIPPET pour gener les extensions jupyter
#$(JUPYTER_LABEXTENSIONS)/dask-labextension:
#	jupyter labextension install dask-labextension{% endif %}
$(JUPYTER_LABEXTENSIONS_DIR)/%:
	@echo -e "$(green)Install jupyter labextension $* $(normal)"
	jupyter labextension install $*
{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour gener les extensions jupyter{% endif %}
$(JUPYTER_LABEXTENSIONS)/%:
	jupyter labextension install $*

JUPYTER_EXTENSIONS:= $(JUPYTER_LABEXTENSIONS)/dask-labextension{% endif %}
{% if cookiecutter.use_text_processing == 'y' %}{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour récupérer les bases de données de nltk.
# Vous devez valoriser NLTK_DATA https://www.nltk.org/data.html{% endif %}
ifndef NLTK_DATA
export NTLK_DATA
# The next line slowed the Makefile.
#NLTK_DATA:=$(shell python -c "import nltk.data; print(nltk.data.path[0])" 2>/dev/null || true)
# Else
ifeq ($(OS),Darwin)
ifeq ($(wildcard ~/nltk_data), )
NLTK_DATA:=/usr/local/share/nltk_data
else
NLTK_DATA:=~/nltk_data
endif
else ifeq ($(OS),Windows)
NLTK_DATA:=C:/nltk_data
else
ifeq ($(wildcard ~/nltk_data), )
NLTK_DATA:=/usr/share/nltk_data
else
NLTK_DATA:=~/nltk_data
endif
endif
endif

# Add here the NLTK database.
# For example, add
# NLTK_DATABASE= \
#   $(NLTK_DATA)/corpora/wordnet \
#   $(NLTK_DATA)/tokenizers/punkt \
#   $(NLTK_DATA)/corpora/stopwords
# and that's all.
NLTK_DATABASE=

$(NLTK_DATA)/tokenizers/%: $(PIP_PACKAGE)
ifneq ($(OFFLINE),True)
	@$(VALIDATE_VENV)
	python $(PYTHON_ARGS) -O -m nltk.downloader $* || true
	touch $(NLTK_DATA)/tokenizers/$*
else
	@echo -e "$(red)Can not download NLTK in offline mode$(normal)"
endif

$(NLTK_DATA)/corpora/%: $(PIP_PACKAGE)
ifneq ($(OFFLINE),True)
	@$(VALIDATE_VENV)
	echo -e "$(cyan)Download $*...$(normal)"
	python $(PYTHON_ARGS) -O -m nltk.downloader $* || true
	touch $(NLTK_DATA)/corpora/$*
else
	@echo -e "$(red)Can not download NLTK in offline mode$(normal)"
endif{% endif %}
{% if cookiecutter.use_tensorflow == "y" %}
$(CONDA_PREFIX)/bin/tensorboard:
	@pip install $(PIP_ARGS) -q tensorboard
## Start tensorbard
tensorboard: $(CONDA_PREFIX)/bin/tensorboard
	tensorboard --host localhost --logdir $(TENSORFLOW_LOGDIR)
{% if cookiecutter.use_aws == 'y' %}
## Start tensorbord on EC2
ec2-tensorboard: clean-pyc $(CONDA_PREFIX)/bin/tensorboard
ifeq ($(OFFLINE),True)
	@echo -e "$(red)Can not use ssh-ec2 in offline$(normal)"
else
	set -x
	ssh-ec2 --stop -L 6006:localhost:6006 "tensorboard --host localhost --logdir $(TENSORFLOW_LOGDIR)"
endif
{% endif %}
{% endif %}
{% if cookiecutter.use_text_processing == 'y' %}{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour récupérer les bases de données de spacy.{% endif %}
# Add here the Spacy database.
# For exemple :
# SPACY_DATABASE= \
#   $(CONDA_PACKAGE)/spacy/data/en
# and that's all.
.PHONY: spacy-database
SPACY_DATABASE=

$(CONDA_PACKAGE)/spacy/data/%: $(PIP_PACKAGE)
ifneq ($(OFFLINE),True)
	@$(VALIDATE_VENV)
	echo -e "$(cyan)Download $*...$(normal)"
	python $(PYTHON_ARGS) -O -m spacy download $*
	@touch $(CONDA_PACKAGE)/spacy/data/$*
else
	@echo -e "$(red)Can not download Spacy database in offline mode$(normal)"
endif{% endif %}
{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour préparer l'environnement d'un projet juste après un `git clone`{% endif %}
.PHONY: configure
## Prepare the work environment (conda venv, kernel, ...)
configure:
	@conda create --name "$(VENV)" python=$(PYTHON_VERSION) -y $(CONDA_ARGS)
	@if [[ "base" == "$(CONDA_DEFAULT_ENV)" ]] || [[ -z "$(CONDA_DEFAULT_ENV)" ]] ; \
	then echo -e "Use: $(cyan)conda activate $(VENV)$(normal)" ; fi
{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------{% endif %}
.PHONY: remove-venv
remove-$(VENV):
	@$(DEACTIVATE_VENV)
	conda env remove --name "$(VENV)" -y 2>/dev/null
	echo -e "Use: $(cyan)conda deactivate$(normal)"
# Remove virtual environement
remove-venv : remove-$(VENV)
{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET de mise à jour des dernières versions des composants.
# Après validation, il est nécessaire de modifier les versions dans le fichier `setup.py`
# pour tenir compte des mises à jours{% endif %}
.PHONY: upgrade-venv
upgrade-$(VENV):
ifeq ($(OFFLINE),True)
	@echo -e "$(red)Can not upgrade virtual env in offline mode$(normal)"
else
	@$(VALIDATE_VENV)
	conda update --all $(CONDA_ARGS)
	pip list --format freeze --outdated | sed 's/(.*//g' | xargs -r -n1 pip install $(EXTRA_INDEX) -U
	@echo -e "$(cyan)After validation, upgrade the setup.py$(normal)"
endif
# Upgrade packages to last versions
upgrade-venv: upgrade-$(VENV)
{% if cookiecutter.use_jupyter == 'y' %}{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET de validation des notebooks en les ré-executants.
# L'idée est d'avoir un sous répertoire par phase, dans le répertoire `notebooks`.
# Ainsi, il suffit d'un `make nb-run-phase1` pour valider tous les notesbooks du répertoire `notebooks/phase1`.
# Pour valider toutes les phases : `make nb-run-*`.
# L'ordre alphabétique est utilisé. Il est conseillé de préfixer chaque notebook d'un numéro.{% endif %}
.PHONY: nb-run-*
notebooks/.make-%: $(PIP_PACKAGE) $(JUPYTER_DATA_DIR)/kernels/$(KERNEL)
	$(VALIDATE_VENV)
	time jupyter nbconvert \
	  --ExecutePreprocessor.timeout=-1 \
	  --execute \
	  --inplace notebooks/$*/*.ipynb
	date >notebooks/.make-$*
# All notebooks
notebooks/phases: $(sort $(subst notebooks/,notebooks/.make-,$(wildcard notebooks/*)))

## Invoke all notebooks in lexical order from notebooks/<% dir>
nb-run-%: $(JUPYTER_DATA_DIR)/kernels/$(KERNEL)
	VENV=$(VENV) $(MAKE) --no-print-directory notebooks/.make-$*
{% endif %}
{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET de validation des scripts en les ré-executant.
# Ces scripts peuvent être la traduction de Notebook Jupyter, via la règle `make nb-convert`.
# L'idée est d'avoir un sous répertoire par phase, dans le répertoire `scripts`.
# Ainsi, il suffit d'un `make run-phase1` pour valider tous les scripts du répertoire `scripts/phase1`.
# Pour valider toutes les phases : `make run-*`.
# L'ordre alphabétique est utilisé. Il est conseillé de préfixer chaque script d'un numéro.{% endif %}
.PHONY: run-*
scripts/.make-%: $(REQUIREMENTS)
	$(VALIDATE_VENV)
	time ls scripts/$*/*.py | grep -v __ | sed 's/\.py//g; s/\//\./g' | \
		xargs -L 1 -t python $(PYTHON_ARGS) -O -m
	@date >scripts/.make-$*

# All phases
scripts/phases: $(sort $(subst scripts/,scripts/.make-,$(wildcard scripts/*)))

## Invoke all script in lexical order from scripts/<% dir>
run-%:
	$(MAKE) --no-print-directory scripts/.make-$*
{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour valider le code avec flake8 et pylint{% endif %}
.PHONY: lint
.pylintrc:
	pylint --generate-rcfile > .pylintrc

.make-lint: $(REQUIREMENTS) $(PYTHON_SRC) | .pylintrc
	$(VALIDATE_VENV)
	@echo -e "$(cyan)Check lint...$(normal)"
	@echo "---------------------- FLAKE"
	@flake8 $(PRJ_PACKAGE)
	@echo "---------------------- PYLINT"
	@pylint $(PRJ_PACKAGE)
	touch .make-lint

## Lint the code
lint: .make-lint

{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour valider le typage avec pytype{% endif %}
$(CONDA_PREFIX)/bin/pytype:
	@pip install $(PIP_ARGS) -q pytype

pytype.cfg: $(CONDA_PREFIX)/bin/pytype
	@[[ ! -f pytype.cfg ]] && pytype --generate-config pytype.cfg || true
	touch pytype.cfg

.PHONY: typing
.make-typing: $(REQUIREMENTS) $(CONDA_PREFIX)/bin/pytype pytype.cfg $(PYTHON_SRC)
	$(VALIDATE_VENV)
	@echo -e "$(cyan)Check typing...$(normal)"
	# pytype
	pytype --config pytype.cfg "$(PRJ)"
	for phase in scripts/*
	do
	  [[ -e "$$phase" ]] && ( cd $$phase && find -L . -type f -name '*.py' -exec pytype --config pytype.cfg {} \; )
	done
	touch ".pytype/pyi/$(PRJ)"
	touch .make-typing

	# mypy
	# TODO: find Pandas stub
	# MYPYPATH=./stubs/ mypy "$(PRJ)"
	# touch .make-mypy

## Check python typing
typing: .make-typing

## Add infered typing in module
add-typing: typing
	@find -L "$(PRJ)" -type f -name '*.py' -exec merge-pyi -i {} .pytype/pyi/{}i \;
	for phase in scripts/*
	do
	  ( cd $$phase ; find -L . -type f -name '*.py' -exec merge-pyi -i {} .pytype/pyi/{}i \; )
	done

{% if cookiecutter.use_docker == 'y' %}
{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour créer un environnement 'make' dans un conteneur Docker.{% endif %}
.PHONY: docker-make-image docker-make-shell docker-make-clean
## Create a docker image to build the project with make
docker-make-image: docker/MakeDockerfile
	$(CHECK_DOCKER)
	echo -e "$(green)Build docker image '$(DOCKER_REPOSITORY)/$(PRJ)-make' to build the project...$(normal)"
	REPO=$(shell git remote get-url origin)
	echo "REPO=$$REPO"
	docker build \
		--build-arg UID=$$(id -u) \
		--build-arg REPO="$$REPO" \
		--build-arg BRANCH=develop \
		--tag $(DOCKER_REPOSITORY)/$(PRJ)-make \
		-f docker/MakeDockerfile .
	printf	"$(green)Declare\n$(cyan)alias dmake='docker run -v $$PWD:/$(PRJ) -it $(DOCKER_REPOSITORY)/$(PRJ)-make'$(normal)\n"
	@echo -e "$(green)and $(cyan)dmake ...  # Use make in a Docker container$(normal)"

## Start a shell to build the project in a docker container
docker-make-shell:
	@docker run --rm \
		-v $(PWD):/$(PRJ) \
		--group-add $$(getent group docker | cut -d: -f3) \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-v $(PWD):/$(PRJ) \
		{% if (cookiecutter.use_aws == 'y' or cookiecutter.use_s3 == 'y') %}
		-v $$HOME/.aws:/home/$(PRJ)/.aws \{% endif %}
		--entrypoint $(SHELL) \
		-it $(DOCKER_REPOSITORY)/$(PRJ)-make

docker-make-clean:
	@docker image rm $(DOCKER_REPOSITORY)/$(PRJ)-make
	@echo -e "$(cyan)Docker image '$(DOCKER_REPOSITORY)/$(PRJ)-make' removed$(normal)"{% endif %}
{% if cookiecutter.use_airflow == 'y' %}
{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour créer un environnement Docker.{% endif %}
## Build docker dev
build-docker-dev:
	docker-compose -f docker/docker-compose-dev.yml build

## Start docker dev
up-docker-dev:
	docker-compose -f docker/docker-compose-dev.yml up
{% endif %}


{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour créer la documentation html et pdf du projet.
# Il est possible d'indiquer build/XXX, ou XXX correspond au type de format
# à produire. Par exemple: html, singlehtml, latexpdf, ...
# Voir https://www.sphinx-doc.org/en/master/usage/builders/index.html{% endif %}
.PHONY: docs
# Use all processors
#PPR SPHINX_FLAGS=-j$(NPROC)
SPHINX_FLAGS=
# Generate API docs
#PPR: Voir Mkdoc https://news.ycombinator.com/item?id=17717513
docs/source: $(REQUIREMENTS) $(PYTHON_SRC)
	$(VALIDATE_VENV)
	sphinx-apidoc -f -o docs/source $(PRJ)/
	touch docs/source

# Build the documentation in specificed format (build/html, build/latexpdf, ...)
build/%: $(REQUIREMENTS) docs/source docs/* *.md | .git
	@$(VALIDATE_VENV)
	@TARGET=$(*:build/%=%)
ifeq ($(OFFLINE),True)
	if [ "$$TARGET" != "linkcheck" ] ; then
endif
	@echo "Build $$TARGET..."
	@LATEXMKOPTS=-silent sphinx-build -M $$TARGET docs build $(SPHINX_FLAGS)
	touch build/$$TARGET
ifeq ($(OFFLINE),True)
	else
		@echo -e "$(red)Can not to build '$$TARGET' in offline mode$(normal)"
	fi
endif
# Build all format of documentations
## Generate and show the HTML documentation
docs: build/html
	@$(BROWSER) build/html/index.html

{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour créer une distribution des sources{% endif %}
.PHONY: sdist
dist/$(PRJ_PACKAGE)-*.tar.gz: $(REQUIREMENTS)
	@$(VALIDATE_VENV)
	python $(PYTHON_ARGS) setup.py sdist

# Create a source distribution
sdist: dist/$(PRJ_PACKAGE)-*.tar.gz
{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour créer une distribution des binaires au format egg.
# Pour vérifier la version produite :
# python setup.py --version
# Cela correspond au dernier tag d'un format 'version'{% endif %}
.PHONY: bdist
dist/$(subst -,_,$(PRJ_PACKAGE))-*.whl: $(REQUIREMENTS) $(PYTHON_SRC)
	@$(VALIDATE_VENV)
	python $(PYTHON_ARGS) setup.py bdist_wheel

# Create a binary wheel distribution
bdist: dist/$(subst -,_,$(PRJ_PACKAGE))-*.whl
{% if cookiecutter.add_makefile_comments == 'y' %}

# ---------------------------------------------------------------------------------------
# SNIPPET pour créer une distribution des binaires au format egg.
# Pour vérifier la version produite :
# python setup.py --version
# Cela correspond au dernier tag d'un format 'version'{% endif %}
.PHONY: dist

## Create a full distribution
dist: bdist sdist
{% if cookiecutter.open_source_software == 'y' %}{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour tester la publication d'une distribution avant sa publication.{% endif %}
.PHONY: check-twine
## Check the distribution before publication
check-twine: bdist
ifeq ($(OFFLINE),True)
	@echo -e "$(red)Can not check-twine in offline mode$(normal)"
else
	$(VALIDATE_VENV)
	twine check \
		$(shell find dist -type f \( -name "*.whl" -or -name '*.gz' \) -and ! -iname "*dev*" )
endif
{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour tester la publication d'une distribution
# sur test.pypi.org.{% endif %}
.PHONY: test-twine
## Publish distribution on test.pypi.org
test-twine: bdist
ifeq ($(OFFLINE),True)
	@echo -e "$(red)Can not test-twine in offline mode$(normal)"
else
	$(VALIDATE_VENV)
	rm -f dist/*.asc
	twine upload --sign --repository-url https://test.pypi.org/legacy/ \
		$(shell find dist -type f \( -name "*.whl" -or -name '*.gz' \) -and ! -iname "*dev*" )
endif
{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour publier la version sur pypi.org.{% endif %}
.PHONY: release
## Publish distribution on pypi.org
release: clean dist
ifeq ($(OFFLINE),True)
	@echo -e "$(red)Can not release in offline mode$(normal)"
else
	@$(VALIDATE_VENV)
	[[ $$( find dist -name "*.dev*" | wc -l ) == 0 ]] || \
		( echo -e "$(red)Add a tag version in GIT before release$(normal)" \
		; exit 1 )
	rm -f dist/*.asc
	echo "Enter Pypi password"
	twine upload --sign \
		$(shell find dist -type f \( -name "*.whl" -or -name '*.gz' \) -and ! -iname "*dev*" )

endif
{% endif %}
{% if cookiecutter.use_jupyter == 'y' %}{% if cookiecutter.add_makefile_comments == 'y' %}

# ---------------------------------------------------------------------------------------
# SNIPPET pour executer jupyter notebook, mais en s'assurant de la bonne application des dépendances.
# Utilisez `make notebook` à la place de `jupyter notebook`.{% endif %}
.PHONY: notebook
## Start jupyter notebooks
notebook: $(REQUIREMENTS) $(JUPYTER_DATA_DIR)/kernels/$(KERNEL) $(_JUPYTER_LABEXTENSIONS)
	@$(VALIDATE_VENV)
	DATA=$$DATA jupyter lab \
		--notebook-dir=notebooks \
		--ExecutePreprocessor.kernel_name=$(KERNEL){% endif %}
{% if (cookiecutter.use_aws == 'y' or cookiecutter.use_s3 == 'y') %}{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour installer aws cli.{% endif %}
$(CONDA_PREFIX)/bin/aws:
	@pip install $(PIP_ARGS) -q awscli
{% endif %}

{% if cookiecutter.use_s3 == 'y' %}{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour synchroniser les données avec un bucket s3.
# Si le repertoire data/raw est ajouté dans .gitignore, il n'est alors plus
# sauvegardé dans .git. Il sera alors récupéré via s3.{% endif %}
.PHONY: sync_to_s3 sync_from_s3
## Upload Data to S3
sync_to_s3/%: $(CONDA_PREFIX)/bin/aws
ifeq ($(OFFLINE),True)
	@echo -e "$(red)Can not use s3 in offline mode$(normal)"
else
ifeq (default,$(PROFILE))
	aws s3 sync $(DATA)/$(*:sync_to_s3/%=%) $(S3_BUCKET)/data/$(*:sync_to_s3/%=%)
else
	aws s3 sync $(DATA)/$(*:sync_to_s3/%=%) $(S3_BUCKET)/data/$(*:sync_to_s3/%=%) --profile $(PROFILE)
endif
endif

## Download Data from S3
sync_from_s3/%: $(CONDA_PREFIX)/bin/aws
ifeq ($(OFFLINE),True)
	@echo -e "$(red)Can not use s3 in offline$(normal)"
else
ifeq (default,$(PROFILE))
	aws s3 sync $(S3_BUCKET)/data/$(*:sync_from_s3/%=%) $(DATA)/$(*:sync_from_s3/%=%)
else
	aws s3 sync $(S3_BUCKET)/data/$(*:sync_from_s3/%=%) $(DATA)/$(*:sync_from_s3/%=%) --profile $(PROFILE)
endif
endif
{% endif %}
# Download raw data if necessary
$(DATA)/raw:
{% if cookiecutter.use_s3 == 'y' %}	make sync_from_s3/data/raw
{% endif %}

{% if cookiecutter.use_jupyter == 'y' %}{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour convertir tous les notebooks de 'notebooks/' en script
# python dans 'scripts/', déjà compatible avec le mode scientifique de PyCharm Pro.
# Le code utilise un modèle permettant d'encadrer les cellules Markdown dans des strings.
# Les scripts possèdent ensuite le flag d'exécution, pour pouvoir les lancer directement
# via un 'scripts/phase1/1_sample.py'.{% endif %}
.PHONY: nb-convert
# Convert all notebooks to python scripts
_nbconvert:  $(JUPYTER_DATA_DIR)/kernels/$(KERNEL)
	@echo -e "Convert all notebooks..."
	notebook_path=notebooks
	script_path=scripts
	tmpfile=$$(mktemp /tmp/make-XXXXX)
	{% raw %}
	cat >$${tmpfile} <<TEMPLATE
	{% extends 'python.tpl' %}
	{% block in_prompt %}# %%{% endblock in_prompt %}
	{%- block header -%}
	#!/usr/bin/env python
	# coding: utf-8
	{% endblock header %}
	{% block input %}
	{{ cell.source | ipython2python }}{% endblock input %}
	{% block markdowncell scoped %}
	# %% md
	"""
	{{ cell.source  }}
	"""
	{% endblock markdowncell %}
	TEMPLATE
	{% endraw %}
	while IFS= read -r -d '' filename; do
		target=$$(echo $$filename | sed "s/^$${notebook_path}/$${script_path}/g; s/ipynb$$/py/g ; s/[ -]/_/g" )
		mkdir -p $$(dirname $${target})
		jupyter nbconvert --to python --ExecutePreprocessor.kernel_name=$(KERNEL) \
		  --template=$${tmpfile} --stdout "$${filename}" >"$${target}"
		chmod +x $${target}
		@echo -e "Convert $${filename} to $${target}"
	done < <(find -L notebooks -name '*.ipynb' -type f -not -path '*/\.*' -prune -print0)
	echo -e "$(cyan)All new scripts are in $${target}$(normal)"
{% if cookiecutter.add_makefile_comments == 'y' %}
# Version permettant de convertir les notebooks et de la ajouter en même temps à GIT
# en ajoutant le flag +x.{% endif %}
## Convert all notebooks to python scripts
nb-convert: _nbconvert
	@find -L scripts/ -type f -iname "*.py" -exec git add "{}" \;
	@find -L scripts/ -type f -iname "*.py" -exec git update-index --chmod=+x  "{}" \;{% endif %}
{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour nettoyer tous les fichiers générés par le compilateur Python.{% endif %}
.PHONY: clean-pyc
# Clean pre-compiled files
clean-pyc:
	@/usr/bin/find -L . -type f -name "*.py[co]" -delete
	@/usr/bin/find -L . -type d -name "__pycache__" -delete
{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour nettoyer les fichiers de builds (package et docs).{% endif %}
.PHONY: clean-build
# Remove build artifacts and docs
clean-build:
	@/usr/bin/find -L . -type f -name ".make-*" -delete
	@rm -fr build/ dist/* *.egg-info .repository
	@echo -e "$(cyan)Build cleaned$(normal)"
{% if cookiecutter.use_jupyter == 'y' %}{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour nettoyer tous les notebooks{% endif %}
.PHONY: clean-notebooks
## Remove all results in notebooks
clean-notebooks: $(REQUIREMENTS)
	@[ -e notebooks ] && find -L notebooks -name '*.ipynb' -exec jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace {} \;
	@echo -e "$(cyan)Notebooks cleaned$(normal)"{% endif %}
{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------{% endif %}
.PHONY: clean-pip
# Remove all the pip package
clean-pip:
	@$(VALIDATE_VENV)
	pip freeze | grep -v "^-e" | xargs pip uninstall -y
	@echo -e "$(cyan)Virtual env cleaned$(normal)"
{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour nettoyer complètement l'environnement Conda{% endif %}
.PHONY: clean-venv clean-$(VENV)
clean-$(VENV): remove-venv
	@conda create -y -q -n $(VENV) $(CONDA_ARGS)
	@touch setup.py
	@echo -e "$(yellow)Warning: Conda virtualenv $(VENV) is empty.$(normal)"
# Set the current VENV empty
clean-venv : clean-$(VENV)
{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour faire le ménage du projet (hors environnement){% endif %}
.PHONY: clean
## Clean current environment
clean: clean-pyc clean-build {% if cookiecutter.use_jupyter == 'y' %}clean-notebooks{% endif %}
{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour faire le ménage du projet{% endif %}
.PHONY: clean-all
# Clean all environments
clean-all:{% if cookiecutter.use_jupyter == 'y' %} remove-kernel{% endif %} clean remove-venv {% if cookiecutter.use_docker == 'y' %}docker-make-clean{% endif %}
{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour executer les tests unitaires et les tests fonctionnels.
# Utilisez 'NPROC=1 make unit-test' pour ne pas paralléliser les tests
# Voir https://setuptools.readthedocs.io/en/latest/setuptools.html#test-build-package-and-run-a-unittest-suite{% endif %}
ifeq ($(shell test $(NPROC) -gt 1; echo $$?),0)
PYTEST_ARGS ?=-n $(NPROC)  --dist loadgroup
else
PYTEST_ARGS ?=
endif
.PHONY: test unittest functionaltest
.make-unit-test: $(REQUIREMENTS) $(PYTHON_TST) $(PYTHON_SRC)
	@$(VALIDATE_VENV)
	@echo -e "$(cyan)Run unit tests...$(normal)"
	python $(PYTHON_ARGS) -m pytest  -s tests $(PYTEST_ARGS) -m "not functional"
	@date >.make-unit-test
# Run only unit tests
unit-test: .make-unit-test

.make-functional-test: $(REQUIREMENTS) $(PYTHON_TST) $(PYTHON_SRC)
	@$(VALIDATE_VENV)
	@echo -e "$(cyan)Run functional tests...$(normal)"
	python $(PYTHON_ARGS) -m pytest  -s tests $(PYTEST_ARGS) -m "functional"
	@date >.make-functional-test
# Run only functional tests
functional-test: .make-functional-test

.make-test: $(REQUIREMENTS) $(PYTHON_TST) $(PYTHON_SRC)
	@echo -e "$(cyan)Run all tests...$(normal)"
	python $(PYTHON_ARGS) -m pytest $(PYTEST_ARGS) -s tests
	#python $(PYTHON_ARGS) setup.py test
	@date >.make-test
	@date >.make-unit-test
	@date >.make-functional-test
## Run all tests (unit and functional)
test: .make-test

{% if cookiecutter.add_makefile_comments == 'y' %}
# SNIPPET pour vérifier les TU et le recalcul de tout les notebooks et scripts.
# Cette règle est invoqué avant un commit sur la branche master de git.{% endif %}
.PHONY: validate
.make-validate: .make-test .make-typing $(DATA)/raw {% if cookiecutter.use_jupyter == 'y' %}notebooks/* {% endif %}build/html build/linkcheck
	@date >.make-validate
## Validate the version before release
validate: .make-validate
{% if cookiecutter.use_aws == 'y' %}{% if cookiecutter.add_makefile_comments == 'y' %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour ajouter la capacité d'exécuter des recettes sur une instance éphémère EC2.
# Voir https://gitlab.octo.com/pprados/ssh-ec2
# L'utilisation de `$(REQUIREMENTS)` dans chaque règle, permet de s'assurer de la bonne
# mise en place de l'environnement nécessaire à l'exécution de la recette,
# même lorsqu'elle est exécuté sur EC2.
# Par exemple :
# - `make on-ec2-test` execute les TU sur EC2 (Invoque `make test`)
# - `make detach-train` détache le l'apprentissage (Invoque `make train`){% endif %}

# Conda virtual env to use in EC2
VENV_AWS={% if cookiecutter.use_aws == 'y' %}tensorflow_p36{% else %}cntk_p36{% endif %}

# Initialize EC2 instance
# The two first lines add a log of the script in /tmp/user-data.log
# for debug
export AWS_USER_DATA
define AWS_USER_DATA
#!/bin/bash -x
exec > /tmp/user-data.log 2>&1
sudo su - ec2-user -c "conda install -n $(VENV_AWS) make>=4 -y $(CONDA_ARGS)"
endef

# What is the life cycle of EC2 instance  via ssh-ec2 ?
#--leave --stop or --terminate
EC2_LIFE_CYCLE?=--terminate
{% if cookiecutter.add_makefile_comments == 'y' %}
# Recette permettant un `make ec2-test`{% endif %}
.PHONY: ec2-* ec2-tmux-* ec2-detach-* ec2-notebook ec2-ssh
## Call 'make %' recipe on EC2 (`make ec2-train`)
ec2-%: $(CONDA_PREFIX)/bin/aws clean-pyc
ifeq ($(OFFLINE),True)
	@echo -e "$(red)Can not use ssh-ec2 in offline mode$(normal)"
else
	set -x
	ssh-ec2 $(EC2_LIFE_CYCLE) "source activate $(VENV_AWS) ; LC_ALL="en_US.UTF-8" VENV=$(VENV_AWS) make $(*:ec2-%=%)"
endif
{% if cookiecutter.add_makefile_comments == 'y' %}
# Recette permettant d'exécuter une recette avec un tmux activé.
# Par exemple `make ec2-tmux-train`{% endif %}
## Call 'make %' recipe on EC2 with a tmux session (`make ec2-tmux-train`)
ec2-tmux-%: $(CONDA_PREFIX)/bin/aws clean-pyc
ifeq ($(OFFLINE),True)
	@echo -e "$(red)Can not use ssh-ec2 in offline mode$(normal)"
else
	@$(VALIDATE_VENV)
	set -x
	NO_RSYNC_END=n ssh-ec2 --multi tmux --leave "source activate $(VENV_AWS) ; LC_ALL="en_US.UTF-8" VENV=$(VENV_AWS) make $(*:ec2-tmux-%=%)"
endif
{% if cookiecutter.add_makefile_comments == 'y' %}
# Recette permettant un `make ec2-detach-test`
# Il faut faire un ssh-ec2 --finish pour rapatrier les résultats à la fin{% endif %}
## Call 'make %' recipe on EC2 and detach immediatly (`make ec2-detach-train`)
ec2-detach-%: $(CONDA_PREFIX)/bin/aws clean-pyc
ifeq ($(OFFLINE),True)
	@echo -e "$(red)Can not use ssh-ec2 in offline mode$(normal)"
else
	@$(VALIDATE_VENV)
	set -x
	ssh-ec2 --detach $(EC2_LIFE_CYCLE) "source activate $(VENV_AWS) ; LC_ALL="en_US.UTF-8" VENV=$(VENV_AWS) make $(*:ec2-detach-%=%)"
endif
{% if cookiecutter.add_makefile_comments == 'y' %}
# Recette permettant un `make ec2-attach`
# Il faut faire un ssh-ec2 --finish pour rapatrier les résultats à la fin{% endif %}
## Call 'make %' recipe on EC2 and detach immediatly (`make ec2-detach-train`)
ec2-attach: $(CONDA_PREFIX)/bin/aws
ifeq ($(OFFLINE),True)
	@echo -e "$(red)Can not use ssh-ec2 in offline mode$(normal)"
else
	@$(VALIDATE_VENV)
	set -x
	ssh-ec2 --attach
endif
{% if cookiecutter.add_makefile_comments == 'y' %}
# Recette permettant un `make ec2-terminate`{% endif %}
## Call 'make %' recipe on EC2 and detach immediatly (`make ec2-detach-train`)
ec2-terminate: $(CONDA_PREFIX)/bin/aws
ifeq ($(OFFLINE),True)
	@echo -e "$(red)Can not use ssh-ec2 in offline mode$(normal)"
else
	@$(VALIDATE_VENV)
	set -x
	ssh-ec2 --finish
endif
{% if cookiecutter.use_aws == 'y' %}
## Start jupyter notebook on EC2
ec2-notebook: $(CONDA_PREFIX)/bin/aws
ifeq ($(OFFLINE),True)
	@echo -e "$(red)Can not use ssh-ec2 in offline$(normal)"
else
	set -x
	ssh-ec2 --stop -L 8888:localhost:8888 "jupyter notebook --NotebookApp.open_browser=False"
endif
{% endif %}{% endif %}

## Install the tools in conda env
install: $(CONDA_PREFIX)/bin/$(PRJ)

## Install the tools in conda env with 'develop' link
develop:
	python $(PYTHON_ARGS) setup.py develop

## Uninstall the tools from the conda env
uninstall: $(CONDA_PREFIX)/bin/$(PRJ)
	pip uninstall $(PRJ)

{% if cookiecutter.add_makefile_comments == 'y' %}
# Recette permettant un `make installer` pour générer un programme autonome comprennant le code et
# un interpreteur Python. Ainsi, il suffit de le copier et de l'exécuter sans pré-requis{% endif %}
# FIXME: Installer for Alpine ?
dist/$(PRJ)$(EXE): .make-validate
	@PYTHONOPTIMIZE=2 && pyinstaller $(PYINSTALLER_OPT) --onefile $(PRJ)/$(PRJ).py
	touch dist/$(PRJ)
ifeq ($(BACKOS),Windows)
# Must have conda installed on windows with tag_images_for_google_drive env
	/mnt/c/WINDOWS/system32/cmd.exe /C 'conda activate $(PRJ) && python $(PYTHON_ARGS) setup.py develop && pyinstaller --onefile tag_images_for_google_drive/tag_images_for_google_drive.py'
	touch dist/$(PRJ).exe
	echo -e "$(cyan)Executable is here 'dist/$(PRJ).exe'$(normal)"
endif
ifeq ($(OS),Darwin)
	ln -f "dist/$(PRJ)" "dist/$(PRJ).macos"
	echo -e "$(cyan)Executable is here 'dist/$(PRJ).macos'$(normal)"
else
	echo -e "$(cyan)Executable is here 'dist/$(PRJ)'$(normal)"
endif

## Build standalone executable for this OS
installer: dist/$(PRJ)

## Publish the distribution in a local repository
local-repository:
	@pip install pypiserver || true
	mkdir -p .repository/$(PRJ)
	( cd .repository/$(PRJ) ; ln -fs ../../dist/*.whl . )
	echo -e "$(green)export PIP_EXTRA_INDEX_URL=http://localhost:8888/simple$(normal)"
	echo -e "or use $(green)pip install --index-url http://localhost:8888/simple/$(normal)"
	pypi-server -p 8888 .repository/

{% if cookiecutter.use_docker == 'y' %}{% if cookiecutter.add_makefile_comments == 'y' %}
# Recette pour créer un Dockerfile.standalone avec la version du projet.
# Modifiez le code du directement ici.{% endif %}
Dockerfile.standalone: setup.py
	@# Build docker file with setup parameters
	VERSION="$$(./setup.py --version)"
	DESCRIPTION="$$(./setup.py --description)"
	LICENSE="$$(./setup.py --license)"
	AUTHOR="$$(./setup.py --author)"
	AUTHOR_EMAIL="$$(./setup.py --author-email)"
	KEYWORDS="$$(./setup.py --keywords)"
	D='$$'

	cat >Dockerfile.standalone <<EOF
	# DO NOT ADD THIS FILE TO VERSION CONTROL!
	ARG OS_VERSION=latest
	FROM alpine:$${D}{OS_VERSION}

	LABEL version="$${VERSION}"
	LABEL description="$${DESCRIPTION}"
	LABEL license="$${LICENSE}"
	LABEL keywords="$${KEYWORDS}"
	LABEL maintainer="$${AUTHOR}"

	ENV LANG=C.UTF-8
	ENV LC_ALL=C.UTF-8
	WORKDIR /data
	COPY dist/$(PRJ) /usr/local/bin
	ENTRYPOINT [ "/usr/local/bin/$(PRJ)" ]
	# TODO: update parameters
	CMD [ "--help" ]
	EOF

.make-docker-build: Dockerfile.standalone dist/$(PRJ)$(EXE)
	@# Detect release version
	if [[ "$${VERSION}" =~ "^[0-9](\.[0-9])+$$" ]];
	then
		TAG_VERSION=-t "$(DOCKER_REPOSITORY)/$(PRJ):$${VERSION}"
	fi
	$(SUDO) docker build \
		-f Dockerfile.standalone \
		--build-arg OS_VERSION="latest" \
		$${TAG_VERSION} \
		-t "$(DOCKER_REPOSITORY)/$(PRJ):latest" .
	date >.make-docker-build

## Build the docker <PRJ>:latest
docker-build: .make-docker-build

# Reset and rebuild the container
docker-rebuild:
	@rm -f Dockerfile.standalone .make-docker-build
	$(MAKE) --no-print-directory docker-stop docker-start

# Create a dedicated volume
docker-volume:
	@$(SUDO) docker volume inspect "$(PRJ)" >/dev/null 2>&1 || \
	$(SUDO) docker volume create --name "$(PRJ)"
	echo -e "$(cyan)Docker volume '$(PRJ)' created$(normal)"

.cid_docker_daemon: .make-docker-build
	$(SUDO) docker volume inspect "$(PRJ)" >/dev/null 2>&1 || $(MAKE) --no-print-directory docker-volume
	# Remove --detach if it's not a daemon
	$(SUDO) docker run \
		--detach \
		--cidfile ".cid_docker_daemon" \
		-v $(PRJ):/data \
		-it "$(DOCKER_REPOSITORY)/$(PRJ):latest"
	echo -e "$(cyan)Docker daemon started$(normal)"

# Start and attach the container
docker-run: .cid_docker_daemon docker-attach

## Start a daemon container with the docker image
docker-start: .cid_docker_daemon

## Attach to the docker
docker-attach: .cid_docker_daemon
	@CID=$$(cat .cid_docker_daemon)
	$(SUDO) docker attach "$${CID}"

## Connect a bash in the container
docker-bash: .cid_docker_daemon
	@CID=$$(cat .cid_docker_daemon)
	$(SUDO) docker exec -i -t "$${CID}" /bin/bash

## Stop the container daemon
docker-stop:
	@if [[ -e ".cid_docker_daemon" ]] ; then
		CID=$$(cat .cid_docker_daemon)
		$(SUDO) docker stop "$${CID}" || true
		rm -f .cid_docker_daemon
		echo -e "$(cyan)Docker daemon stopped$(normal)"
	fi

docker-logs: .cid_docker_daemon
	@$(SUDO) docker container logs -f "$(PRJ)"

docker-top: .cid_docker_daemon
	@$(SUDO) docker container top "$(PRJ)"
{% endif %}

{% if cookiecutter.use_DVC == 'y' %}
{% include 'DVC.mak' %}
{% else %}
{% include 'Classic.mak' %}
{% endif %}
