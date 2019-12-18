#!/usr/bin/env bash
# ----------- Manage colors
if test -t 1; then

    # see if it supports colors...
    ncolors=$(tput colors)

    if test -n "$ncolors" && test $ncolors -ge 8; then
        normal="$(tput sgr0)"
        red="$(tput setaf 1)"
        green="$(tput setaf 2)"
        yellow="$(tput setaf 3)"
        gray="$(tput setaf 8)"
    fi
fi

rm Classic.mak DVC.mak
{% if cookiecutter.use_jupyter == "n" %}
rm -Rf notebooks
{% endif %}
{% if cookiecutter.use_s3 == "n" %}
rm data/raw/.gitignore
{% else %}
rm data/raw/.gitkeep
{% endif %}

ln -s ../README.md docs/README.md
ln -s ../CHANGELOG.md docs/CHANGELOG.md
ln -s ../commands.md docs/commands.md

cat <<END
Read README.md file.

The project {% if cookiecutter.open_source_software == "y" %}is open source and {% endif %}use:
- Python {{ cookiecutter.python_version }}{% if cookiecutter.use_tensorflow == "y" %}
- Tensorflow with or without GPU{% endif %}{% if cookiecutter.use_text_processing == "y" %}
- Text processing (NLTK and/or Spacy){% endif %}{% if cookiecutter.use_aws == "y" %}
- AWS and ssh-ec2{% endif %}{% if cookiecutter.use_DVC == "y" %}
- DVC to manage datas{% endif %}

Use can use:
- ${yellow}make prepare${normal}    # To prepare datas
- ${yellow}make feature${normal}    # To add features
- ${yellow}make train${normal}      # To train the model
- ${yellow}make evaluate${normal}   # To validate the model
- ${yellow}make visualize${normal}  # To visualize the results{% if cookiecutter.use_DVC == "y" %}
{# PPR - ${yellow}make repro${normal}      # To rebuild DVC dependencies #}{% endif %}

Now, check if the make version is 4+:
$ ${green}make -v${normal}
and
$ ${green}cd {{ cookiecutter.project_slug }} && make configure${normal}
END
