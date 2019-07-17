# PROJECT RULES                                                                 #
#################################################################################
#
# ┌─────────┐ ┌───────┐ ┌──────────┐ ┌───────────┐
# │ prepare ├─┤ train ├─┤ evaluate ├─┤ visualize │
# └─────────┘ └───────┘ └──────────┘ └───────────┘
#
#.NOTPARALLEL:
NPROC = 0 # PPR: si tensorflow ?

# Meta-parameters
ifeq ($(DEBUG),True)
FILTER=$(DATA)/processed/\*\*/21\*.jpg
EPOCHS=--epochs 1
BATCH_SIZE=--batch-size 1
else
FILTER=$(DATA)/processed/\*\*/\*.jpg
EPOCHS=--epochs 10
BATCH_SIZE=--batch-size 16
endif
SEED=--seed 12345

## Clean all intermediate files for pipeline
clean-run: clean-build
	rm -rf $(DATA)/processed/* models/model_flower_classifier.*

$(DATA)/raw/flower_photos.tgz: | .dvc
	dvc pull
	[[ -e $(DATA)/raw/flower_photos.tgz ]] || \
	wget -P $(DATA)/raw/ 'http://download.tensorflow.org/example_images/flower_photos.tgz'

.PHONY: prepare features train evaluate visualize

# Rule to declare an implicite dependencies from sub module for all root project files
TOOLS:=$(shell find flower_classifier/ -mindepth 2 -type f -name '*.py')
flower_classifier/*.py : $(TOOLS)
	@touch $@

prepare.dvc \
$(DATA)/processed/*: $(REQUIREMENTS) \
	flower_classifier/prepare_dataset.py \
	$(DATA)/raw/flower_photos.tgz
	dvc run -q -f prepare.dvc \
		--overwrite-dvcfile \
		--ignore-build-cache \
		-d flower_classifier/prepare_dataset.py \
		-d flower_classifier/tools \
		-d $(DATA)/raw/flower_photos.tgz \
		-o $(DATA)/processed/ \
	python -O -m flower_classifier.prepare_dataset \
		$(DATA)/raw/flower_photos.tgz \
		$(DATA)/processed/
	git add prepare.dvc

## Prepare the dataset
prepare: $(DATA)/processed/*

train.dvc \
models/model_flower_classifier.h5 \
models/model_flower_classifier.pkl : $(REQUIREMENTS) \
	flower_classifier/train_model.py \
	$(DATA)/processed/*
	dvc run -q -f train.dvc \
		--overwrite-dvcfile \
		--ignore-build-cache \
		-d flower_classifier/train_model.py \
		-d flower_classifier/tools \
		-d $(DATA)/processed/ \
		-o models/model_flower_classifier.h5 \
		-o models/model_flower_classifier.pkl \
	python -O -m flower_classifier.train_model \
		$(SEED) \
		$(BATCH_SIZE) \
		$(EPOCHS) \
		'$(FILTER)' \
		models/model_flower_classifier.h5 \
		models/model_flower_classifier.pkl
	git add train.dvc

## Train the model
train: models/model_flower_classifier.h5


# Last step of pipeline
Dvcfile.dvc \
reports/metric.json: $(REQUIREMENTS) \
	flower_classifier/evaluate_model.py \
	models/model_flower_classifier.h5 \
	models/model_flower_classifier.pkl
	dvc run -q -f Dvcfile.dvc \
		--overwrite-dvcfile \
		--ignore-build-cache \
		-d flower_classifier/evaluate_model.py \
		-d flower_classifier/tools \
		-d models/model_flower_classifier.h5 \
		-d models/model_flower_classifier.pkl \
		-M reports/metric.json \
	python -O -m flower_classifier.evaluate_model \
		'$(FILTER)' \
		models/model_flower_classifier.h5 \
		models/model_flower_classifier.pkl \
		reports/metric.json
	git add Dvcfile.dvc

## Evalutate the model
evaluate: reports/metric.json

## Visualize the result
visualize: $(REQUIREMENTS) \
	flower_classifier/visualize.py \
	models/model_flower_classifier.h5 \
	reports/metric.json
	@dvc metrics show -a -x acc
	@python -O -m flower_classifier.visualize \
		$(DATA)/processed/\*\*/11\*.jpg \
		models/model_flower_classifier.h5 \
		models/model_flower_classifier.pkl \
		--interactive False




