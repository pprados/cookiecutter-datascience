# -*- coding: utf-8 -*-
import os
import re
import subprocess

from setuptools import setup, find_packages

# USE_GPU="-gpu" ou "" si le PC possède une carte NVidia
# ou suivant la valeur de la variable d'environnement GPU (export GPU=yes)
USE_GPU = "-gpu" if (os.environ['GPU'].lower() in 'yes'
                     if "GPU" in os.environ
                     else os.path.isdir("/proc/driver/nvidia")
                          or "CUDA_PATH" in os.environ) else ""

def _git_url():
    try:
        with open(os.devnull, "wb") as devnull:
            out = subprocess.check_output(
                ["git", "remote", "get-url", "origin"],
                cwd=".",
                universal_newlines=True,
                stderr=devnull,
            )
        return out.strip()
    except subprocess.CalledProcessError:
        # git returned error, we are not in a git repo
        return ""
    except OSError:
        # git command not found, probably
        return ""


def _git_http_url():
    return re.sub(r".*@(.*):(.*).git", r"http://\1/\2", _git_url())


setup(
    name='{{cookiecutter.project_slug}}' + USE_GPU,
    author="Octo Technology",
    author_email="bda@octo.com",
    description="{{cookiecutter.project_short_description}}",
    # PPR bug sur ssh-ec2. A cause de l'UTF8 ?
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    long_description_content_type='text/markdown',
    url=_git_http_url(),

    license={% if cookiecutter.open_source_software == 'y' %}'Apache License'{% else %}'Private usage'{% endif %},
    keywords= "data science",
    classifiers=[  # See https://pypi.org/classifiers/
        'Development Status :: 2 - PRE-ALPHA',
        # Before release
        # 'Development Status :: 5 - Production/Stable'
        'Environment :: Console',
        'Intended Audience :: Developers',
        {% if cookiecutter.open_source_software == 'y' %}'License :: OSI Approved'{% else %}'License :: Other/Proprietary License'{% endif %},
        'Natural Language :: English',
        'Programming Language :: Python :: {{ cookiecutter.python_version }}',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    test_suite="tests",

    python_requires='~={{ cookiecutter.python_version }}',  # Version de Python
    packages=find_packages(),
    # Pour utiliser Git pour extraire les numéros des versions
    use_scm_version=True,  # Gestion des versions à partir des commits Git
    setup_requires=['setuptools_scm'],
    # Package nécessaires aux builds et tests mais pas au run
    extras_require={
        # FIXME Indiquer les dépendances nécessaire au build et au tests à ajuster suivant le projet
        'dev':
            [
                'twine',  # For publish package in Pypi
                'sphinx', 'sphinx-execute-code', 'sphinx_rtd_theme', 'm2r', 'nbsphinx',  # For generate doc
                'unittest2', 'mock',  # For unit tests
                'pytest', 'pytest-openfiles',
                'flake8', 'pylint',  # For lint
                'daff',
{% if cookiecutter.use_jupyter == "y" %}                'jupyter',  # Ouvre les add-on Jupyter{% endif %}
{% if cookiecutter.use_DVC == "y"     %}                'dvc',  # Utilise DVC{% endif %}
{% if cookiecutter.use_aws == "y"     %}                'awscli',  # Utilise AWS{% endif %}
            ]
        },
    # TODO Indiquez les dépendances nécessaire à l'execution du composant, à ajuster suivant le projet
    install_requires=
    [
        'click',
        'python-dotenv',
{% if cookiecutter.use_tensorflow == "y"      %}        'tensorflow' + USE_GPU + '~=0.5', {% endif %}        # PPR: Bug a l'usage
{% if cookiecutter.use_text_processing == "y" %}        'spacy~=2.0', {% endif %}
{% if cookiecutter.use_text_processing == "y" %}        'nltk~=3.3', {% endif %}
        'numpy~=1.14',
        'pandas~=0.22',
    ],
)
