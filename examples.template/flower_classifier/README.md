# Best practice
Ce projet est un exemple de bonne pratique, lors du développement de pipeline de machine learning.

Il respecte les règles suivantes:
- Clean architecture (le coeur du code n'a pas connaissance de l'environnement, 
ignore les fichiers, etc). Cela facilite l'intégration, la réorganisation du pipeline, les tests, etc.
- Chaque étape du pipeline peut être invoquée individuellement en ligne de commande.
C'est la méthode `main()` qui se charge de lier le _clean code_à l'environnement
- Le pipeline peut également être construit en intégralité et être exécuté uniquement en mémoire.
Cela permet d'économiser des ressources lors d'une exécution sur le cloud par exemple.
- Tous les méta-paramètres peuvent être valorisé via des paramètres de la ligne de commande
- Le code peut être lancé en local ou sur EC2 (via ssh-ec2)
- Le typage python est présent dans toutes les interfaces des fonctions et méthodes
- Par construction, le fichier `Makefile` évite d'avoir les situations du type :
"Si tu fais ceci, alors n'oublie pas de faire cela". Tous ce qui doit être fait est fait, uniquement
si c'est nécessaire. Par exemple, si le source préparation du dataset est modifié, il est appliqué à nouveau
avant un entrainement.
- toutes les dependences sont dans `setup.py`
- fonctionne automatiquement avec ou sans GPU
- Utilisez `make help` pour en savoir plus.

# TODO
- Faire les TU
- Verifier tous les règles (dont lint et typing)
- Download tgz en URL générique type s3 ? (http://code.activestate.com/recipes/578957-urllib-handler-for-amazon-s3-buckets/)

# Remarques générales:
- Tous les paramètres sont traités à l'aide d'annotation [`click`](https://click.palletsprojects.com/en/7.x/). 
Le type retourné par les anotations sont porteur de sens, 
- Il est alors possible d'invoquer les modèles avec `--help` pour en savoir plus
pour ne pas avoir à le traiter dans le core de la méthode.
- Dès que possible, le code utilise des `Generator` à la place de conteneur (`Map`, `List`), afin
d'économiser la mémoire (en ne gardant que ce qui est nécessaire à chaque instant).
Cela permet de les emboiter pour cumuler des traitements en mode _paresseux_(`Generator` lui même
alimenté par à un autre `Generator`). 
- Le code utilise toujours le type `Path` lorsque cela est pertinent (à la place de `str`). Cela
permet de manipuler plus facilement, avec moins de code, les noms des fichiers. Par exemple, pour
extraire la classe d'image, il suffit de `clazz = path.parts[-2:-1][0]`

`prepare_dataset.py`:
- Le fichier tgz d'origine, avec les images du dataset, est décompressé par le code. Il en profite 
pour modifier la taille des images à la dimension voulu pour l'apprentissage et retourne un `np.array`.
- Cela s'effecture via un `Generator` afin de ne monter en mémoire les images que lorsque cela est nécessaire,
et pouvoir également les supprimer de la mémoire lorsqu'elles ne sont plus utiles. 
- Le code de la fonction `main()` se charge alors de sauvegarder les images sur disque pour une utilisation
du pipeline "étape par étape"

`train_dataset.py`:
- Utilise une déclaration de type `tools.Model` pour produire le modèle. Ainsi, il est possible de modifier le
type de modèle à un seul endroit, pour que tous le code s'ajuste
- Le code de `main()` se charge d'initialiser les Generateur à partir des images sur disque,
et de sauvegarder le modèle et les domains.
- Le code utilise un pattern Glob pour sélectionner les fichiers images à utiliser, et ainsi, facilement
limiter leurs nombres lance du lancement du traitement. Par exemple, avec `data/processed/**/212*.jpg`.
C'est pratique lors des phases de mise au point.

`evaluate_model.py`:
- A partir d'une sélection de fichier (via un pattern Glob), du model entrainé et du domain,
le code qualifie les résultats et sauve les métriques dans un fichier .json. Ce dernier à vocation a être
ajouté à Git. Il représente le résultat du scénario.

`visualize.py`:
- A partir d'une sélection de fichier (via un pattern Glob), du model entrainé et du domain,
le code applique le modèle et affiche l'estimation.
- Un mode interatif permet d'afficher les images

`pipeline.py`:
- Ce code permet également un apprentissage, mais en partant directement du fichier `tgz` d'origine, tout
en mémoire. C'est potentiellement plus rapide (car il n'y a pas d'IO), moins exigeant en ressource sur une 
instance dans le cloud, et donc plus économique.

