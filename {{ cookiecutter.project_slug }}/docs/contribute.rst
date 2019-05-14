.. index:: clone

Contribute
==========

First, get the source code:

``$ git clone |giturl| {{cookiecutter.repo_name}}``

then::

$ cd {{cookiecutter.repo_name}}
$ make configure
$ conda activate {{cookiecutter.repo_name}}
$ make evaluate
$ make help
