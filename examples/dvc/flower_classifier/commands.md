# Commands

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
* ``make test`` will run all unit-tests
* ``make typing`` will check the typing
* ``make add-typing`` will add annotation for typing
* ``make validate`` will validate the version before commit
* ``make clean`` will clean current environment

* ``make docs`` will create and show a HTML documentation in 'build/'
* ``make dist`` will create a full wheel distribution


* ``make ec2-notebook`` will start jupyter notebooks in EC2 instance (via `ssh-ec2 <https://gitlab.octo.com/pprados/ssh-ec2>`_)


## DVC commands
* ``make dvc-external-%`` will add a traking of modifications of external files
* ``make lock-%`` will lock a specific dvc file
* ``make metrics`` will print the DVC metrics


## AWS commands
* ``make sync_to_s3/data`` will send :file:`data/` to S3
* ``make sync_from_s3/data`` will pull :file:`data/` from S3
* ``make ec2-%`` will execute make rules in EC2 instance
* ``make ec2-tmux-%`` will execute make rules with Tmux in EC2 instance
* ``make ec2-detach-%`` will execute make rule and detach terminal



