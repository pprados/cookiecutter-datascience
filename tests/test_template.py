import pytest



@pytest.fixture
def context():
    """Test template creation with test parameters."""
    return {
        "project_name": "bda_project",
        "project_slug": "bda_project",
        "project_short_description": "Test",
    }


def test_template(cookies, context):
    """Test the template for proper creation.

    cookies is a fixture provided by the pytest-cookies
    plugin. Its bake() method creates a temporary directory
    and installs the cookiecutter template into that directory.
    """
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == 'bda_project'
    assert result.project.isdir()


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
        "use_DVC": "n",
        "use_aws": "n",
        "add_makefile_comments": "n"
        }
    }
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == 'bda_project'
    assert result.project.isdir()

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
        "use_DVC": "y",
        "use_aws": "y",
        "add_makefile_comments": ""
        }
    }
    result = cookies.bake(extra_context=context)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == 'bda_project'
    assert result.project.isdir()
