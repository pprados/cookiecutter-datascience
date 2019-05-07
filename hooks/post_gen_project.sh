#!/usr/bin/env bash
#rm DVC.mak
rm Classic.mak DVC.mak
{% if cookiecutter.use_jupyter == "n" %}
rm -Rf notebooks
{% endif %}
cat <<END
Read README.md file.

The project use:
- Python {{ cookiecutter.python_version }}
{% if cookiecutter.use_tensorflow == "y" %}- Tensorflow with or without GPU{% endif %}
{% if cookiecutter.use_text_processing == "y" %}- Text processing (NLTK and/or Spacy){% endif %}
{% if cookiecutter.use_aws == "y" %}- AWS and ssh-ec2{% endif %}
{% if cookiecutter.use_DVC == "y" %}- DVC to manage datas{% endif %}

Use can use:
- make prepare    # To prepare datas
- make feature    # To add features
- make train      # To train the model
- make evaluate   # To validate the model
- make visualize  # To validate
{% if cookiecutter.use_DVC == "y" %}- make repro      # To rebuild DVC dependencies{% endif %}

(update the python file in '{{ cookiecutter.project_slug }}' directory)
END
