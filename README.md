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

## Impact des différents options
Lors de la création d'un projet, des questions vous sont posées
pour identifier les caractèristiques du projet à créer.
Elles permettent d'alléger le project, en supprimant les règles
et les fichiers qui ne sont pas nécessaires.

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
- `make build-%` # Invoke all script in lexical order from scripts/<% dir> 
- `make lint` # Lint the code
- `make docs` # Create the HTML doc
- `make test` # Run all unit-tests
- `make validate` # Validate the version before commit
- `make clean` # Clean current environment
- `make sdist` # Create a source distribution
- `make bdist` # Create a binary wheel distribution

### use_jupyter
- un répertoire `notebooks/`
- une dépendance à jupyter dans `setup.py`
- des hooks à GIT pour nettoyer les notebooks lors des push/pull
- la gestion d'un kernel Jupyter dédié au projet
- `make remove-kernel` # Pour supprimer le kernel du projet
- `make nbbuild-%` # Pour executer tous les notebooks
- `make notebook` # pour gérer les dépendances
- `make nbconvert` # Pour convertir les notebooks en script pythons
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

