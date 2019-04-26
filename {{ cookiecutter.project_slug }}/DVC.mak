# /!\ WORK IN PROGRESS
# Sous-projet pour essayer de faire des recettes pour DVC (https://dvc.org)

# Invoke dvc run
# $1 : dvc file
# $2 : cmd to invoke (python ...)
# $3 : empty or -M
define dvc_run
	if [ -e $1 ] ; then dvc remove $1 ; fi
	rm -f $1
	#dvc remove $(addsuffix .dvc,$@)
	#	--no-commit
	dvc run -f $1 \
		$(addprefix -d ,$?) \
		$(if $3,-M $@,-o $@) \
	$2
	#if [ -e $(@D)/.gitignore ] ; then git add $(@D)/.gitignore ; fi
	#if [ -e $1 ] ; then git add $1 ; fi
endef

PRJ:=bda_project

DEPENDENCIES=dvc-init

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
	# FIXME dvc install
	dvc remote add -d dvcremote $(DVC_REMOTE)
	# PPR: fixme ?
	#dvc remote modify dvcremote region eu-west-3
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


.PHONY: prepare
data/interim/datas-prepared.csv: $(PRJ)/prepare_dataset.py data/raw/*
	$(call dvc_run,prepare.dvc,\
	python -O -m $(PRJ).prepare_dataset \
		data/raw/datas.csv \
		data/interim/datas-prepared.csv\
	)
prepare.dvc: data/interim/datas-prepared.csv

prepare: $(DEPENDENCIES) prepare.dvc

.PHONY: features
data/interim/datas-features.csv : $(PRJ)/build_features.py data/interim/datas-prepared.csv
	$(call dvc_run,feature.dvc,\
	python -O -m $(PRJ).build_features \
		data/interim/datas-prepared.csv \
		data/interim/datas-features.csv\
	)
features: $(DEPENDENCIES) data/interim/datas-features.csv

.PHONY: train
models/model.pkl : $(PRJ)/train_model.py data/interim/datas-features.csv
	$(call dvc_run,train.dvc,\
	python -O -m $(PRJ).train_model \
		data/interim/datas-features.csv \
		models/model.pkl \
	)
train: $(DEPENDENCIES) models/model.pkl


.PHONY: evaluate
reports/auc.metric: $(PRJ)/evaluate_model.py models/model.pkl
	$(call dvc_run,Dvcfile,\
	python -O -m $(PRJ).evaluate_model \
		models/model.pkl \
		data/interim/datas-features.csv \
		reports/auc.metric \
	,-M \
	)
evaluate: $(DEPENDENCIES) reports/auc.metric

.PHONY: visualize
visualize: $(DEPENDENCIES) $(PRJ)/visualize.py models/model.pkl
	$(call dvc_run,visualize.dvc,\
	python -O -m $(PRJ).visualize \
		reports/ \
	)

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

