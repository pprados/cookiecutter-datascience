import os

from setuptools import setup, find_packages

# USE_GPU="-gpu" ou "" si le PC possède une carte NVidia
# ou suivant la valeur de la variable d'environnement GPU (export GPU=yes)
USE_GPU = "-gpu" if (os.environ['GPU'].lower() in ('yes')
                     if "GPU" in os.environ
                     else os.path.isdir("/proc/driver/nvidia")
                          or "CUDA_PATH" in os.environ) else ""
setup(
    name='{{cookiecutter.project_slug}}' + USE_GPU,
    author="Octo Technology",
    use_scm_version=True,       # Gestion des versions à partir des commits Git
    python_requires='~=3.6',    # Version de Python
    packages=find_packages(),
    # Pour utiliser Git pour gérer les versions
    setup_requires=['setuptools_scm'],
    # Package nécessaires aux builds et tests mais pas au run
    extras_require={
        'tests': # FIXME Les des dépendances à ajuster suivant le projet
            ['mock',
             'unittest2',
             'daff',
             'awscli',
             'flake8',
             ]
    },
    # Exemples de packages nécessaires au run
    install_requires= # FIXME Les des dépendances à ajuster suivant le projet
    [
        'click',
        'python-dotenv',
        # Exemple avec une alternative GPU
        'tensorflow' + USE_GPU + '~=0.5',
        {% if cookiecutter.use_jupyter == "y" %}
        'jupyter~=1.0',  # Ouvre les add-on Jupyter
        {% endif %}
        'numpy~=1.14',
        'pandas~=0.22',
        'plotly~=2.7',
        'scikit-learn~=0.19',
        {% if cookiecutter.use_Spacy == "y" %}
        'spacy~=2.0',
        {% endif %}
        {% if cookiecutter.use_NLTK == "y" %}
        'nltk~=3.3',
        {% endif %}
    ],
    # test_suite="tests",
    classifiers = [
                  'Development Status :: 4 - Beta',
                  'Environment :: Console',
                  'Intended Audience :: Developers',
                  'Natural Language :: English',
                  'Programming Language :: Python :: {{ cookiecutter.python_version }}',
                  'Topic :: Software Development',
              ],
)
