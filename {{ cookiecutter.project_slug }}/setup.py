# -*- coding: utf-8 -*-
import os
import re
import subprocess
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

# USE_GPU="-gpu" ou "" si le PC possède une carte NVidia
# ou suivant la valeur de la variable d'environnement GPU (export GPU=yes)
USE_GPU = "-gpu" if (os.environ['GPU'].lower() in 'yes'
                     if "GPU" in os.environ
                     else os.path.isdir("/proc/driver/nvidia")
                          or "CUDA_PATH" in os.environ) else ""


# Package nécessaires à l'execution
requirements = [
    'click',
    'python-dotenv',
{% if cookiecutter.use_tensorflow == "y"      %}    'tensorflow' + USE_GPU + '~=1.3', # Ubuntu: sudo apt-get install cuda-libraries-10.0 {% endif %}
{% if cookiecutter.use_text_processing == "y" %}    'spacy~=2.0', {% endif %}
{% if cookiecutter.use_text_processing == "y" %}    'nltk~=3.3', {% endif %}
    'numpy~=1.14',
    'pandas~=0.22',
]

# Package nécessaires aux tests
test_requirements = [
    'pytest>=2.8.0',
    'pytest-cookies',
    'pytest-xdist',
    'pytest-httpbin==0.0.7',
    'unittest2',
    #'pytest-cov',
    'pytest-mock',
    #'pytest-xdist',
]

# Package nécessaires aux builds et tests mais pas au run
# FIXME Indiquer les dépendances nécessaire au build et au tests à ajuster suivant le projet
dev_requirements = [
    'twine',  # To publish package in Pypi
    'sphinx', 'sphinx-execute-code', 'sphinx_rtd_theme', 'm2r', 'nbsphinx',  # To generate doc
    'unittest2', 'mock', 'pytest', 'pytest-openfiles', # For tests
    'flake8', 'pylint',  # For lint
    'daff',
{% if cookiecutter.use_jupyter == "y" %}    'jupyter',  # Use Jupyter{% endif %}
{% if cookiecutter.use_DVC == "y"     %}    'dvc',  # Use DVC{% endif %}
{% if cookiecutter.use_aws == "y"     %}    'awscli',  # Use AWS{% endif %}
]


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

{#
# PPR: voir comment ajouter des params à python setup.py test pour les utiliser
# pour differencier les tests U et fonctionnel
# See https://github.com/kennethreitz/requests/blob/master/setup.py
# python setup.py --help-commands
class PyTest(TestCommand):
    user_options = TestCommand.user_options+[('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        super().initialize_options()
        try:
            from multiprocessing import cpu_count
            self.pytest_args = ['-n', str(cpu_count()), '--boxed']
        except (ImportError, NotImplementedError):
            self.pytest_args = ['-n', '1', '--boxed']

    def finalize_options(self):
        super().finalize_options()
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)
#}
setup(
    name='{{cookiecutter.project_slug}}' + USE_GPU,
    author="Octo Technology",
    author_email="bda@octo.com",
    description="{{cookiecutter.project_short_description}}",
    long_description=open('README.md', mode='r', encoding='utf-8').read(),
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
    python_requires='~={{ cookiecutter.python_version }}',  # Version de Python
    test_suite="tests",
    tests_require=test_requirements,
{#     #cmdclass={'test': PyTest}, #}
    extras_require={
        'dev': dev_requirements,
        },
    packages=find_packages(),
    # Pour utiliser Git pour extraire les numéros des versions
    use_scm_version=True,  # Gestion des versions à partir des commits Git
    setup_requires=["pytest-runner","setuptools_scm"],
    # TODO Indiquez les dépendances nécessaire à l'execution du composant, à ajuster suivant le projet
    install_requires=requirements,
)
