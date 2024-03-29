# Cookiecutter BDA

Un [modèle](https://gitlab.octo.com/pprados/cookiecutter-bda) raisonable de bootstrap de projet pour BDA.
Ce dernier est inspiré d'un projet similaire : [cookiecutter-data-science](https://drivendata.github.io/cookiecutter-data-science)

## Pré-requis pour utiliser le modèle cookiecutter :
 - [Cookiecutter Python package](http://cookiecutter.readthedocs.org/en/latest/installation.html) >= 1.4.0: 
 Cela peut être installé avec pip ou conda :

```bash
$ pip install cookiecutter
```

ou

```bash
$ conda config --add channels conda-forge
$ conda install cookiecutter
```


## Pour démarrer un nouveau projet, executez:
```bash
    cookiecutter https://github.com/pprados/cookiecutter-datascience.git
```
et répondez aux questions.

## Exemples
Des exemples de projets complet, pour différentes combinaisons de paramètres,
sont disponibles [ici](examples/)

## Principe des projects
- Les projets utilisent un environnement conda pour isoler les dépendances
- Elles doivent être déclarées dans `setup.py`
- Le numéro de version du projet est géré automatiquement via GIT et les tags

Une fois le projet créer, il suffit de se rendre dans le répertoire
et de faire un 
```bash
make configure
```
et suivre les instructions.

Ensuite, un `make help` permet de connaitre les fonctions principales pour gérer le projet.

## Difficulté d'un "bon Makefile"
Un Makefile efficace doit:
- pouvoir executer n'importe quelle règle sans pré-requis
- les règles de constructions doivent pouvoir être exécutés plusieurs fois
de suite. Seule le première invocation produit de nouveaux fichiers. Les autres
invocations ne font rien.

C'est à cette ambition que nous nous sommes attaqué. Par exemple, il est
possible de faire un `make validate` deux fois de suite.

Pour vérifier cela, il faut des tests unitaires construisant un projet avec différentes
combinaisons de paramètres, et qui executent chaque cible du Makefile, sans
rien d'autre auparavant. Les tests du projets procèdent ainsi pour s'assurer
de la bonne rédaction des règles.

## Impact des différentes options
Lors de la création d'un projet, des questions vous sont posées
pour identifier les caractèristiques du projet à créer.
Elles permettent d'alléger le project, en supprimant des règles du `Makefile`
et les fichiers qui ne sont pas nécessaires.

Pour simplifier l'aide, toutes ne sont pas indiquées dans `make help`.
Il suffit de doubler le `#` du commentaire avant une règle pour modifier cela.

### Fonctionalités présentes quelque soit les options

Pour le pipeline de data-science
- `make prepare` # Prepare the dataset
- `make features` # Add features
- `make train` # Train the model
- `make evaluate` # Evalutate the model 
- `make visualize` # Visualize the result

A vous de les enrichir ou de les simplifier si certaines étapes ne sont pas nécessaires.

Le reste des règles sont pour la gestion du projet
- `make help` # Print all majors target
- `make configure`  # Prepare the environment (conda venv, kernel, ...)
- `make run-%` # Invoke all script in lexical order from scripts/<% dir> 
- `make build/%` # Create sphinx documentation with % format (make build/html)
- `make lint` # Lint the code
- `make docs` # Create and show the HTML and PDF doc in 'build/'
- `make test` # Run all tests (unit and functional)
- `make typing` # Check python typing
- `make add-typing` # Add python typing in source code
- `make validate` # Validate the version before commit
- `make clean` # Clean current environment
- `make dist` # Create a binary and source distribution

### use_jupyter
- Un répertoire `notebooks/`
- Une dépendance à jupyter dans `setup.py`
- Des hooks à GIT pour nettoyer les notebooks lors des push/pull
- La gestion d'un kernel Jupyter dédié au projet
- `make remove-kernel` # Pour supprimer le kernel du projet
- `make nb-run-%` # Pour executer tous les notebooks
- `make notebook` # Pour lancer jupyter notebook en gérant les dépendances
- `make nb-convert` # Pour convertir les notebooks en script pythons
- `make clean-notebooks` # Pour nettoyer les données dans les notebooks
- `make ec2-notebook` # Si AWS, pour lancer un notebook sur une instance EC2 (via [ssh-ec2](https://gitlab.octo.com/pprados/ssh-ec2))
 
### use_tensorflow
- Une dépendance à Tensorflow, avec ou sans GPU suivant la plateforme
- L'utilisation de l'environement 'tensorflow_p36' en cas d'utilisation de `ssh-ec2`
- Variable TENSORFLOW_LOGDIR à './logdir'
- `make tensorboard` pour lancer tensorboard en écoute de `TENSORFLOW_LOGDIR` 
- `make ec2-tensorboard` pour lancer tensorboard en écoute de `TENSORFLOW_LOGDIR` sur EC2

### use_text_processing
- Une dépendance à [Spacy](https://spacy.io/) et [NLTK](https://www.nltk.org/)
- Des règles pour gérer les bases de données associées via les variables 
`NLTK_DATABASE` et `SPACY_DATABASE` dans le `Makefile`
 
### use_git_LFS
- Installation des hooks LFS dans le projet si possible
- Tracks des fichiers standards (.pkl, *.bin, *.jpg, *.jpeg, *.git, *.png)

### use_[DVC](https://dvc.org/)
- Modification dès règles du workflow du projet, pour exploiter `dvc run`
- Une variable `DVC_BUCKET` pour indiquer où localiser les données
- `make dvc-external-%` # Pour ajouter un suivit des modifications de fichier externe
- `make lock-%` # Pour bloquer le rebuild d'un fichier DVC
- `make metrics` # Pour afficher les métriques des executions via DVC

### use_aws (utilisation de [ssh-ec2](https://gitlab.octo.com/pprados/ssh-ec2))
- Une dépendance à `awscli` et `boto3`
- `make ec2-%` # Pour executer une règle sur une instance EC2 via `ssh-ec2`
- `make ec2-tmux-%` # Pour executer une règle  sur une instance EC2 via `ssh-ec2` en mode tmux
- `make ec2-detach-%` # Pour détacher une règle sur une instance EC2
- `make ec2-attach` # Pour se rattacher à une instance EC2
- `make ec2-terminate` # Pour se rattacher puis récupérer les résultats

### use_s3
- Une dépendance à `awscli` et `boto3`
- Une variable `S3_BUCKET` pour le bucket du projet
- `make sync_to_s3/%` # Pour envoyer une copie des `data/` vers S3
- `make sync_from_s3/%` # Pour récupérer une copie des `data/` depuis S3
- Une dépandance automatique de `data/raw` avec `s3://bucket` et ajout
de ce répertoire à `.gitignore`

### open_source_software
- Modification des licenses dans `setup.py`
- `make check-twine` # Pour tester le packaging avant publication
- `make test-twine` # Pour tester la publication du package sur [test.pypi.org]((https://test.pypi.org))
- `make twine` # Pour publier la version du package sur [pypi.org](https://pypi.org)

### add_makefile_comments
- Ajout des commentaires "verbeux" dans le `Makefile`

## Snippet de Makefile
Il est également possible de consulter la plupart des [snippets de code
du Makefile](Makefile.snippet).


# Fonctionnalités à ajouter

De base
- [X] Proposition d'un pipeline standard de datascience
- [X] Execution unique en cas de rejeu de la règle make
- [X] Fonctionnement Conda
- [ ] Fonctionnement virtualenv
- [X] Offline (partiel)
- [ ] GPU
- [ ] Execution compatible avec le mode parallèle (-j)
- [ ] Extraction des métriques dans les différentes branches Git (à la [DVC](https://dvc.org/doc/commands-reference/metrics)

Datascience
- [X] [Jupyter](https://jupyter.org/)
- [X] [Tensorflow](https://www.tensorflow.org/)
- [ ] [Tensorflow template](https://github.com/Mrgemy95/Tensorflow-Project-Template)
- [X] [Spacy](https://spacy.io/) 
- [X] [NLTK](https://www.nltk.org/)
- [X] [pylint](https://www.pylint.org/) et [flake8](http://flake8.pycqa.org/)
- [X] [DVC](https://dvc.org/)
- [ ] [MLFlow](https://mlflow.org/) (alternative a DVC et exposition REST)
- [ ] [MLeap](http://mleap-docs.combust.ml/)
- [ ] [Pachyderm](https://www.pachyderm.io/open_source.html)

Explicabilité
- [ ] [Facet](https://pair-code.github.io/facets/)
- [ ] [Eli5](https://eli5.readthedocs.io/en/latest/overview.html)

Norme et qualité
- [X] Typing
- [ ] Typing at runtime ([Enforce](https://pypi.org/project/enforce/), [pydantic](https://pypi.org/project/pydantic/),
      ou [pytypes](https://pypi.org/project/pytypes/))
- [X] [PEP8](https://pep8.readthedocs.io/en/latest/)

Tests
- [X] [pytype](https://opensource.google.com/projects/pytype)
- [ ] [Runtime typechecking](https://github.com/agronholm/typeguard)
- [X] Test unitaires
- [X] Test unitaires du makefile produit par cookiecutter
- [X] [Pytest xdist](https://docs.pytest.org/en/3.0.0/xdist.html)
- [ ] [Pytest for jenkins](https://docs.pytest.org/en/latest/usage.html#creating-junitxml-format-files)
- [ ] [Plugin Pytest](https://pypi.org/search/?q=pytest)
- [ ] [Pytest open files](https://pypi.org/project/pytest-openfiles/)
- [ ] [Coverage](https://coverage.readthedocs.io/) et voir Sphinx coverage comment l'activer)
- [ ] [Cobertura](http://cobertura.github.io/cobertura/)
- [ ] [Test isolation](https://notes.farcellier.com/blog/20190315_ecrire_des_tests_isoles_avec_des_effets_de_bords_sur_le_filesystem_en_python/page.html)
- [ ] [Hypothesis](https://hypothesis.readthedocs.io/)
- [ ] [Pyramide des tests](https://blog.octo.com/la-pyramide-des-tests-par-la-pratique-1-5/)
- [ ] [Sonarcube](https://www.sonarqube.org/)
- [ ] [Behave](https://behave.readthedocs.io/en/latest/)
- [ ] [Retry](https://notes.farcellier.com/python/index.html#retrying)

Docs
- [X] Documentation et [Sphinx](http://www.sphinx-doc.org/)
- [ ] [ReadTheDoc](https://readthedocs.org/)
- [ ] [Upload sphinx](https://pythonhosted.org/an_example_pypi_project/setuptools.html#using-setup-py)
- [ ] Injecter les notebooks dans la documentation

Ressources
- [X] [LFS](https://git-lfs.github.com/)
- [ ] [Gitlab LFS](https://docs.gitlab.com/ce/workflow/lfs/lfs_administration.html#storing-lfs-objects-in-remote-object-storage)
- [ ] [Cloud storage](https://pypi.org/project/cloudstorage/)

CI/CD
- [X] Hook avant un `commit` sur la branche `master` de git
- [ ] [Jenkins](https://jenkins.io/)
- [ ] [Github Travis](https://notes.farcellier.com/travisci/index.html)
- [ ] Gitlab CI
- [ ] Docker pour le build/train
- [X] Docker pour le run

Cloud
- [X] AWS ([aws cli](https://aws.amazon.com/fr/cli/))
- [X] [ssh-ec2](https://gitlab.octo.com/pprados/ssh-ec2)
- [ ] [Amazon SageMaker](https://aws.amazon.com/fr/sagemaker/) direct ou via mlflow ou Sagemaker-compatible Docker container.
- [ ] [Aws NEO](https://aws.amazon.com/fr/sagemaker/neo/) pour optimmiser les modèles
- [ ] AWS lambda avec [Zappa](https://notes.farcellier.com/zappa/index.html) serverless compatible HTTP

Sécurité
- [ ] [Sops](https://pypi.org/project/sops/)
- [ ] [Secret AWS](https://drivendata.github.io/cookiecutter-data-science/#keep-secrets-and-configuration-out-of-version-control)

Pipeline
- [ ] [Airflow](https://airflow.apache.org/)
- [ ] [Prefect](https://www.prefect.io/)

Autres
- [X] Distribution et publication ([twine](https://pypi.org/project/twine/))
- [X] [PyInstaller](https://www.pyinstaller.org/)
- [ ] [Cython](https://cython.org/) et [tests](https://pypi.org/project/pytest-cython/)
- [X] [Hook git locaux](https://fr.atlassian.com/git/tutorials/git-hooks)
- [ ] [Koalas](https://databricks.com/blog/2019/04/24/koalas-easy-transition-from-pandas-to-apache-spark.html)
- [ ] [Prefect](https://www.prefect.io/)
- [ ] [Tox](https://tox.readthedocs.io/en/latest/)
- [ ] [Nox](https://nox.thea.codes/en/stable/)
- [ ] [DevPi](https://devpi.net/docs/devpi/devpi/stable/%2Bd/index.html)
- [ ] [Structured logs](https://github.com/FabienArcellier/spike_json_formatter_for_logging_python)
- [ ] Dans le code python, lecture depuis URI et non d'un fichier
- [ ] [Cloud Bridge](https://github.com/CloudVE/cloudbridge)
- [ ] [pysoniq](https://pysoniq.com)
- [ ] Spark
- [ ] [Spark+Array](https://spark.apache.org/docs/2.4.0/sql-pyspark-pandas-with-arrow.html#apache-arrow-in-spark)
- [ ] [Sécurité Bandit](https://pypi.org/project/bandit/)
- [ ] [Honcho](https://honcho.readthedocs.io/)
- [ ] [Snap](https://tutorials.ubuntu.com/tutorial/create-your-first-snap)