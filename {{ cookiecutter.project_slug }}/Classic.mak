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

$(DATA)/interim/datas-prepared.csv : $(REQUIREMENTS) {{ cookiecutter.project_slug }}/prepare_dataset.py $(DATA)/raw/*
	@python -O -m {{ cookiecutter.project_slug }}.prepare_$(DATA)set \
		$(DATA)/raw/datas.csv \
		$(DATA)/interim/datas-prepared.csv
## Prepare the dataset
prepare: $(DATA)/interim/datas-prepared.csv

$(DATA)/processed/datas-features.csv : $(REQUIREMENTS) {{ cookiecutter.project_slug }}/build_features.py $(DATA)/interim/datas-prepared.csv
	@python -O -m {{ cookiecutter.project_slug }}.build_features \
		$(DATA)/interim/datas-prepared.csv \
		$(DATA)/processed/datas-features.csv
## Add features
features: $(DATA)/processed/datas-features.csv

models/model.pkl : $(REQUIREMENTS) {{ cookiecutter.project_slug }}/train_model.py $(DATA)/processed/datas-features.csv
	@python -O -m {{ cookiecutter.project_slug }}.train_model \
		$(DATA)/processed/datas-features.csv \
		models/model.pkl
## Train the model
train: models/model.pkl

reports/auc.metric: $(REQUIREMENTS) {{ cookiecutter.project_slug }}/evaluate_model.py models/model.pkl
	@python -O -m {{ cookiecutter.project_slug }}.evaluate_model \
		models/model.pkl \
		$(DATA)/processed/datas-features.csv \
		reports/auc.metric
## Evalutate the model
evaluate: reports/auc.metric

## Visualize the result
visualize: $(REQUIREMENTS) {{ cookiecutter.project_slug }}/visualize.py models/model.pkl
	@python -O -m {{ cookiecutter.project_slug }}.visualize \
	    'reports/*.metric'
