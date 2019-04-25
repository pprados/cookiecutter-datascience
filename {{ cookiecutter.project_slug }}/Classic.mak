# Sous-projet pour essayer de faire des recettes pour DVC (https://dvc.org)
# /!\ WORK IN PROGRESS

# PPR a gérer
PRJ:={{cookiecutter.project_slug}}

.PHONY: prepare
data/interim/datas-prepared.csv : $(PRJ)/prepare_dataset.py data/raw/*
	python -O $(PRJ)/prepare_dataset.py \
		data/raw/datas.csv \
		data/interim/datas-prepared.csv
prepare: data/interim/datas-prepared.csv

.PHONY: features
data/interim/datas-features.csv : $(PRJ)/build_features.py data/interim/datas-prepared.csv
	python -O $(PRJ)/build_features.py \
		data/interim/datas-prepared.csv \
		data/interim/datas-features.csv
features: data/interim/datas-features.csv

.PHONY: train
models/model.pkl : $(PRJ)/train_model.py data/interim/datas-features.csv
	python -O $(PRJ)train_model.py \
		data/interim/datas-features.csv \
		models/model.pkl
train: models/model.pkl


# See https://dvc.org/doc/commands-reference/repro
.PHONY: evaluate
auc.metric: $(PRJ)/predict_model.py models/model.pkl
	python -O $(PRJ)/evaluate_dataset.py \
		models/model.pkl \
		data/interim/datas-features.csv
evaluate: auc.metric
