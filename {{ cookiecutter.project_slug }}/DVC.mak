{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# Initialize DVC{% endif %}
.dvc: | .git
	@dvc init
	@dvc config cache.protected true
	@dvc remote add -d origin $(DVC_BUCKET)
	@git add .dvc/config

{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour initialiser DVC avec la production de fichiers distants dans des buckets
# Voir: https://dvc.org/doc/user-guide/external-outputs{% endif %}
# Use :
# - make dvc-external-s3
# - make dvc-external-gs
# - make dvc-external-azure
# - make dvc-external-ssh
# - make dvc-external-htfs
.PHONY: dvc-external-*
## Initialize the DVC external cache provider (dvc-external-s3)
dvc-external-%: $(REQUIREMENTS) | .dvc
	@dvc remote add ${*}cache $(DVC_BUCKET)/cache
	@dvc config cache.${*} ${*}cache
{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour vérouiller un fichier DVC pour ne plus le reconstruire, meme si cela
# semble nécessaire. C'est util en phase de développement.
# See https://dvc.org/doc/commands-reference/lock{% endif %}
# Lock DVC file
lock-%: $(REQUIREMENTS) | .dvc
	@dvc lock $(*:lock-%=%)
{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour dévérouiller un fichier DVC pour pouvoir le reconstruire.
# See https://dvc.org/doc/commands-reference/unlock{% endif %}
# Lock DVC file
unlock-%: $(REQUIREMENTS) | .dvc
	@dvc unlock $(*:lock-%=%)
{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour afficher les métrics gérées par DVC.
# See https://dvc.org/doc/commands-reference/metrics{% endif %}
## show the DVC metrics
metrics: $(REQUIREMENTS) | .dvc
	@dvc metrics show
{% if cookiecutter.add_makefile_comments == "y" %}
# ---------------------------------------------------------------------------------------
# SNIPPET pour supprimer les fichiers de DVC du projet{% endif %}
# Remove all .dvc files
clean-dvc:
	@rm -Rf .dvc
	@-/usr/bin/find . -type f -name "*.dvc" -delete

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################
#
# ┌─────────┐ ┌──────────┐ ┌───────┐ ┌──────────┐ ┌───────────┐
# │ prepare ├─┤ features ├─┤ train ├─┤ evaluate ├─┤ visualize │
# └─────────┘ └──────────┘ └───────┘ └──────────┘ └───────────┘
#

.PHONY: prepare features train evaluate visualize

# Rule to declare an implicite dependencies from sub module for all root project files
TOOLS:=$(shell find {{ cookiecutter.project_slug }}/ -mindepth 2 -type f -name '*.py')
{{ cookiecutter.project_slug }}/*.py : $(TOOLS)
	@touch $@

data/interim/datas-prepared.csv: $(REQUIREMENTS) {{ cookiecutter.project_slug }}/prepare_dataset.py data/raw/*
	dvc run -q -f prepare.dvc \
		-d {{ cookiecutter.project_slug }}/prepare_dataset.py \
		-d data/raw/ \
		-o data/interim/datas-prepared.csv \
	python -O -m {{ cookiecutter.project_slug }}.prepare_dataset \
		data/raw/datas.csv \
		data/interim/datas-prepared.csv\
	)
prepare.dvc: data/interim/datas-prepared.csv
## Prepare the dataset
prepare: prepare.dvc

data/interim/datas-features.csv : $(REQUIREMENTS) {{ cookiecutter.project_slug }}/build_features.py data/interim/datas-prepared.csv
	dvc run -q -f features.dvc \
		-d {{ cookiecutter.project_slug }}/build_features.py \
		-d data/interim/datas-prepared.csv \
		-o data/interim/datas-features.csv \
	python -O -m {{ cookiecutter.project_slug }}.build_features \
		data/interim/datas-prepared.csv \
		data/interim/datas-features.csv
## Add features
features: data/interim/datas-features.csv

models/model.pkl : $(REQUIREMENTS) {{ cookiecutter.project_slug }}/train_model.py data/interim/datas-features.csv
	dvc run -q -f train.dvc \
		-d {{ cookiecutter.project_slug }}/train_model.py \
		-d data/interim/datas-features.csv \
	python -O -m {{ cookiecutter.project_slug }}.train_model \{% if cookiecutter.use_tensorflow == "y" %}
	    --logdir $(TENSORFLOW_LOGDIR) \{% endif %}
		data/interim/datas-features.csv \
		models/model.pkl
## Train the model
train: models/model.pkl


reports/metric.json: $(REQUIREMENTS) {{ cookiecutter.project_slug }}/evaluate_model.py models/model.pkl
	dvc run -q -f evaluate.dvc \
		-d {{ cookiecutter.project_slug }}/evaluate_model.py \
		-d models/model.pkl \
		-M reports/metric.json \
	python -O -m {{ cookiecutter.project_slug }}.evaluate_model \
		models/model.pkl \
		data/interim/datas-features.csv \
		reports/metric.json
## Evalutate the model
evaluate: reports/metric.json

## Visualize the result
visualize: $(REQUIREMENTS) {{ cookiecutter.project_slug }}/visualize.py models/model.pkl
	@python -O -m {{ cookiecutter.project_slug }}.visualize \
	    reports/

{% if cookiecutter.add_makefile_comments == "y" %}
# See https://dvc.org/doc/commands-reference/repro{% endif %}
.PHONY: repro
## 	Re-run commands recorded in the last DVC stages in the same order.
repro: evaluate.dvc
	dvc repro $<


