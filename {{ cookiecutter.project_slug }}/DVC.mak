
{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------{% endif %}
# Function to invoke DVC run
# $1 : dvc file
# $2 : cmd to invoke (python ...)
# $3 : empty or -M
define dvc_run
	if [ -e $1 ] ; then dvc remove $1 ; fi
	rm -f $1
	#dvc remove $(addsuffix .dvc,$@)
	#	--no-commit
	dvc run -f $1 \
		$(addprefix -d ,$(filter-out .%,$?)) \
		$(if $3,-M $@,-o $@) \
	$2
	if [ -e $(@D)/.gitignore ] ; then git add $(@D)/.gitignore ; fi
	if [ -e $1 ] ; then git add $1 ; fi
endef

{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# Initialize DVC{% endif %}
.dvc: | .git
	dvc init
	dvc config cache.protected true
	dvc remote add -d origin $(DVC_BUCKET)
	git add .dvc/config
REQUIREMENTS += | .dvc
{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour initialiser DVC avec la production de fichiers distants dans des buckets
# Voir: https://dvc.org/doc/user-guide/external-outputs
# Use :
# - make dvc-external-s3cache
# - make dvc-external-gscache
# - make dvc-external-azurecache
# - make dvc-external-sshcache
# - make dvc-external-htfscache{% endif %}
.PHONY: dvc-external-*
## Initialize the DVC external cache provider (dvc-external-s3cache)
dvc-external-%: .dvc
	dvc remote add ${*} $(BUCKET)/cache
	dvc config cache.gs $*
{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour vérouiller un fichier DVC pour ne plus le reconstruire, meme si cela
# semble nécessaire. C'est util en phase de développement.
# See https://dvc.org/doc/commands-reference/lock{% endif %}
# Lock DVC file
lock-%: .dvc
	dvc lock $(*:lock-%=%)
{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour afficher les métrics gérées par DVC.
# See https://dvc.org/doc/commands-reference/metrics{% endif %}
## show the DVC metrics
metrics: .dvc
	dvc metrics show
{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour supprimer les fichiers de DVC du projet{% endif %}
# Remove all .dvc files
clean-dvc:
	rm -Rf .dvc
	-/usr/bin/find . -type f -name "*.dvc" -delete

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################
#
# ┌─────────┐ ┌──────────┐ ┌───────┐ ┌──────────┐ ┌───────────┐
# │ prepare ├─┤ features ├─┤ train ├─┤ evaluate ├─┤ visualize │
# └─────────┘ └──────────┘ └───────┘ └──────────┘ └───────────┘
#

SOURCES=$(shell find {{ cookiecutter.project_slug }}/ -type f -name '*.py')
TOOLS=$(shell find {{ cookiecutter.project_slug }}/ -mindepth 2 -type f -name '*.py')
.PHONY: prepare features train evaluate visualize

# Rule to declare an implicite dependencies from sub module for all root project files
{{ cookiecutter.project_slug }}/*.py : $(TOOLS)
	@touch $@

data/interim/datas-prepared.csv: $(REQUIREMENTS) {{ cookiecutter.project_slug }}/prepare_dataset.py data/raw/*
	$(call dvc_run,prepare.dvc,\
	python -O -m {{ cookiecutter.project_slug }}.prepare_dataset \
		data/raw/datas.csv \
		data/interim/datas-prepared.csv\
	)
prepare.dvc: data/interim/datas-prepared.csv
## Prepare the dataset
prepare: prepare.dvc

data/interim/datas-features.csv : $(REQUIREMENTS) {{ cookiecutter.project_slug }}/build_features.py data/interim/datas-prepared.csv
	$(call dvc_run,feature.dvc,\
	python -O -m {{ cookiecutter.project_slug }}.build_features \
		data/interim/datas-prepared.csv \
		data/interim/datas-features.csv\
	)
## Add features
features: data/interim/datas-features.csv

models/model.pkl : $(REQUIREMENTS) {{ cookiecutter.project_slug }}/train_model.py data/interim/datas-features.csv
	$(call dvc_run,train.dvc,\
	python -O -m {{ cookiecutter.project_slug }}.train_model \
		data/interim/datas-features.csv \
		models/model.pkl \
	)
## Train the model
train: models/model.pkl


reports/auc.metric: $(REQUIREMENTS) {{ cookiecutter.project_slug }}/evaluate_model.py models/model.pkl
	$(call dvc_run,evaluate.dvc,\
	python -O -m {{ cookiecutter.project_slug }}.evaluate_model \
		models/model.pkl \
		data/interim/datas-features.csv \
		reports/auc.metric \
	,-M \
	)
## Evalutate the model
evaluate: reports/auc.metric

## Visualize the result
visualize: $(REQUIREMENTS) {{ cookiecutter.project_slug }}/visualize.py models/model.pkl
	$(call dvc_run,visualize.dvc,\
	python -O -m {{ cookiecutter.project_slug }}.visualize \
		reports/ \
	)
{% if cookiecutter.add_makefile_comments == "y" %}
# See https://dvc.org/doc/commands-reference/repro{% endif %}
.PHONY: repro
## 	Re-run commands recorded in the last DVC stages in the same order.
repro: evaluate.dvc
	dvc repro $<

