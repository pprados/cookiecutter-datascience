# -*- coding: utf-8 -*-
{% if cookiecutter.add_makefile_comments == 'y' %}#
# testcutter documentation build configuration file, created by
# sphinx-quickstart.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.
{% endif %}
import os
import re
import subprocess
import sys


def _git_url():
    try:
        with open(os.devnull, "wb") as devnull:
            out = subprocess.check_output(
                ["git", "remote", "get-url","origin"],
                cwd=".",
                universal_newlines=True,
                stderr=devnull,
            )
        return out.strip()
    except subprocess.CalledProcessError:
        # git returned error, we are not in a git repo
        return "TODO"
    except OSError:
        # git command not found, probably
        return "TODO"

# For git clone ...
git_url=_git_url()
# Project home
home_url=re.sub(r".*@(.*):(.*).git", r"http://\1/\2", _git_url())

{% if cookiecutter.add_makefile_comments == 'y' %}# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.{% endif %}
sys.path.insert(0, os.path.abspath('..'))
{% if cookiecutter.add_makefile_comments == 'y' %}
# -- General configuration -----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.{% endif %}
extensions = [
    'sphinx.ext.autodoc',
    # 'sphinx.ext.coverage',
    'sphinx.ext.githubpages',
    'sphinx.ext.ifconfig',
    'sphinx.ext.mathjax',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    {% if cookiecutter.use_jupyter == 'y' %}'nbsphinx',{% endif %}
    'm2r',
]
{% if cookiecutter.add_makefile_comments == 'y' %}
# Add any paths that contain templates here, relative to this directory.{% endif %}
templates_path = ['_templates']
{% if cookiecutter.add_makefile_comments == 'y' %}
# The suffix of source filenames.{% endif %}
source_suffix = '.rst'
{% if cookiecutter.add_makefile_comments == 'y' %}
# The encoding of source files.
# source_encoding = 'utf-8-sig'

# The master toctree document.{% endif %}
master_doc = 'index'
{% if cookiecutter.add_makefile_comments == 'y' %}
# General information about the project.{% endif %}
project = '{{cookiecutter.project_slug}}'
{% if cookiecutter.add_makefile_comments == 'y' %}
# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.{% endif %}
version = subprocess.Popen(['python', 'setup.py', '--version'],
                           cwd="..",
                           stdout=subprocess.PIPE)\
    .stdout.read().decode("utf-8").strip()
{% if cookiecutter.add_makefile_comments == 'y' %}
# The full version, including alpha/beta/rc tags.{% endif %}
release = version
{% if cookiecutter.add_makefile_comments == 'y' %}
# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
# language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ''
# Else, today_fmt is used as the format for a strftime call.
# today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.{% endif %}
exclude_patterns = ['../tests']
exclude_patterns = ['_build', '**.ipynb_checkpoints']
{% if cookiecutter.add_makefile_comments == 'y' %}
# The reST default role (used for this markup: `text`) to use for all documents.
# default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
# add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.{% endif %}
show_authors = False
{% if cookiecutter.add_makefile_comments == 'y' %}
# The name of the Pygments (syntax highlighting) style to use.{% endif %}
pygments_style = 'sphinx'
{% if cookiecutter.add_makefile_comments == 'y' %}
# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
# We are on readthedocs.org ?{% endif %}
if not os.environ.get('READTHEDOCS', None) == 'True':  # only set the theme if we're building docs locally
    html_theme = 'sphinx_rtd_theme'{% if cookiecutter.add_makefile_comments == 'y' %}
# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
# html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
# html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
# html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".{% endif %}
html_static_path = ['_static']
{% if cookiecutter.add_makefile_comments == 'y' %}
# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
# html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
# html_domain_indices = True

# If false, no index is generated.{% endif %}
html_use_index = True
{% if cookiecutter.add_makefile_comments == 'y' %}
# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.{% endif %}
html_show_sourcelink = False
{% if cookiecutter.add_makefile_comments == 'y' %}
# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
# html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.{% endif %}
html_show_copyright = True
copyright='{{cookiecutter.author}}'
{% if cookiecutter.add_makefile_comments == 'y' %}
# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.{% endif %}
html_use_opensearch = ''
{% if cookiecutter.add_makefile_comments == 'y' %}
# This is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = None

# Output file base name for HTML help builder.{% endif %}
htmlhelp_basename = '{{cookiecutter.project_slug}}doc'
{% if cookiecutter.add_makefile_comments == 'y' %}
# -- Options for LaTeX output --------------------------------------------------{% endif %}
latex_engine = 'pdflatex'
latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    'papersize': 'a4paper',

    # The font size ('10pt', '11pt' or '12pt').
    'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    # 'preamble': '',
}
{% if cookiecutter.add_makefile_comments == 'y' %}
# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).{% endif %}
latex_documents = [
    (
        master_doc,  # Doc name
        '{{cookiecutter.project_slug.replace('_', '')}}.tex',  # targetname
        '{{cookiecutter.project_name}} Documentation',  # title
        '{{cookiecutter.project_slug.replace('_', '')}}',  # author
#        'manual',  # documentclass
        'howto',  # documentclass
        False, # toctree_only
    ),
]
{% if cookiecutter.add_makefile_comments == 'y' %}
# The name of an image file (relative to this directory) to place at the top of
# the title page.
# latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
# latex_use_parts = False

# If true, show page references after internal links.
# latex_show_pagerefs = False

# If true, show URL addresses after external links.
# latex_show_urls = False

# Documents to append as an appendix to all manuals.
# latex_appendices = []

# If false, no module index is generated.
# latex_domain_indices = True


# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).{% endif %}
man_pages = [
    ('index',
     '{{cookiecutter.project_slug}}',
     '{{cookiecutter.project_name}} Documentation',
     ['{{cookiecutter.author}}'], 1)
]
{% if cookiecutter.add_makefile_comments == 'y' %}
# If true, show URL addresses after external links.
# man_show_urls = False


# -- Options for Texinfo output ------------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category){% endif %}
texinfo_documents = [
    ('index',
     '{{cookiecutter.project_slug}}',
     '{{cookiecutter.project_name}} Documentation',
     '{{cookiecutter.author}}',
     ),
]
{% if cookiecutter.add_makefile_comments == 'y' %}
# Documents to append as an appendix to all manuals.
# texinfo_appendices = []

# If false, no module index is generated.
# texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
# texinfo_show_urls = 'footnote'

# -- Options for todo output --------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/todo.html{% endif %}
todo_include_todos=True
{% if cookiecutter.add_makefile_comments == 'y' %}
# -- Options for applehelp output --------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/builders/index.html?highlight=pdf#sphinxcontrib.applehelp.AppleHelpBuilder{% endif %}
applehelp_disable_external_tools=False
{% if cookiecutter.add_makefile_comments == 'y' %}
# Add project variables{% endif %}
rst_prolog = f"""
.. |giturl| replace:: {git_url}
.. |homeurl| replace:: {home_url}
"""