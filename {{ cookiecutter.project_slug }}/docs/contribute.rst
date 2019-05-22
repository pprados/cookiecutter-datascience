.. index:: clone

Contribute
==========

Récupérez les sources

``$ git clone |giturl| {{cookiecutter.project_slug}}``

puis::

$ cd {{cookiecutter.project_slug}}
$ make configure
$ conda activate {{cookiecutter.project_slug}}
$ make docs

Principes d'organisation du projet
==================================
* Les traitements de Data sciences utilisent une approche à l'aide de fichiers, indiqués
  dans les paramètres de la ligne de commande. Cela permet:

  - d'executer plusieurs règles en parallèle dans le ``Makefile`` utilisant le même script (``make -j 4 ...``)
  - d'ajuster les noms des répertoires aux environements d'exécution (local, Docker, SageMaker, etc)
  - d'avoir des tests unitaires isolant chaque étape du pipeline

* Les meta-paramètres des algorithmes doivent également pouvoir être valorisé via des paramètres de la ligne
  de commande. Cela permet d'utiliser des outils d'optimisations des meta-paramètres.

* Les metrics doivent être sauvegardées dans un fichier ``.json`` et pushé sur GIT. Cela permet
  d'avoir une trace des différents scénarios dans différents tags ou branches, pour les comparer,
  comme le propose DVC par exemple.

* Un ``make validate`` est exécuter automatiquement avant un ``git push`` sur la branche ``master``.
  Il ne doit pas générer d'erreurs. Cela permet d'avoir un build incassable, en ne publiant
  que des commits validés.
  Il est possible de forcer tout de même le push avec ``FORCE=y git push``.

* Pour les fichiers de données, le modèle propose
  d'utiliser :

  - git classic si les fichiers ne sont pas trop gros. L'utilisation
    de `daff <https://paulfitz.github.io/daff/>`_ permet alors
    de gérer plus facilement les évolutions des fichiers CSV.
  - `git lfs <https://git-lfs.github.com/>`_ pour les gros fichiers,
    mais il faut avoir un serveur LFS disponible. C'est le cas pour Gitlab ou Github.
  - `DVC <https://dvc.org/>`_ pour une autre approche, avec backup sur le cloud
  - Un bucket S3 pour les données ``raw``. Dans ce cas, il faut ajouter ``data/raw/`` à ``.gitignore``.
    Une règle permet alors de télécharger des données depuis le bucket s3 si le développeur ne possède pas ce
    répertoire.

* Le modèle propose d'utiliser

  - un module pour ``{{cookiecutter.project_slug}}``
  - des scripts Python dans ``scripts/``
{% if cookiecutter.use_jupyter == "y" %}  - des scripts Jupyter dans ``notebooks/``{% endif %}

* Le code du projet doit être présent dans le package ``{{cookiecutter.project_slug}}``.
  Ils doivent être exécuté depuis le ``home`` du projet. Pour cela, une astuce consiste
  à forcer le home dans les templates Python de PyCharm. Ainsi, un run depuis un source
  fonctionne directement, sans manipulation.

* Pour gérer des scripts python autonome{% if cookiecutter.use_jupyter == "y" %} ou des notebooks{% endif %},
  il est proposé d'utiliser des sous-répertoires correspondant
  au différentes phases de projet (e.g. ``scripts/phase1/``{% if cookiecutter.use_jupyter == "y" %} ou ``notebooks/phase1/``{% endif %}).
  Dans ces répertoires, les scripts seront exécuté dans
  l'ordre lexicographique pour validation.

* La documentation est générée en ``html`` et ``latedpdf`` dans le répertoire ``build/``. Tous les autres format
  de Sphinx sont possible, via un ``make build/epub`` par exemple.

* La distribution du package est conforme aux usages sous Python, avec un package avec les sources
  et un package WHL.

* Le `typing <https://realpython.com/python-type-checking/>`_ est recommandé, avant d'améliorer la qualité du code et sa documentation

Recommandations
===============
* Utilisez un CHANGELOG basé sur `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
* Utilisez un format de version conforme à `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.
* faite toujours un `make validate` avant de commiter le code

