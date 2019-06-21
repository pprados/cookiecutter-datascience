import sys
from typing import List

import click
from cookiecutter.main import cookiecutter


def try_cookiecutter(params: List[str], output_dir: str = "tmp") -> str:
    # All default value to false
    options = {
        "project_name": "BDA Project",
        "project_slug": "bda_project",
        "project_short_description": "Description of the project",
        "open_source_software": "n",
        "author": "OCTO Technology",
        "python_version": "3.6",
        "use_jupyter": "n",
        "use_tensorflow": "n",
        "use_text_processing": "n",
        "use_git_LFS": "n",
        "use_aws": "n",
        "use_s3": "n",
        "use_DVC": "n",
        "add_makefile_comments": "y"
    }
    options.update(dict(s.split('=', 1) for s in params))
    return cookiecutter(
        template=".",
        no_input=True,
        overwrite_if_exists=True,
        extra_context=options,
        output_dir=output_dir,
        # config_file="."
    )


@click.command()
@click.option('--output_dir', default="tmp", type=click.Path(exists=True))
@click.argument('params', nargs=-1, type=str)
def main(output_dir: str, params: List[str]):
    """ Apply cookiecutter with specific extra parameters

        :param output_dir: Output directory (default "tmp")
        :param params: List of key=vals
        :return: 0 if ok, else error
    """
    try:
        try_cookiecutter(params, output_dir)
    except SystemExit as e:
        return e.code
    except Exception as e:
        return -1


if __name__ == "__main__":
    sys.exit(main())