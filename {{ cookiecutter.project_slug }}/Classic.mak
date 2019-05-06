#################################################################################
# PROJECT RULES                                                                 #
#################################################################################

.PHONY: prepare features train evaluate visualize

# Rule to declare dependencies from tools package for all project files
$(PRJ)/* : $(PRJ)/tools/*
	@touch $@

data/interim/datas-prepared.csv : $(DEPENDENCIES) $(PRJ)/prepare_dataset.py data/raw/*
	python -O -m $(PRJ).prepare_dataset \
		data/raw/datas.csv \
		data/interim/datas-prepared.csv
## Prepare the dataset
prepare: data/interim/datas-prepared.csv

data/interim/datas-features.csv : $(DEPENDENCIES) $(PRJ)/build_features.py data/interim/datas-prepared.csv
	python -O -m $(PRJ).build_features \
		data/interim/datas-prepared.csv \
		data/interim/datas-features.csv
## Add features
features: data/interim/datas-features.csv

models/model.pkl : $(DEPENDENCIES) $(PRJ)/train_model.py data/interim/datas-features.csv
	python -O -m $(PRJ).train_model \
		data/interim/datas-features.csv \
		models/model.pkl
## Train the model
train: models/model.pkl

reports/auc.metric: $(DEPENDENCIES) $(PRJ)/evaluate_model.py models/model.pkl
	python -O -m $(PRJ).evaluate_model \
		models/model.pkl \
		data/interim/datas-features.csv \
		reports/auc.metric
## Evalutate the model
evaluate: reports/auc.metric

## Visualize the result
visualize: $(DEPENDENCIES) $(PRJ)/visualize.py models/model.pkl
	python -O -m $(PRJ).visualize reports/