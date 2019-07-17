# PROJECT RULES                                                                 #
#################################################################################
# Mode NORMAL
#
# ┌─────────┐ ┌───────┐ ┌──────────┐ ┌───────────┐
# │ prepare ├─┤ train ├─┤ evaluate ├─┤ visualize │
# └─────────┘ └───────┘ └──────────┘ └───────────┘
#
#.NOTPARALLEL:
NPROC = 0 # PPR: si tensorflow ?

# Meta-parameters
ifeq ($(DEBUG),True)
FILTER=$(DATA)/processed/**/21*.jpg
EPOCHS=--epochs 1
BATCH_SIZE=--batch-size 1
else
FILTER=$(DATA)/processed/**/*.jpg
EPOCHS=--epochs 10
BATCH_SIZE=--batch-size 16
endif
SEED=--seed 12345

## Clean all intermediate files for pipeline
clean-run: clean-build
	rm -rf $(DATA)/processed/* models/model_flower_classifier.*

$(DATA)/raw/flower_photos.tgz:
	wget -P $(DATA)/raw/ 'http://download.tensorflow.org/example_images/flower_photos.tgz'

.PHONY: prepare features train evaluate visualize

# Rule to declare an implicite dependencies from sub module for all root project files
TOOLS:=$(shell find flower_classifier/ -mindepth 2 -type f -name '*.py')
flower_classifier/*.py : $(TOOLS)
	@touch $@

$(DATA)/processed/*: $(REQUIREMENTS) \
	flower_classifier/prepare_dataset.py \
	$(DATA)/raw/flower_photos.tgz
	python -O -m flower_classifier.prepare_dataset \
		$(DATA)/raw/flower_photos.tgz \
		$(DATA)/processed/

## Prepare the dataset
prepare: $(DATA)/processed/*

models/model_flower_classifier.h5 \
models/model_flower_classifier.pkl : $(REQUIREMENTS) \
	flower_classifier/train_model.py \
	$(DATA)/processed/*
	python -O -m flower_classifier.train_model \
		$(SEED) \
		$(BATCH_SIZE) \
		$(EPOCHS) \
		'$(FILTER)' \
		models/model_flower_classifier.h5 \
		models/model_flower_classifier.pkl

## Train the model
train: models/model_flower_classifier.h5


reports/metric.json: $(REQUIREMENTS) \
	$(PYTHON_SRC) \
	flower_classifier/evaluate_model.py \
	models/model_flower_classifier.h5 \
	models/model_flower_classifier.pkl
	python -O -m flower_classifier.evaluate_model \
		'$(FILTER)' \
		models/model_flower_classifier.h5 \
		models/model_flower_classifier.pkl \
		reports/metric.json

## Evalutate the model
evaluate: reports/metric.json

## Visualize the result
visualize: $(REQUIREMENTS) \
	flower_classifier/visualize.py \
	models/model_flower_classifier.h5 \
	reports/metric.json
	@python -O -m flower_classifier.visualize \
		'$(DATA)/processed/**/11*.jpg' \
		models/model_flower_classifier.h5 \
		models/model_flower_classifier.pkl \
		--interactive False



