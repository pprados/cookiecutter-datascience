# Sous-projet pour essayer de faire des recettes pour DVC (https://dvc.org)
# /!\ WORK IN PROGRESS

PRJ:={{cookiecutter.project_slug}}

# ---------------------------------------------------------------------------------------
# See https://github.com/iterative/dvc/issues/211
# SNIPPET initialiser DVC
# see https://dvc.org/doc/get-started/configure

# Note: l'import fonctionne avec cache local, même si s3: ou autres
#DVC_REMOTE?=$(BUCKET)
DVC_REMOTE?=/tmp/$(PRJ)
.dvc:
	dvc init
	# See https://dvc.org/doc/commands-reference/checkout
	dvc install
	dvc add -d remote $(DVC_REMOTE)
	# PPR: fixme ?
	dvc remote modify remote region eu-west-3
	git add .dvc/config
	# Azure https://dvc.org/doc/commands-reference/remote-modify
	# ??? dvc remote modify myremote connection_string my-connection-string


BUCKET?=s3://$(PRJ)
BUCKET?=gs://$(PRJ)
BUCKET?=ssh://user@example.com:
BUCKET?=hdfs://user@example.com

.PHONY: dump-*
dump-%:
	@if [ "${${*}}" = "" ]; then
		echo "Environment variable $* is not set";
		exit 1;
	else
		echo "$*=${${*}}";
	fi

# SNIPPET pour initialiser DVC pour utiliser un distant.
# Voir: https://dvc.org/doc/user-guide/external-outputs
# Voir: https://dvc.org/doc/commands-reference/remote-add
# Use :
# - dvc-init-s3cache
# - dvc-init-gscache
# - dvc-init-azurecache
# - dvc-init-sshcache
# - dvc-init-htfscache
.PHONY: dvc-init-*
## Initialize the DVC cache provider
dvc-init-%:
	dvc remote add ${*} $(BUCKET)/cache
	dvc config cache.gs $*
	# https://dvc.org/doc/commands-reference/config
	dvc config cache.protected true

## Initialize DVC
dvc-init: | .dvc

# Invoke dvc run
# $1 : dvc file
# $2 : cmd to invoke (python ...)
# $3 : empty or -M
define dvc_run
	dvc remove $(addsuffix .dvc,$@)
	dvc run -f $1 \
		--no-commit \
		-d $(DVC_REMOTE) \
		$(addprefix -d ,$?) \
		$(if $3,-M $@,-o $(@D)) \
	$2
	git add data/.gitignore $@
	dvc add $1
endef

.PHONY: prepare
data/interim/datas-prepared.csv : $(PRJ)/prepare_dataset.py data/raw/*
	$(call dvc_run,prepare.dvc,\
	python -O $(PRJ)/prepare_dataset.py \
		data/raw/datas.csv \
		data/interim/datas-prepared.csv\
	)
prepare: data/interim/datas-prepared.csv

.PHONY: features
data/interim/datas-features.csv : $(PRJ)/build_features.py data/interim/datas-prepared.csv
	$(call dvc_run,feature.dvc,\
	python -O $(PRJ)/build_features.py \
		data/interim/datas-prepared.csv \
		data/interim/datas-features.csv\
	)
features: data/interim/datas-features.csv

.PHONY: train
models/model.pkl : $(PRJ)/train_model.py data/interim/datas-features.csv
	$(call dvc_run,train.dvc,\
	python -O $(PRJ)train_model.py \
		data/interim/datas-features.csv \
		models/model.pkl \
	)
train: models/model.pkl


.PHONY: evaluate
auc.metric: $(PRJ)/predict_model.py models/model.pkl
	$(call dvc_run,Dvcfile,\
	python -O $(PRJ)/evaluate_dataset.py \
		models/model.pkl \
		data/interim/datas-features.csv \
	,-M \
	)
evaluate: auc.metric

.PHONY: visualize
reports/*: $(PRJ)/visualize.py models/model.pkl
	$(call dvc_run,visualize.dvc,\
	python -O $(PRJ)/visualize.py \
		models/model.pkl \
		data/interim/datas-features.csv \
	)
visualize: reports/*

# PPR c'est redondant la gestion des dépendances
# Lock file. DVC ne le reconstruit plus. Meme si cela semble nécessaire
# See https://dvc.org/doc/commands-reference/lock
lock-%:
	dvc lock $(*:lock-%=%)

# See https://dvc.org/doc/commands-reference/repro
## 	Rerun commands recorded in the pipeline stages in the same order.
repro: DvcFile
	dvc repro Dvcfile

push:
	git push
	dvc push

# See https://dvc.org/doc/commands-reference/commit
# Approche --no-commit dans le dvc run, pour la recherche
commit-% :
	$(MAKE) $(*:commit-%=%)
	dvc commit

commit:
	dvc commit

# See https://dvc.org/doc/commands-reference/metrics
metrics:
	dvc metrics show

