import pytest


@pytest.fixture
def context():
    """Test template creation with test parameters."""
    return {
        "project_name": "test_repo",
        "project_slug": "test_repo",
        "project_short_description": "Test",
        "repo_name": "test_repo"
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
    assert result.project.basename == 'test_repo'
    assert result.project.isdir()