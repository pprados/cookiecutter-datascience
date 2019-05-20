.. index:: clone

Contribute
==========

First, get the source code:

``$ git clone |giturl| {{cookiecutter.project_slug}}``

then::

$ cd {{cookiecutter.project_slug}}
$ make configure
$ conda activate {{cookiecutter.project_slug}}
$ make evaluate
$ make help

Principes
=========
* Les traitements de Data sciences utilisent une approche à l'aide de fichiers, indiqués
dans les paramètres de la ligne de commande. Cela permet:
- d'avoir plusieurs règles en parallèle dans le Makefile utilisant le même script
- d'ajuster les noms des répertoires aux environements d'exécution (local, Docker, SageMaker, etc)

* Les meta-données doivent également pouvoir être valorisé via des paramètres de la ligne
de commande. Cela permet d'utiliser des outils de recherche de meta-paramètres

* Les metrics doivent être sauvegardées dans un fichier .json et pushé sur GIT. Cela permet
d'avoir une trace des différents scénarios pour les comparer, comme le propose DVC par exemple.

* Un 'make validate' ne doit pas générer d'erreurs avant un ``git push``. Cela permet d'avoir un
build incassable. Il est possible de forcer tout de même le push avec ``FORCE=y git push``.

* Pour les fichiers de données, le modèle propose d'utiliser :
- git classic si les fichiers ne sont pas trop gros. L'utilisation de daff permet alors
de gérer plus facilement les évolutions des fichiers CSV.
- git lfs pour les gros fichiers, mais il faut avoir un serveur LFS disponible. C'est le cas pour Gitlab ou Github.
- DVC pour une autre approche, avec backup sur le cloud

* La documentation est générée en html et pdf dans le répertoire ``build/``. Tous les autres format
de Sphinx sont possible, via un ``make build/epub`` par exemple.

