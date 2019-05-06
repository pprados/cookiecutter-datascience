#!/usr/bin/env make
{% if cookiecutter.add_makefile_comments == "y" %}
# SNIPPET Le shebang précédant permet de creer des alias des cibles du Makefile.
# Il faut que le Makefile soit executable
# 	chmod u+x Makefile
# 	git update-index --chmod=+x Makefile
# Puis, par exemple
# 	ln -s Makefile configure
# 	ln -s Makefile test
# 	ln -s Makefile train
# 	./configure		# Execute make test
# 	./test 			# Execute make test
#   ./train 		# Train the model
# Attention, il n'est pas possible de passer les paramètres aux scripts{% endif %}{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour changer le mode de gestion du Makefile.
# Avec ces trois paramètres, toutes les lignes d'une recette sont invoquées dans le même shell.
# Ainsi, il n'est pas nécessaire d'ajouter des '&&' ou des '\' pour regrouper les lignes.
# Comme Make affiche l'intégralité du block de la recette avant de l'exécuter, il n'est
# pas toujours facile de savoir quel est la ligne en échec.
# Je vous conseille dans ce cas d'ajouter au début de la recette 'set -x'
# Attention : il faut une version > 4 de  `make` (`make -v`).
# Sur Mac : https://stackoverflow.com/questions/38901894/how-can-i-install-a-newer-version-of-make-on-mac-os
# Les versions CentOS d'Amazone ont une version 3.82.
# Utilisez `conda install -n $(VENV_AWS) make>=4 -y`{% endif %}
# WARNING: Use make >4.0
SHELL=/bin/bash
.SHELLFLAGS = -e -c
.ONESHELL:
{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour détecter l'OS d'exécution.{% endif %}
ifeq ($(OS),Windows_NT)
    OS := Windows
else
    OS := $(shell sh -c 'uname 2>/dev/null || echo Unknown')
endif
{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour détecter la présence d'un GPU afin de modifier le nom du projet
# et ses dépendances si nécessaire.{% endif %}
ifdef GPU
USE_GPU:=$(shell [[ "$$GPU" == yes ]] && echo "-gpu")
else ifneq ("$(wildcard /proc/driver/nvidia)","")
USE_GPU:=-gpu
else ifdef CUDA_PATH
USE_GPU:=-gpu
endif
{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour récupérer les séquences de caractères pour les couleurs
# A utiliser avec un
# echo -e "Use '$(cyan)make$(normal)' ..."
# Si vous n'utilisez pas ce snippet, les variables de couleurs non initialisés
# sont simplement ignorées.{% endif %}
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
{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour gérer le projet, le virtualenv et le kernel
# Par convention, les noms du projet, de l'environnement Conda ou le Kernel Jupyter
# correspondent au nom du répertoire du projet.
# Il est possible de modifier cela, en valorisant les variables VENV et/ou KERNEL
# avant le lancement du Makefile (`VENV=cntk_p36 make`){% endif %}
PRJ:=$(shell basename $(shell pwd))
VENV ?= $(PRJ)
{% if cookiecutter.use_jupyter == "y" %}KERNEL ?=$(VENV){% endif %}
PRJ_PACKAGE:=$(PRJ)$(USE_GPU)
PYTHON_VERSION:={{ cookiecutter.python_version }}
{% if cookiecutter.use_aws == "y" %}S3_BUCKET?=s3://$(PRJ)
PROFILE = default{% endif %}
{% if cookiecutter.add_makefile_comments == "y" %}
{% if cookiecutter.use_DVC == "y" %}
# Use DVC bucket. May be :
# DVC_BUCKET?=s3://$(PRJ)
# DVC_BUCKET?=gs://$(PRJ)
# DVC_BUCKET?=ssh://user@example.com:
# DVC_BUCKET?=hdfs://user@example.com
DVC_BUCKET?={% if cookiecutter.use_aws == "y" %}$(S3_BUCKET){% else %}~/.dvc{% endif %}
{% endif %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour reconstruire tous les chemins importants permettant
# de gérer correctement les dépendances des modules sous Conda.
# Cela servira à gérer automatiquement les environnements.
# Pour que cela fonctionne, il faut avoir un environement Conda actif,
# identifié par la variable CONDA_PREFIX (c'est généralement le cas).{% endif %}
CONDA_BASE=$(shell conda info --base)
CONDA_PACKAGE:=$(CONDA_PREFIX)/lib/python$(PYTHON_VERSION)/site-packages
CONDA_PYTHON:=$(CONDA_PREFIX)/bin/python
PIP_PACKAGE:=$(CONDA_PACKAGE)/$(PRJ_PACKAGE).egg-link
{% if cookiecutter.use_jupyter == "y" %}JUPYTER_DATA_DIR:=$(shell jupyter --data-dir 2>/dev/null || echo "~/.local/share/jupyter"){% endif %}
{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour ajouter des repositories complémentaires à PIP.
# A utiliser avec par exemple
# pip $(EXTRA_INDEX) install ...{% endif %}
EXTRA_INDEX:=--extra-index-url=https://pypi.anaconda.org/octo/label/dev/simple
{% if cookiecutter.add_makefile_comments == "y" %}
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
{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour affichier la valeur d'une variable d'environnement
# tel quelle est vue par le Makefile. Par exemple 'make dump-CONDA_PACKAGE'{% endif %}
.PHONY: dump-*
dump-%:
	@if [ "${${*}}" = "" ]; then
		echo "Environment variable $* is not set";
		exit 1;
	else
		echo "$*=${${*}}";
	fi
{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour gérer les Notebooks avec GIT.
# Les recettes suivantes s'assure que git est bien initialisé
# et ajoute des recettes pour les fichiers *.ipynb
# et eventuellement pour les fichiers *.csv.
#
# Pour cela, un fichier .gitattribute est maintenu à jour.
# Les recettes pour les notebooks se chargent de les nettoyer avant de les commiter.
# Pour cela, elles appliquent `jupyter nbconvert` à la volée. Ainsi, les comparaisons
# de version ne sont plus parasités par les data.
#
# Les scripts pour les CSV utilisent le composant `daff` (pip install daff)
# pour comparer plus efficacement les évolutions des fichiers csv.
# Un `git diff toto.csv` est plus clair.

# S'assure de la présence de git (util en cas de synchronisation sur le cloud par exemple,
# après avoir exclus le répertoire .git -cf ssh-ec2){% endif %}
.git:
	@git init -q
{% if cookiecutter.use_jupyter == "y" %}{% if cookiecutter.add_makefile_comments == "y" %}
# Règle importante, invoquées lors du `git commit` d'un fichier *.ipynb via
# le paramètrage de `.gitattributes`.{% endif %}
.PHONY: pipe_clear_jupyter_output
pipe_clear_jupyter_output:
	jupyter nbconvert --to notebook --ClearOutputPreprocessor.enabled=True <(cat <&0) --stdout 2>/dev/null
{% endif %}
# Initialiser la configuration de Git
.gitattributes: | .git  # Configure git
	@git config --local core.autocrlf input
	# Set tabulation to 4 when use 'git diff'
	@git config --local core.page 'less -x4'

{% if cookiecutter.use_DVC == "n" %}
ifeq ($(shell which git-lfs >/dev/null ; echo "$$?"),0)
	# Add git lfs if possible
	@git lfs install >/dev/null
	# Add some extensions in lfs
	@git lfs track "*.pkl"  >/dev/null
	@git lfs track "*.bin"  >/dev/null
	@git lfs track "*.jpg"  >/dev/null
	@git lfs track "*.jpeg" >/dev/null
	@git lfs track "*.gif"  >/dev/null
	@git lfs track "*.png"  >/dev/null
endif
{% endif %}

{% if cookiecutter.use_jupyter == "y" %}ifeq ($(shell which jupyter >/dev/null ; echo "$$?"),0)
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

ifeq ($(shell which dvc >/dev/null ; echo "$$?"),0)
	# Add DVC/Git integration
	dvc install
endif
{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour vérifier la présence d'un environnement Conda conforme
# avant le lancement d'un traitement.
# Il faut ajouter $(VALIDATE_VENV) dans les recettes
# et choisir la version à appliquer.
# Soit :
# - CHECK_VENV pour vérifier l'activation d'un VENV avant de commencer
# - ACTIVATE_VENV pour activer le VENV avant le traitement (merci les 3 lignes magiques)
# Pour cela, sélectionnez la version de VALIDATE_VENV qui vous convient.{% endif %}
CHECK_VENV=@if [[ "base" == "$(CONDA_DEFAULT_ENV)" ]] || [[ -z "$(CONDA_DEFAULT_ENV)" ]] ; \
  then ( echo -e "$(green)Use: $(cyan)conda activate $(VENV)$(green) before using 'make'$(normal)"; exit 1 ) ; fi

ACTIVATE_VENV=source $(CONDA_BASE)/bin/activate $(VENV)
DEACTIVATE_VENV=source $(CONDA_BASE)/bin/deactivate $(VENV)

VALIDATE_VENV=$(CHECK_VENV)
#VALIDATE_VENV=$(ACTIVATE_VENV)
{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour gérer correctement toute les dépendances python du projet.
# La cible `requirements` se charge de gérer toutes les dépendances
# d'un projet Python. Dans le SNIPPET présenté, il y a de quoi gérer :
# - les dépendances PIP{% if cookiecutter.use_text_processing == "y" %}
# - l'import de données pour spacy
# - l'import de données pour nltk{% endif %}{% if cookiecutter.use_jupyter == "y" %}
# - la gestion d'un kernel pour Jupyter{% endif %}
#
# Il suffit, dans les autres de règles, d'ajouter la dépendances sur `$(REQUIREMENTS)`
# pour qu'un simple `make test` garantie la mise à jour de l'environnement avant
# le lancement des tests par exemple.
#
# Pour cela, il faut indiquer dans le fichier setup.py, toutes les dépendances
# de run et de test (voir l'exemple `setup.py`){% endif %}

# Toutes les dépendances du projet à regrouper ici
.PHONY: requirements
REQUIREMENTS=$(PIP_PACKAGE) \
{% if cookiecutter.use_text_processing == "y" %}		$(NLTK_DATABASE) $(SPACY-DATABASE) \
{% endif %}		.gitattributes
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
{% if cookiecutter.use_jupyter == "y" %}{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour gérer les kernels Jupyter{% endif %}
# Règle d'installation du Kernel pour Jupyter
$(JUPYTER_DATA_DIR)/kernels/$(KERNEL): $(PIP_PACKAGE)
	$(VALIDATE_VENV)
	python -O -m ipykernel install --user --name $(KERNEL)

# Règle de suppression du kernel
.PHONY: remove-kernel
remove-kernel:
	@echo y | jupyter kernelspec uninstall $(KERNEL) 2>/dev/null || true
	echo -e "$(yellow)Warning: Kernel $(KERNEL) uninstalled$(normal)"{% endif %}
{% if cookiecutter.use_text_processing == "y" %}{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour récupérer les bases de données de nltk.
# Ci-dessous, la recette pour lister toutes les bases.
# Vous pouvez valoriser NLTK_DATA https://www.nltk.org/data.html{% endif %}
ifndef NLTK_DATA
export NTLK_DATA
# La ligne suivante ralentie le Makefile. A activer qu'avec des env. spécifiques.
#NLTK_DATA:=$(shell python -c "import nltk.data; print(nltk.data.path[0])" 2>/dev/null || true)
# Sinon, utiliser le code suivant
ifeq ($(OS),Darwin)
ifeq ($(wildcard ~/nltk_data), )
NLTK_DATA=/usr/local/share/nltk_data
else
NLTK_DATA=~/nltk_data
endif
else ifeq ($(OS),Windows)
NLTK_DATA=C:/nltk_data
else
ifeq ($(wildcard ~/nltk_data), )
NLTK_DATA=/usr/share/nltk_data
else
NLTK_DATA=~/nltk_data
endif
endif
endif

# Ajoutez ici les bases de données supplémentaires.
# Par exemple, ajoutez
# NLTK_DATABASE=$(PIP_PACKAGE) \
# $(NLTK_DATA)/corpora/wordnet \
# $(NLTK_DATA)/tokenizers/punkt \
# $(NLTK_DATA)/corpora/stopwords
# et c'est tout.
NLTK_DATABASE=$(PIP_PACKAGE) \


# Les recettes génériques de downloads
$(NLTK_DATA)/tokenizers/%: $(PIP_PACKAGE)
	$(VALIDATE_VENV)
	python -O -m nltk.downloader $*
	touch ~/nltk_data/tokenizers/$*

$(NLTK_DATA)/corpora/%: $(PIP_PACKAGE)
	$(VALIDATE_VENV)
	python -O -m nltk.downloader $*
	touch ~/nltk_data/corpora/$*{% endif %}
{% if cookiecutter.use_text_processing == "y" %}{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour récupérer les bases de données de spacy.
# Ci-dessous, la recette pour lister toutes les bases{% endif %}
# Ajoutez les bases complémentaires.
# Par exemple :
# SPACY-DATABASE=$(PIP_PACKAGE) \
#   $(CONDA_PACKAGE)/spacy/data/en
# et c'est tout.
.PHONY: spacy-database
SPACY-DATABASE=$(PIP_PACKAGE) \


# La recette générique de téléchargement
$(CONDA_PACKAGE)/spacy/data/%: $(PIP_PACKAGE)
	$(VALIDATE_VENV)
	python -O -m spacy download $*
	@touch $(CONDA_PACKAGE)/spacy/data/$*{% endif %}
{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour préparer l'environnement d'un projet juste après un `git clone`{% endif %}
.PHONY: configure
## Prepare the environment (conda venv, kernel, ...)
configure:
	@conda create --name "$(VENV)" python=$(PYTHON_VERSION) -y
	echo -e "Use: $(cyan)conda activate $(VENV)$(normal)"
{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------{% endif %}
.PHONY: remove-venv
remove-$(VENV):
	@$(DEACTIVATE_VENV)
	conda env remove --name "$(VENV)" -y
	echo -e "Use: $(cyan)conda deactivate$(normal)"
# Remove venv
remove-venv : remove-$(VENV)
{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET de mise à jour des dernières versions des composants.
# Après validation, il est nécessaire de modifier les versions dans le fichier `setup.py`
# pour tenir compte des mises à jours{% endif %}
.PHONY: upgrade-venv
upgrade-$(VENV):
	$(VALIDATE_VENV)
	conda update --all
	pip list --format freeze --outdated | sed 's/(.*//g' | xargs -r -n1 pip install $(EXTRA_INDEX) -U
	echo -e "$(cyan)After validation, upgrade the setup.py$(normal)"
# Upgrade packages to last versions
upgrade-venv: upgrade-$(VENV)
{% if cookiecutter.use_jupyter == "y" %}{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET de validation des notebooks en les ré-executants.
# L'idée est d'avoir un sous répertoire par phase, dans le répertoire `notebooks`.
# Ainsi, il suffit d'un `make nbbuild-phase1` pour valider tous les notesbooks du répertoire `notebooks/phase1`.
# Pour valider toutes les phases : `make nbbuild-*`.
# L'ordre alphabétique est utilisé. Il est conseillé de préfixer chaque notebook d'un numéro.{% endif %}
.PHONY: nbbuild-*
## Invoke all notebooks in lexical order from pipeline/%
nbbuild-%: $(REQUIREMENTS)
	$(VALIDATE_VENV)
	time jupyter nbconvert \
	  --ExecutePreprocessor.timeout=-1 \
	  --execute \
	  --inplace notebooks/$*/*.ipynb{% endif %}
{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET de validation des scripts en les ré-executants.
# Ces scripts peuvent être la traduction de Notebook Jupyter, via la règle 'make nbconvert'.
# L'idée est d'avoir un sous répertoire par phase, dans le répertoire `notebooks`.
# Ainsi, il suffit d'un `make build-phase1` pour valider tous les scripts du répertoire `scripts/phase1`.
# Pour valider toutes les phases : `make build-*`.
# L'ordre alphabétique est utilisé. Il est conseillé de préfixer chaque notebook d'un numéro.{% endif %}
.PHONY: build-*
## Invoke all script in lexical order from pipeline/<dir>
build-%: $(REQUIREMENTS)
	$(VALIDATE_VENV)
	time ls pipeline/$*/*.py | grep -v __ | sed 's/\.py//g; s/\//\./g' | \
		xargs -L 1 -t python -O -m
{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour valider le code avec flake8{% endif %}
.PHONY: lint
## Lint TODO
lint: $(REQUIREMENTS)
	flake8 src
{% if cookiecutter.use_jupyter == "y" %}{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour executer jupyter notebook, mais en s'assurant de la bonne application des dépendances.
# Utilisez 'make notebook' à la place de 'jupyter notebook'.{% endif %}
.PHONY: notebook
## Start jupyter notebooks
notebook: $(REQUIREMENTS) $(JUPYTER_DATA_DIR)/kernels/$(KERNEL)
	$(VALIDATE_VENV)
	jupyter notebook{% endif %}
{% if cookiecutter.use_aws == "y" %}{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour synchroniser les données avec un buket s3{% endif %}
.PHONY: sync_data_to_s3 sync_data_from_s3
## Upload Data to S3
sync_data_to_s3:
ifeq (default,$(PROFILE))
	aws s3 sync data/ s3://$(S3_BUCKET)/data/
else
	aws s3 sync data/ s3://$(S3_BUCKET)/data/ --profile $(PROFILE)
endif

## Download Data from S3
sync_data_from_s3:
ifeq (default,$(PROFILE))
	aws s3 sync s3://$(S3_BUCKET)/data/ data/
else
	aws s3 sync s3://$(S3_BUCKET)/data/ data/ --profile $(PROFILE)
endif{% endif %}
{% if cookiecutter.use_jupyter == "y" %}{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour convertir tous les notebooks du repertoire 'notebooks' en script
# python dans le répertoire 'src/scripts', déjà compatible avec le mode scientifique de PyCharm Pro.
# Le code utilise un modèle permettant d'encadrer les cellules Markdown dans des strings.
# Les scripts possède ensuite le flag d'exécution, pour pouvoir les lancer directement
# via un 'scripts/phase1/1_sample.py'.{% endif %}
.PHONY: nbconvert add_nbconvert_to_git
# Convert all notebooks to python scripts
_nbconvert:  $(JUPYTER_DATA_DIR)/kernels/$(KERNEL)
	@echo -e "Convert all notebooks..."
	notebook_path=notebooks
	script_path=src/scripts
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
		jupyter nbconvert --to python --template=$${tmpfile} --stdout "$${filename}" >"$${target}"
		chmod +x $${target}
		@echo -e "Convert $${filename} to $${target}"
	done < <(find notebooks -name '*.ipynb' -type f -not -path '*/\.*' -prune -print0)
	echo -e "$(cyan)All new scripts are in $${target}$(normal)"
{% if cookiecutter.add_makefile_comments == "y" %}
# Version permettant de convertir les notebooks et de la ajouter en même temps à GIT
# en ajouter le flag +x.{% endif %}
## Convert all notebooks to python scripts
nbconvert: _nbconvert
	find scripts/ -type f -iname "*.py" -exec git add "{}" \;
	find scripts/ -type f -iname "*.py" -exec git update-index --chmod=+x  "{}" \;{% endif %}
{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour nettoyer tous les fichiers générés par le compilateur Python.{% endif %}
.PHONY: clean-pyc
# Clean pre-compiled files
clean-pyc:
	-/usr/bin/find . -type f -name "*.py[co]" -delete
	-/usr/bin/find . -type d -name "__pycache__" -delete
{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour nettoyer les fichiers de builds.{% endif %}
.PHONY: clean-build
## Remove build artifacts
clean-build:
	@echo "+ $@"
	@rm -fr build/
	@rm -fr dist/
	@rm -fr *.egg-info
{% if cookiecutter.use_jupyter == "y" %}{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour nettoyer tous les notebooks{% endif %}
.PHONY: clean-notebooks
## Remove all results of notebooks
clean-notebooks:
	@[ -e notebooks ] && find notebooks -name '*.ipynb' -exec jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace {} \;
	@echo "Notebooks cleaned"{% endif %}
{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------{% endif %}
.PHONY: clean-pip
# Remove all the pip package
clean-pip:
	$(VALIDATE_VENV)
	pip freeze | grep -v "^-e" | xargs pip uninstall -y
{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour nettoyer complètement l'environnement Conda{% endif %}
.PHONY: clean-venv clean-$(VENV)
clean-$(VENV): remove-venv
	@echo -e "$(cyan)Re-create virtualenv $(VENV)...$(normal)"
	conda create -y -q -n $(VENV)
	touch setup.py
	echo -e "$(yellow)Warning: Conda virtualenv $(VENV) is empty.$(normal)"
# Set the current VENV empty
clean-venv : clean-$(VENV)
{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour faire le ménage du projet (hors environnement){% endif %}
.PHONY: clean
## Clean current environment
{% if cookiecutter.use_jupyter == "y" %}clean: clean-pyc clean-build clean-notebooks{% else %}clean: clean-pyc clean-build{% endif %}
{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour faire le ménage du projet (hors environnement){% endif %}
.PHONY: clean-all
## Clean all environments
{% if cookiecutter.use_jupyter == "y" %}clean-all: clean remove-venv remove-kernel{% else %}clean-all: clean remove-venv{% endif %}
{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour déclencher les tests unitaires{% endif %}
.PHONY: test
## Run all tests
test: $(REQUIREMENTS)
	$(VALIDATE_VENV)
	python -m unittest discover -s tests -b
{% if cookiecutter.add_makefile_comments == "y" %}
# SNIPPET pour vérifier les TU et le recalcule de tous les notebooks{% endif %}
.PHONY: validate
## Validate the version before commit
validate: test build-*
{% if cookiecutter.use_aws == "y" %}{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour ajouter la capacité d'exécuter des recettes sur une instance éphémère EC2.
# Voir https://gitlab.octo.com/pprados/ssh-ec2
# L'utilisation de `$(REQUIREMENTS)` dans chaque règle, permet de s'assurer de la bonne
# mise en place de l'environnement nécessaire à l'exécution de la recette,
# même lorsqu'elle est exécuté sur EC2.
# Par exemple :
# - `make on-ec2-test` execute les TU sur EC2
# - `make detach-build-all` détache le recalcule tous les notebooks sur EC2{% endif %}

# Quel venv utilisé sur l'instance EC2 ?
VENV_AWS=cntk_p36

# Initialisation de l'instance EC2
export AWS_USER_DATA
# Les deux premières lignes permettent d'avoir une trace de l'initialisation
# de l'instance EC2 sur /tmp/user-data.log
# C'est pratique pour le debug
define AWS_USER_DATA
#!/bin/bash -x
exec > /tmp/user-data.log 2>&1
sudo su - ec2-user -c "conda install -n $(VENV_AWS) make>=4 -y"
endef

# Quel est le cycle de vie par défaut des instances, via ssh-ec2 ?
#EC2_LIFE_CYCLE=--terminate
EC2_LIFE_CYCLE=--leave
{% if cookiecutter.add_makefile_comments == "y" %}
# Recette permettant un 'make ec2-test'{% endif %}
.PHONY: ec2-* ec2-tmux-* ec2-detach-* ec2-notebook ec2-ssh
## Call 'make %' recipe on EC2 (make ec2-train)
ec2-%:
	$(VALIDATE_VENV)
	ssh-ec2 $(EC2_LIFE_CYCLE) "source activate $(VENV_AWS) ; VENV=$(VENV_AWS) make $(*:ec2-%=%)"
{% if cookiecutter.add_makefile_comments == "y" %}
# Recette permettant d'exécuter une recette avec un tmux activé.
# Par exemple `make ec2-tmux-train`{% endif %}
## Call 'make %' recipe on EC2 with a tmux session (`make ec2-tmux-train`)
ec2-tmux-%:
	$(VALIDATE_VENV)
	NO_RSYNC_END=n ssh-ec2 --multi tmux --leave "source activate $(VENV_AWS) ; VENV=$(VENV_AWS) make $(*:ec2-tmux-%=%)"
{% if cookiecutter.add_makefile_comments == "y" %}
# Recette permettant un 'make ec2-detach-test'
# Il faut faire un ssh-ec2 --finish pour rapatrier les résultats à la fin{% endif %}
## Call 'make %' recipe on EC2 and detach immediatly (`make ec2-detach-train`)
ec2-detach-%:
	$(VALIDATE_VENV)
	ssh-ec2 --detach $(EC2_LIFE_CYCLE) "source activate $(VENV_AWS) ; VENV=$(VENV_AWS) make $(*:ec2-detach-%=%)"
{% if cookiecutter.use_jupyter == "y" %}
## Start jupyter notebook on EC2
ec2-notebook:
	$(VALIDATE_VENV)
	ssh-ec2 --stop -L 8888:localhost:8888 "jupyter notebook --NotebookApp.open_browser=False"
{% endif %}{% endif %}

{#
# ---------------------------------------------------------------------------------------
# EXPERIMENTAL SNIPPET pour calculer automatiquement les dépendances entres fichiers python.
# Pour cela, il faut installer [importlab](https://github.com/google/importlab)
# et ajouter pour chaque fichiers python
# toto.py: $(call python_dep,toto.py)
# Comme c'est très lent, je déconseille d'utiliser cette approche.
define python_dep
	$(shell importlab --tree $1 2>/dev/null | grep -v '::' | grep '^ .*\.py$$')
endef

#}

{% if cookiecutter.use_DVC == "y" %}
{% include 'DVC.mak' %}
{% else %}
{% include 'Classic.mak' %}
{% endif %}