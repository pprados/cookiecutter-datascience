import os

import pytest

# See https://github.com/hackebrot/pytest-cookies

@pytest.fixture
def context():
    """Test template creation with test parameters."""
    return {
        "project_name": "bda_project",
        "project_slug": "bda_project",
        "project_short_description": "Test",
    }


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

    os.system(f"""
        cd {result.project.dirname}/bda_project ; 
        make validate
        """)


def test_template_with_all_no(cookies, context):
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
        "use_aws": "n",
        "use_s3": "n",
        "use_DVC": "n",
        "add_makefile_comments": "n"
        }
    }
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == 'bda_project'
    assert result.project.isdir()

    os.system(f"""
        cd {result.project.dirname}/bda_project ; 
        make validate ;
        make train
        """)

def test_template_with_all_yes(cookies, context):
    """Test the template for proper creation.

    cookies is a fixture provided by the pytest-cookies
    plugin. Its bake() method creates a temporary directory
    and installs the cookiecutter template into that directory.
    """
    context = {**context, **{
        "open_source_software": "y",
        "use_jupyter": "y",
        "use_tensorflow": "y",
        "use_text_processing": "y",
        "use_git_LFS": "y",
        "use_aws": "y",
        "use_s3": "y",
        "use_DVC": "y",
        "add_makefile_comments": ""
        }
    }
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == 'bda_project'
    assert result.project.isdir()

    os.system(f"""
        cd {result.project.dirname}/bda_project ; 
        make validate
        """)

def test_template_with_s3(cookies, context):
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

    os.system(f"""
        rm -Rf {result.project.dirname}/bda_project/data/raw
        cd {result.project.dirname}/bda_project ; 
        make train
        """)

# PPR
# def test_template_with_dvc(cookies, context):
#     """Test the template for proper creation.
#
#     cookies is a fixture provided by the pytest-cookies
#     plugin. Its bake() method creates a temporary directory
#     and installs the cookiecutter template into that directory.
#     """
#     context = {**context, **{
#         "open_source_software": "n",
#         "use_jupyter": "n",
#         "use_tensorflow": "n",
#         "use_text_processing": "n",
#         "use_git_LFS": "n",
#         "use_aws": "n",
#         "use_s3": "n",
#         "use_DVC": "y",
#         "add_makefile_comments": ""
#         }
#     }
#     result = cookies.bake(extra_context=context)
#
#     assert result.exit_code == 0
#     assert result.exception is None
#     assert result.project.basename == 'bda_project'
#     assert result.project.isdir()
#
#     os.system(f"""
#         cd {result.project.dirname}/bda_project ;
#         make validate ;
#         make train
#         """)
