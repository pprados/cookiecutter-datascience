#################################################################################
# PROJECT RULES                                                                 #
#################################################################################
#
# ┌─────────┐ ┌──────────┐ ┌───────┐ ┌──────────┐ ┌───────────┐
# │ prepare ├─┤ features ├─┤ train ├─┤ evaluate ├─┤ visualize │
# └─────────┘ └──────────┘ └───────┘ └──────────┘ └───────────┘
#

.PHONY: prepare features train evaluate visualize

# Rule to declare dependencies from tools module for all project files
$(PRJ)/*.py : $(PRJ)/tools/*.py
	@touch $@

data/interim/datas-prepared.csv : $(REQUIREMENTS) $(PRJ)/prepare_dataset.py data/raw/*
	python -O -m $(PRJ).prepare_dataset \
		data/raw/datas.csv \
		data/interim/datas-prepared.csv
## Prepare the dataset
prepare: data/interim/datas-prepared.csv

data/processed/datas-features.csv : $(REQUIREMENTS) $(PRJ)/build_features.py data/interim/datas-prepared.csv
	python -O -m $(PRJ).build_features \
		data/interim/datas-prepared.csv \
		data/processed/datas-features.csv
## Add features
features: data/interim/datas-features.csv

models/model.pkl : $(REQUIREMENTS) $(PRJ)/train_model.py data/processed/datas-features.csv
	python -O -m $(PRJ).train_model \
		data/processed/datas-features.csv \
		models/model.pkl
## Train the model
train: models/model.pkl

reports/auc.metric: $(REQUIREMENTS) $(PRJ)/evaluate_model.py models/model.pkl
	python -O -m $(PRJ).evaluate_model \
		models/model.pkl \
		data/interim/datas-features.csv \
		reports/auc.metric
## Evalutate the model
evaluate: reports/auc.metric

## Visualize the result
visualize: $(REQUIREMENTS) $(PRJ)/visualize.py models/model.pkl
	python -O -m $(PRJ).visualize reports/