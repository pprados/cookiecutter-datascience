# Make commands

The Makefile contains the central entry points for common tasks related to this project.

## Build machine learning
* ``make prepare`` will prepare the dataset
* ``make features`` will add some features
* ``make train`` will train the model
* ``make evaluate`` will evaluate the model
* ``make visualize`` will visualize the result

## Others commands
* ``make help`` will print all majors target
* ``make configure``  will prepare the environment (conda venv, kernel, ...)
* ``make run-%`` will invoke all script in lexical order from scripts/<% dir>
* ``make lint`` will lint the code
* ``make test`` will run all tests
* ``make typing`` will check the typing
* ``make validate`` will validate the version before commit
* ``make clean`` will clean current environment

* ``make docs`` will create and show a HTML documentation in 'build/'
* ``make dist`` will create a full wheel distribution
* ``make installer`` will create a standalone executable for this OS
{% if cookiecutter.use_jupyter == 'y' %}
## Jupyter commands
* ``make notebook`` will start a jupyter notebook
* ``make remove-kernel`` will remove the project's kernel
* ``make nb-run-%`` will execute all notebooks
* ``make nb-convert`` will convert all notebooks to python
* ``make clean-notebooks`` will clean all datas in the notebooks
{% endif %}{% if cookiecutter.use_aws == 'y' %}
* ``make ec2-notebook`` will start jupyter notebooks in EC2 instance (via `ssh-ec2 <https://gitlab.octo.com/pprados/ssh-ec2>`_)
{% endif %}{% if cookiecutter.use_DVC == 'y' %}
## DVC commands
* ``make dvc-external-%`` will add a traking of modifications of external files
* ``make lock-%`` will lock a specific dvc file
* ``make metrics`` will print the DVC metrics
{% endif %}{% if cookiecutter.use_aws == 'y' %}
## AWS commands
* ``make sync_to_s3/data`` will send :file:`data/` to S3
* ``make sync_from_s3/data`` will pull :file:`data/` from S3
* ``make ec2-%`` will execute make rules in EC2 instance
* ``make ec2-tmux-%`` will execute make rules with Tmux in EC2 instance
* ``make ec2-detach-%`` will execute make rule and detach terminal
{% endif %}{% if cookiecutter.open_source_software == 'y' %}
## Twine commands
* ``make check-twine`` will check the packaging before publication
* ``make test-twine`` will publish the package in `test.pypi.org <https://test.pypi.org>`_)
* ``make twine`` will publish the package in `pypi.org <https://pypi.org>`_)
{% endif %}{% if cookiecutter.use_docker == 'y' %}
## Docker commands
* ``make docker-build`` will build the Dockerfile and container
* ``make docker-run`` will start the container in background and attach the console
* ``make docker-start`` will start the container in background
* ``make docker-stop`` will stop the container
* ``make docker-attach`` will attach the console to the container
* ``make docker-bash`` will attach a shell in the container

* ``make docker-make-image`` create an image to build the project inside a container
* ``make docker-make-shell`` start a shell inside a container to build the project
* ``make docker-make-clean`` remove the docker image for build the project
{% endif %}
