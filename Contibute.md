# Contribuer au projet

Le code est complexe, car il y a plein de langage de template imbriqué.

## Templating

Il y a d'abord cookiecutter qui utilise Jinja2 pour générer les fichiers lors la génération du projet. 
Pour cela, il faut utiliser des syntaxes du type `{{ … }}`.

Puis il y a le fichier `Makefile` qui utilise:
- `$(VAR)` pour remplacer le text d’un script par la valeur de la variable, vu du Makefile
Il faut donc doubler le $ lors d’une utilisation à l'intérieur d’un shell
- `$(shell cmd)` pour executer une commande dans le `Makfile`, et suivant les cas, 
la ré-executer à chaque fois, ou une seule fois.
    - `TOTO:=$(shell cmd)` # Exécuté une fois
    - `TOTO=$(shell cmd)` # Exécuté à chaque résolution de la variable.
Puis il y a les scripts bash produit par le `Makefile`, devant s’exécuter via bash. 
Ces scripts utilisent:
- `${VAR}` pour les variables (donc `$${VAR}` depuis une règle de `Makefile`)
- `$(cmd)` pour exécuter une commande dans le bash (donc `$$(cmd)` )

Avec de la rigueur, on s’en sort. Voici un exemple typique dans le Makefile à générer dans le projet:
```makefile
# Utilisation de variable du Makefile
PRJ:=$(shell basename $(shell pwd))
# Initialisation d’une variable, ssi elle n’est pas valorisé par une variable d’environnement
VENV ?= $(PRJ)
# Injection d’une variable via Jinja2
PYTHON_VERSION:={{ cookiecutter.python_version }}
```
Attention à vérifier qu'il y a bien une tabulation au début des règles de Makefile (utilisez un plugin PyCharm pour cela)

## Makefiles
La doc de [Gnu Makefile](https://www.gnu.org/software/make/manual/make.html).

Il y a plusieurs `Makefile`, à différents niveaux:
- Le `Makefile` à la racine du projet. Il est en charge de qualifier la génération des projets via Cookiecutter
- Le `Makefile` dans le répertoire `{{ cookiecutter.project_slug }}`. C’est le `Makefile` servabt à générer 
le projet créé par Cookiecutter
- Le `Makefile` dans les projets d’exemples, dans `examples/(classic|dvc)/*/Makefile`. 
Ce dernier est généré à partir du précédent, lors de la création du projet d’exemple, 
puis patché pour injecter les fichiers `exemples.template/*/Project_*.mak` suivant les cas

## Generation standard
Pour valider une génération de projet depuis cookiecutter, il faut invoquer une règle `try_*`. Par exemple,

`make try_jupyter`

Cela génère un projet dans `./try/<nom de la branche git>/bda_project`.

L’idéal est d’utiliser un autre shell pour s’y placer, activer l’env conda bda_project, et tester les règles
```bash
cd try/master/bda_project
conda activate bda_project
make evaluate
```
Il y a plusieurs scénario proposé (try, try_jupyter, try_text_processing, try_DVC, try_aws, try_opensource, try_default)

Le code racine propose des TU pour vérifier les différentes règles.
```
make test
```
Pour pousser les modifications sur la branche master, il faut vérifier le code via un `make validate`.

## Exemples
Pour générer les exemples, il faut invoquer, par exemple (Voir `Makefile` racine) :
```bash
rm -rf examples/classic/flower_classifier && make examples/classic/flower_classifier
```
dans le cas de la production d’un exemple en mode ‘classic’. Faire de même pour dvc.

Attention, si vous etiez dans ce répertoire, il faut probablement faire un 
```
cd ../flower_classifier
```
car le répertoire précédent n’existe plus, et bash est perdu.

Le répertoire `.../flower_classifier/flower_classifier` est un lien symbolique vers
`examples.template/flower_classifier/flower_classifier` pour que les modifications
soient appliquées lors des générations suivantes.

# Quelques justifications techniques

Les différents variables d'environnement peuvent être valorisés soit définitivement
pour la session shell:
```bash
export DEBUG=True
make train

```
soit uniquement une une commande `make`
```bash
DEBUG=True make train
```
Elles sont conçu pour pouvoir être surchargées avant l'invocation (opérateur `?=` de `make`)

| Quoi  | Pourquoi |
| :---: |:-------- | 
| VENV=_name_ | Cette variable permet d'utiliser un environnement conda existant. Par exemple, lors de l'utilisation d'une instance AWS par exemple.|
| DATA=_dir_ | Certaines technologies (SageMaker par exemple) imposent la localisation des datas. Il faut pouvoir la modifier. |
| DEBUG=True | Avant de lancer un tir, il peut être judicieux de tester avec des paramètres plus légers. |
| NPROC=_n_ | Permet de limiter le nb de traitement en parallèle (`NPROC=0 make ...` pour executer les TU en série) |
| OFFLINE=True | Pour éviter d'aller sur internet pour résourdre les dépendances |

# Reste à faire pour la version 1.0
- ajouter des TU à flower_classifier
- deverminer le code pour qu'il puisse apprendre (probablement un pb sur la normalisation des images)
- Verifier le typing de cet exemple
- Verifier le format des sources
- Ajouter un deuxieme exemple, basé sur predictive_failure
- Fixer les TODO de type PPR
- Fixer le NPROC (multiprocesseur du makefile)
- Voir le 'WARNING: Logging before flag parsing goes to stderr.'
- et probablement plein d'autres trucs