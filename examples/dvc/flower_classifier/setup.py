# -*- coding: utf-8 -*-
import os
import re
import subprocess
from typing import List

from setuptools import setup, find_packages

# USE_GPU="-gpu" ou "" si le PC possède une carte NVidia
# ou suivant la valeur de la variable d'environnement GPU (export GPU=yes)
USE_GPU: str = "-gpu" if (os.environ['GPU'].lower() in 'yes'
                     if "GPU" in os.environ
                     else os.path.isdir("/proc/driver/nvidia")
                          or "CUDA_PATH" in os.environ) else ""


# Package nécessaires à l'execution
# FIXME Ajoutez et ajustez les dépendences nécessaire à l'exécution.
requirements: List[str] = [
    'matplotlib',
    'Pillow',
    'click', 'click-pathlib',
    'python-dotenv',
    'sklearn',
    'tensorflow' + USE_GPU + '~=1.3', # Ubuntu: sudo apt-get install cuda-libraries-10.0
    'keras',
    'appdirs', 
    'numpy~=1.14',
    'pandas~=0.22',
]

setup_requirements: List[str] = ["pytest-runner","setuptools_scm"]

# Package nécessaires aux tests
test_requirements: List[str] = [
    'pytest>=2.8.0',
    'pytest-openfiles', # For tests
    'pytest-xdist',
    'pytest-httpbin==0.0.7',
    'pytest-mock',
    
    'unittest2',
]

# Package nécessaires aux builds mais pas au run
# FIXME Ajoutez les dépendances nécessaire au build et au tests à ajuster suivant le projet
dev_requirements: List[str] = [
    'pip',
    # PPR necessaire a mlflow ? 'conda',
    'twine',  # To publish package in Pypi
    'sphinx', 'sphinx-execute-code', 'sphinx_rtd_theme', 'm2r', 'nbsphinx',  # To generate doc
    'flake8', 'pylint',  # For lint
    'daff',
    'pytype',

    'dvc', 'boto3', # Use DVC
    'awscli',  # Use AWS
    'tensorboard',  # Use tensorflow
]


# Return git remote url
def _git_url() -> str:
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


# Return Git remote in HTTP form
def _git_http_url() -> str:
    return re.sub(r".*@(.*):(.*).git", r"http://\1/\2", _git_url())

setup(
    name='flower_classifier' + USE_GPU,
    author="Octo Technology",
    author_email="bda@octo.com",
    description="Description of the project",
    long_description=open('README.md', mode='r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url=_git_http_url(),

    license='Private usage',
    keywords= "data science",
    classifiers=[  # See https://pypi.org/classifiers/
        'Development Status :: 2 - PRE-ALPHA',
        # Before release
        # 'Development Status :: 5 - Production/Stable'
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    python_requires='~=3.6',  # Version de Python
    test_suite="tests",
    setup_requires=setup_requirements,
    tests_require=test_requirements,
    extras_require={
        'dev': dev_requirements,
        'test': test_requirements,
        },
    packages=find_packages(),
    use_scm_version=True,  # Gestion des versions à partir des tags Git
    install_requires=requirements,
)
