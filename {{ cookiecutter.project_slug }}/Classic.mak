
.PHONY: prepare features train evaluate visualize

data/interim/datas-prepared.csv : $(PRJ)/prepare_dataset.py data/raw/*
	python -O -m $(PRJ).prepare_dataset \
		data/raw/datas.csv \
		data/interim/datas-prepared.csv
prepare: data/interim/datas-prepared.csv

data/interim/datas-features.csv : $(PRJ)/build_features.py data/interim/datas-prepared.csv
	python -O -m $(PRJ).build_features \
		data/interim/datas-prepared.csv \
		data/interim/datas-features.csv
features: data/interim/datas-features.csv

models/model.pkl : $(PRJ)/train_model.py data/interim/datas-features.csv
	python -O -m $(PRJ).train_model \
		data/interim/datas-features.csv \
		models/model.pkl
train: models/model.pkl

reports/: $(PRJ)/evaluate_model.py models/model.pkl
	python -O -m $(PRJ).evaluate_model \
		models/model.pkl \
		data/interim/datas-features.csv \
		reports/
	@touch reports/
evaluate: reports/auc.metric

visualize: $(PRJ)/visualize.py models/model.pkl
	python -O $(PRJ)/visualize.py reports/