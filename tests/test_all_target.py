import subprocess

import pytest

OPT = "" # PPR


def _run_make_cmd(dirname: str, cmd: str):
    print(f"Execute '{cmd}'...")
    return subprocess.call(f"""
        . "$(conda info --base)/etc/profile.d/conda.sh"
        conda activate bda_project
        export AWS_INSTANCE_TYPE=t2.small
        ln -f Makefile-TU {dirname}/bda_project/Makefile-TU
        set -x
        cd {dirname}/bda_project
        {cmd}
        """, shell=True)


@pytest.fixture
def context():
    """Test template creation with test parameters."""
    return {
        "project_name": "bda_project",
        "project_slug": "bda_project",
        "project_short_description": "Test",
    }


@pytest.mark.slow
def test_template_default_values(cookies, context):
    """Test the template for proper creation.

    cookies is a fixture provided by the pytest-cookies
    plugin. Its bake() method creates a temporary directory
    and installs the cookiecutter template into that directory.
    """
    result = cookies.bake(extra_context=context)
    # result.project.dirname
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == 'bda_project'
    assert result.project.isdir()

    # PPR assert 0 == _run_make_cmd(result.project.dirname, f"make {OPT} -f Makefile-TU DEFAULT DOCS")
    assert 0 == _run_make_cmd(result.project.dirname, f"make {OPT} -f Makefile-TU DIST")


@pytest.mark.slow
def test_template_with_aws_and_s3(cookies, context):
    """Test the template for proper creation.

    cookies is a fixture provided by the pytest-cookies
    plugin. Its bake() method creates a temporary directory
    and installs the cookiecutter template into that directory.
    """
    context = {**context, **{
        "open_source_software": "n",
        "use_jupyter": "n",
        "use_tensorflow": "n",
        "use_text_processing": "n",
        "use_git_LFS": "n",
        "use_aws": "y",
        "use_s3": "y",
        "use_DVC": "n",
        "add_makefile_comments": ""
    }
               }
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == 'bda_project'
    assert result.project.isdir()

    assert 0 == _run_make_cmd(result.project.dirname, f"make {OPT} -f Makefile-TU AWS")


@pytest.mark.slow
def test_template_with_jupyter(cookies, context):
    """Test the template for proper creation.

    cookies is a fixture provided by the pytest-cookies
    plugin. Its bake() method creates a temporary directory
    and installs the cookiecutter template into that directory.
    """
    context = {**context, **{
        "open_source_software": "n",
        "use_jupyter": "y",
        "use_tensorflow": "n",
        "use_text_processing": "n",
        "use_git_LFS": "n",
        "use_aws": "n",
        "use_s3": "n",
        "use_DVC": "n",
        "add_makefile_comments": ""
    }
               }
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == 'bda_project'
    assert result.project.isdir()

    assert 0 == _run_make_cmd(result.project.dirname, f"make {OPT} -f Makefile-TU JUPYTER")


@pytest.mark.slow
def test_template_with_text_processing(cookies, context):
    """Test the template for proper creation.

    cookies is a fixture provided by the pytest-cookies
    plugin. Its bake() method creates a temporary directory
    and installs the cookiecutter template into that directory.
    """
    context = {**context, **{
        "open_source_software": "n",
        "use_jupyter": "y",
        "use_tensorflow": "n",
        "use_text_processing": "y",
        "use_git_LFS": "n",
        "use_aws": "n",
        "use_s3": "n",
        "use_DVC": "n",
        "add_makefile_comments": ""
    }
               }
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == 'bda_project'
    assert result.project.isdir()

    assert 0 == _run_make_cmd(result.project.dirname, f"make {OPT} -f Makefile-TU TEXT_PROCESSING")


@pytest.mark.slow
def test_template_with_open_source(cookies, context):
    """Test the template for proper creation.

    cookies is a fixture provided by the pytest-cookies
    plugin. Its bake() method creates a temporary directory
    and installs the cookiecutter template into that directory.
    """
    context = {**context, **{
        "open_source_software": "y",
        "use_jupyter": "n",
        "use_tensorflow": "n",
        "use_text_processing": "n",
        "use_git_LFS": "n",
        "use_aws": "n",
        "use_s3": "n",
        "use_DVC": "n",
        "add_makefile_comments": ""
    }
               }
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == 'bda_project'
    assert result.project.isdir()

    assert 0 == _run_make_cmd(result.project.dirname, f"make {OPT} -f Makefile-TU OPENSOURCE")

