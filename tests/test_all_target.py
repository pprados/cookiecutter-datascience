import os
import subprocess

import pytest

# Use PARALLEL=True make ...
PARALLEL=os.getenv("PARALLEL","False").lower() in ("yes", "true")
MAKE_PARALLEL = os.getenv("MAKE_PARALLEL","-j -O" if PARALLEL else "")
PYTEST_PARALLEL=os.getenv("PYTEST_PARALLEL","-n 10" if PARALLEL else "")

# PPR
print("--------------------------------------------------------")
print("PARALLEL=",PARALLEL)
print("MAKE_PARALLEL=",MAKE_PARALLEL)
print("PYTEST_PARALLEL=",PYTEST_PARALLEL)
print("--------------------------------------------------------")

def _run_make_cmd(dirname: str, cmd: str):
    print(f"Execute '{cmd}'...")
    return subprocess.call(f"""
        set -e
        . "$(conda info --base)/etc/profile.d/conda.sh"
    	V=CC_temp_$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 10 | head -n 1)
	    D=/tmp/$V
    	conda create -n $V -y
	    conda activate $V
        export AWS_INSTANCE_TYPE=t2.small
        ln -f Makefile-TU {dirname}/bda_project/Makefile-TU
        cd "{dirname}/bda_project"
        {cmd}
        conda deactivate
        conda env remove -n $V
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

    # PPR assert 0 == _run_make_cmd(result.project.dirname, f"make {PYTEST_PARALLEL} make {MAKE_PARALLEL} -f Makefile-TU DEFAULT DOCS")
    assert 0 == _run_make_cmd(result.project.dirname,
                              f"PYTEST_PARALLEL=\"{PYTEST_PARALLEL}\" make {MAKE_PARALLEL} -f Makefile-TU DIST")


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

    assert 0 == _run_make_cmd(result.project.dirname,
                              f"PYTEST_PARALLEL=\"{PYTEST_PARALLEL}\" make {MAKE_PARALLEL} -f Makefile-TU AWS")


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

    assert 0 == _run_make_cmd(result.project.dirname,
                              f"PYTEST_PARALLEL=\"{PYTEST_PARALLEL}\" make {MAKE_PARALLEL} -f Makefile-TU JUPYTER")


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

    assert 0 == _run_make_cmd(result.project.dirname,
                              f"PYTEST_PARALLEL=\"{PYTEST_PARALLEL}\" make {MAKE_PARALLEL} -f Makefile-TU TEXT_PROCESSING")


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

    assert 0 == _run_make_cmd(result.project.dirname,
                              f"PYTEST_PARALLEL=\"{PYTEST_PARALLEL}\" make {MAKE_PARALLEL} -f Makefile-TU OPENSOURCE")

