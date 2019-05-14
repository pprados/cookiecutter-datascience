# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from distutils.core import setup

setup(
    name='cookiecutter-bda',
    packages=[],
    # Pour utiliser Git pour extraire les numéros des versions
    use_scm_version=True,  # Gestion des versions à partir des commits Git
    setup_requires=['setuptools_scm'],
    description='Cookiecutter template for BDA',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    long_description_content_type='text/markdown',
    author='Philippe Prados',
    author_email='pprados@octo.com',
    license='Private',
    test_suite="tests",
    url='https://gitlab.octo.com/pprados/cookiecutter-bda',
    keywords=['cookiecutter', 'template', 'package', ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: Other/Proprietary License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
    ],
    extras_require={
        'tests':
            [
                'unittest2', 'mock',  # For unit tests
                'pytest', 'pytest-openfiles', 'pytest-cookies',
            ]
    },
    install_requires=
    [
        'cookiecutter',
    ],
)
