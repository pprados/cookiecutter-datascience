#################################################################################
# PROJECT RULES                                                                 #
#################################################################################
#
# ┌─────────┐ ┌───────┐ ┌──────────┐ ┌───────────┐
# │ prepare ├─┤ train ├─┤ evaluate ├─┤ visualize │
# └─────────┘ └───────┘ └──────────┘ └───────────┘
#
#.NOTPARALLEL:
NPROC = 0 # PPR: si tensorflow ?

clean-run: clean-build
	rm -rf data/processed/* models/model_flower_classifier.*

data/raw/flower_photos.tgz:
	wget -P data/raw/ 'http://download.tensorflow.org/example_images/flower_photos.tgz'

.PHONY: prepare features train evaluate visualize

# Rule to declare an implicite dependencies from sub module for all root project files
TOOLS:=$(shell find flower_classifier/ -mindepth 2 -type f -name '*.py')
flower_classifier/*.py : $(TOOLS)
	@touch $@

prepare.dvc \
data/processed/*: $(REQUIREMENTS) flower_classifier/prepare_dataset.py data/raw/flower_photos.tgz
	dvc run -q -f prepare.dvc \
		-d flower_classifier/prepare_dataset.py \
		-d data/raw/flower_photos.tgz \
		-o data/processed/ \
	python -O -m flower_classifier.prepare_dataset \
		data/raw/flower_photos.tgz \
		data/processed/

## Prepare the dataset
prepare: data/processed/*

train.dvc \
models/model_flower_classifier.h5 models/model_flower_classifier.pkl : $(REQUIREMENTS) \
	flower_classifier/train_model.py data/processed/*
	dvc run -q -f train.dvc \
		-d flower_classifier/train_model.py \
		-d data/processed/ \
		-o models/model_flower_classifier.h5 \
		-o models/model_flower_classifier.pkl \
	python -O -m flower_classifier.train_model \
		--seed 12345 \
		'data/processed/\*\*/212\*.jpg' \
		models/model_flower_classifier.h5 \
		models/model_flower_classifier.pkl

## Train the model
train: models/model_flower_classifier.h5


evaluate.dvc \
reports/metric.json: $(REQUIREMENTS) flower_classifier/evaluate_model.py \
	models/model_flower_classifier.h5 models/model_flower_classifier.pkl
	dvc run -q -f evaluate.dvc \
		-d flower_classifier/evaluate_model.py \
		-d models/model_flower_classifier.h5 \
		-d models/model_flower_classifier.pkl \
		-M reports/metric.json \
	python -O -m flower_classifier.evaluate_model \
		'data/processed/\*\*/212\*.jpg' \
		models/model_flower_classifier.h5 \
		models/model_flower_classifier.pkl \
		reports/metric.json \

## Evalutate the model
evaluate: reports/metric.json

## Visualize the result
visualize: $(REQUIREMENTS) flower_classifier/visualize.py models/model_flower_classifier.h5
	@python -O -m flower_classifier.visualize \
		data/processed/\*\*/11\*.jpg \
		models/model_flower_classifier.h5 \
		models/model_flower_classifier.pkl \
		--interactive False




