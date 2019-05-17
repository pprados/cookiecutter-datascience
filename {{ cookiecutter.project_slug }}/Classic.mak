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

$(DATA)/interim/datas-prepared.csv : $(REQUIREMENTS) $(PRJ)/prepare_dataset.py $(DATA)/raw/*
	python -O -m $(PRJ).prepare_$(DATA)set \
		$(DATA)/raw/datas.csv \
		$(DATA)/interim/datas-prepared.csv
## Prepare the dataset
prepare: $(DATA)/interim/datas-prepared.csv

$(DATA)/processed/datas-features.csv : $(REQUIREMENTS) $(PRJ)/build_features.py $(DATA)/interim/datas-prepared.csv
	python -O -m $(PRJ).build_features \
		$(DATA)/interim/datas-prepared.csv \
		$(DATA)/processed/datas-features.csv
## Add features
features: $(DATA)/processed/datas-features.csv

models/model.pkl : $(REQUIREMENTS) $(PRJ)/train_model.py $(DATA)/processed/datas-features.csv
	python -O -m $(PRJ).train_model \
		$(DATA)/processed/datas-features.csv \
		models/model.pkl
## Train the model
train: models/model.pkl

reports/auc.metric: $(REQUIREMENTS) $(PRJ)/evaluate_model.py models/model.pkl
	python -O -m $(PRJ).evaluate_model \
		models/model.pkl \
		$(DATA)/processed/datas-features.csv \
		reports/auc.metric
## Evalutate the model
evaluate: reports/auc.metric

## Visualize the result
visualize: $(REQUIREMENTS) $(PRJ)/visualize.py models/model.pkl
	python -O -m $(PRJ).visualize reports/