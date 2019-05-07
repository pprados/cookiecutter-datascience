import os

from setuptools import setup, find_packages

# USE_GPU="-gpu" ou "" si le PC possède une carte NVidia
# ou suivant la valeur de la variable d'environnement GPU (export GPU=yes)
USE_GPU = "-gpu" if (os.environ['GPU'].lower() in 'yes'
                     if "GPU" in os.environ
                     else os.path.isdir("/proc/driver/nvidia")
                          or "CUDA_PATH" in os.environ) else ""
setup(
    name='{{cookiecutter.project_slug}}' + USE_GPU,
    author="Octo Technology",
    python_requires='~={{ cookiecutter.python_version }}',  # Version de Python
    packages=find_packages(),
    # Pour utiliser Git pour extraire les numéros des versions
    use_scm_version=True,  # Gestion des versions à partir des commits Git
    setup_requires=['setuptools_scm'],
    # Package nécessaires aux builds et tests mais pas au run
    extras_require={
        # FIXME Indiquer les dépendances nécessaire au build et au tests à ajuster suivant le projet
        'tests':
            [
                'unittest2', 'mock',  # For unit tests
                'flake8', 'pylint',  # For lint
                'daff',
{% if cookiecutter.use_jupyter == "y" %}                'jupyter~=1.0',  # Ouvre les add-on Jupyter{% endif %}
{% if cookiecutter.use_DVC == "y"     %}                'dvc',  # Utilise DVC{% endif %}
{% if cookiecutter.use_aws == "y"     %}                'awscli',  # Utilise AWS{% endif %}
            ]
        },
    # TODO Indiquer les dépendances à ajuster suivant le projet
    install_requires =
    [
        'click',
        'python-dotenv',
{% if cookiecutter.use_tensorflow == "y"      %}       'tensorflow' + USE_GPU + '~=0.5', {% endif %}
{% if cookiecutter.use_text_processing == "y" %}       'spacy~=2.0', {% endif %}
{% if cookiecutter.use_text_processing == "y" %}       'nltk~=3.3', {% endif %}
        'numpy~=1.14',
        'pandas~=0.22',
        'plotly~=2.7',
        'scikit-learn~=0.19',
    ],
    # test_suite="tests",
    classifiers = [
                  'Development Status :: 4 - Beta',
                  'Environment :: Console',
                  'Intended Audience :: Developers',
                  'Natural Language :: English',
                  'Programming Language :: Python :: {{ cookiecutter.python_version }}',
                  'Topic :: Machine Learning',
              ],
)
