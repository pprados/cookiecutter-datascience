# Cookiecutter BDA

Un [modèle](https://gitlab.octo.com/pprados/cookiecutter-bda) raisonable de bootstrap de projet pour BDA.

## Pré-requis pour utiliser le modèle cookiecutter :
 - [Cookiecutter Python package](http://cookiecutter.readthedocs.org/en/latest/installation.html) >= 1.4.0: This can be installed with pip by or conda depending on how you manage your Python packages:

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
    cookiecutter https://gitlab.octo.com/pprados/cookiecutter-bda.git
```
et répondez aux questions.

## Principe des projects
- Les projets utilisent un environnement conda pour isoler les dépendances
- Elles doivent être déclarées dans `setup.py`
- Le numéro de version du projet est géré automatiquement via GIT et les labels
- Le Makefile doit pouvoir s'exécuter sur plusieurs processeurs (`make -j -O ...`)

## Impact des différentes options
Lors de la création d'un projet, des questions vous sont posées
pour identifier les caractèristiques du projet à créer.
Elles permettent d'alléger le project, en supprimant les règles
et les fichiers qui ne sont pas nécessaires.
Pour simplifier l'aide, toutes ne sont pas indiquées dans `make help`.
Il suffit de doubler le `#` du commentaire avant la règle pour modifier cela.

### Présent quelque soit les options

Pour le pipeline de data-science
- `make prepare` # Prepare the dataset
- `make features` # Add features
- `make train` # Train the model
- `make evaluate` # Evalutate the model 
- `make visualize` # Visualize the result

Et le reste, pour la gestion du projet
- `make help` # Print all majors target
- `make configure`  # Prepare the environment (conda venv, kernel, ...)
- `make run-%` # Invoke all script in lexical order from scripts/<% dir> 
- `make build/%` # Create sphinx documentation with % format (make build/html)
- `make lint` # Lint the code
- `make docs` # Create and show the HTML and PDF doc in 'build/'
- `make test` # Run all unit-tests
- `make validate` # Validate the version before commit
- `make clean` # Clean current environment
- `make sdist` # Create a source distribution
- `make bdist` # Create a binary wheel distribution
- `make dist` # Create a binary and source distribution

### use_jupyter
- un répertoire `notebooks/`
- une dépendance à jupyter dans `setup.py`
- des hooks à GIT pour nettoyer les notebooks lors des push/pull
- la gestion d'un kernel Jupyter dédié au projet
- `make remove-kernel` # Pour supprimer le kernel du projet
- `make nb-run-%` # Pour executer tous les notebooks
- `make notebook` # pour gérer les dépendances
- `make nb-convert` # Pour convertir les notebooks en script pythons
- `make clean-notebooks` # Pour nettoyer les données dans les notebooks
- `make ec2-notebook` # Si AWS, pour lancer un notebook sur une instance EC2 (via [ssh-ec2](https://gitlab.octo.com/pprados/ssh-ec2))
 
### use_tensorflow
- une dépendance à Tensorflow, avec ou sans GPU suivant la plateforme

### use_text_processing
- une dépendance à [Spacy](https://spacy.io/) et [NLTK](https://www.nltk.org/)
- des règles pour gérer les bases de données associées via les variables 
`NLTK_DATABASE` et `SPACY_DATABASE` dans le `Makefile`
 
### use_git_LFS
- ajout de l'installation des hooks LFS dans le projet si possible
- ajout des tracks de fichiers standards (.pkl, *.bin, *.jpg, *.jpeg, *.git, *.png)

### use_[DVC](https://dvc.org/)
- modification dès règles du pipeline du projet, pour exploiter `dvc run`
- ajout d'une variable `DVC_BUCKET` pour indiquer où localiser les données
- `make dvc-external-%` # Pour ajouter un suivit des modifications de fichier externe
- `make lock-%` # Pour bloquer le rebuild d'un fichier DVC
- `make metrics` # Pour afficher les métriques de DVC

### use_aws (utilisation de [ssh-ec2](https://gitlab.octo.com/pprados/ssh-ec2))
- une dépendance à `awscli` et `boto3`
- une variable `S3_BUCKET` pour le bucket du projet
- `make sync_data_to_s3` # Pour envoyer une copie des `data/\ vers S3
- `make sync_data_from_s3` # Pour récupérer une copie des `data/` depuis S3
- `make ec2-%` # Pour executer une règle via `ssh-ec2`
- `make ec2-tmux-%` # Pour executer une règle via `ssh-ec2` en mode tmux
- `make ec2-detach-%` # Pour détacher une règle sur une instance EC2

### open_source_software
- Modification des licenses dans `setup.py`
- `make check-twine` # Pour tester le packaging avant publication
- `make test-twine` # Pour tester la publication du package sur [test.pypi.org]((http://test.pypi.org))
- `make twine` # Pour publier la version du package sur [pypi.org](http://pypi.org)

### add_makefile_comments
- Ajout des commentaires "verbeux" dans le `Makefile`

## Snippet de Makefile
Il est également possible de consulter la plupart des [snippets de code
du Makefile](Makefile.snippet).

# Conseils
- Utilisez un CHANGELOG basé sur [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
- Utilisez un format de version conforme à [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
- faite toujours un `make validate` avant de commiter le code

# TODO
- [X] Pipeline datascience
- [X] Test unitaires
- [X] [Jupyter](https://jupyter.org/)
- [X] Distribution et publication ([twine](https://pypi.org/project/twine/))
- [X] [Tensorflow](https://www.tensorflow.org/)
- [X] [Spacy](https://spacy.io/) et [NLTK](https://www.nltk.org/)
- [X] [pylint](https://www.pylint.org/) et [flake8](http://flake8.pycqa.org/)
- [X] AWS ([aws cli](https://aws.amazon.com/fr/cli/))
- [X] [ssh-ec2](https://gitlab.octo.com/pprados/ssh-ec2)
- [X] [LFS](https://git-lfs.github.com/)
- [X] [DVC](https://dvc.org/)
- [ ] [MLFlow](https://mlflow.org/) (alternative a DVC))
- [X] Documentation et [Sphinx](http://www.sphinx-doc.org/)
- [ ] [Coverage](https://coverage.readthedocs.io/)
- [ ] [Hypothesis](https://hypothesis.readthedocs.io/)
- [ ] [Airflow](https://airflow.apache.org/)
- [ ] Injecter les notebooks dans la documentation
- [ ] Gestion plusieurs fichiers datas en parallèles
- [ ] [Amazon SageMaker](https://aws.amazon.com/fr/sagemaker/)
- [X] TU du makefile
- [ ] [Plugin](https://pypi.org/search/?q=pytest) pytest
- [ ] [Cython](https://cython.org/) et [tests](https://pypi.org/project/pytest-cython/)
- [ ] [Aws NEO](https://aws.amazon.com/fr/sagemaker/neo/) pour optimmiser les modèles
- [ ] Execution parfaite en rejeu
- [ ] Execution parfaite en parallèle (-j)
- [ ] [Hook git locaux](https://fr.atlassian.com/git/tutorials/git-hooks)
- [ ] [Koalas](https://databricks.com/blog/2019/04/24/koalas-easy-transition-from-pandas-to-apache-spark.html)
- [ ] [Prefect](https://www.prefect.io/)