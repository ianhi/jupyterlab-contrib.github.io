# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

# List all organization extensions
import os
import pathlib
import requests

HERE = pathlib.Path(__file__).parent
GET_REPOS = "https://api.github.com/orgs/jupyterlab-contrib/repos"
TOKEN = os.getenv("GITHUB_TOKEN")

extensions = (HERE / "extensions.tpl").read_text()
default_headers = {}
if TOKEN is not None:
    default_headers["authorization"] = f"Bearer {TOKEN}"

try:
    repos = requests.get(
        GET_REPOS,
        headers={**default_headers, "Accept": "application/vnd.github.v3+json"},
        params={"per_page": 100},
    )
    data = repos.json()
    for repo in data:
        if isinstance(repo, str):
            raise ValueError(data["message"])

        if repo["name"].startswith("jupyterlab-contrib"):
            continue  # Skip special repositories

        try:
            readme = requests.get(
                repo["contents_url"].replace("{+path}", "README.md"),
                headers={
                    **default_headers,
                    "Accept": "application/vnd.github.VERSION.raw",
                },
            )
            filename = repo["name"]
            (HERE / (filename + ".md")).write_text(readme.text)
            extensions += f"\n   {filename}"
        except BaseException as err:
            print(err)
            print(f"Fail to get README for {filename}.")
except BaseException as err:
    print(err)
    print("Fail to get organization repositories")
finally:
    (HERE / "extensions.rst").write_text(extensions)


# -- Project information -----------------------------------------------------

project = "jupyterlab-contrib"
copyright = "2020, JupyterLab Contrib Team"
author = "JupyterLab Contrib Team"

# The full version, including alpha/beta/rc tags
release = "1.0.0"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "recommonmark",
    # Auto-generate section labels.
    "sphinx.ext.autosectionlabel",
    "sphinx_markdown_tables",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Prefix document path to section labels, otherwise autogenerated labels would look like 'heading'
# rather than 'path/to/file:heading'
autosectionlabel_prefix_document = True

source_suffix = [".rst", ".md"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_material"

html_copy_source = False

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_sidebars = {
    "**": ["logo-text.html", "globaltoc.html", "localtoc.html", "searchbox.html"]
}

# Material theme options (see theme.conf for more information)
html_theme_options = {
    # Set the name of the project to appear in the navigation.
    "nav_title": "JupyterLab Unofficial Extensions & Tools",
    "nav_links": [
        {
            "href": "https://jupyterlab.readthedocs.io/en/stable/",
            "title": "JupyterLab Documentation",
            "internal": False,
        },
        {
            "href": "https://jupyter-server.readthedocs.io/en/stable/",
            "title": "Jupyter Server Documentation",
            "internal": False,
        },
        {
            "href": "https://github.com/jupyterlab-contrib/jupyterlab-contrib.github.io/issues/new?labels=transfer&template=transfer-repository-to-this-organization.md",
            "title": "Transfer your extension",
            "internal": False,
        },
        {
            "href": "https://github.com/jupyterlab-contrib/jupyterlab-contrib.github.io/issues/new?template=help-with-maintenance.md",
            "title": "I want to help",
            "internal": False,
        },
    ],
    "master_doc": False,
    # Set you GA account ID to enable tracking
    # 'google_analytics_account': 'UA-XXXXX',
    # Specify a base_url used to generate sitemap.xml. If not
    # specified, then no sitemap will be built.
    "base_url": "https://jupyterlab-contrib.github.io",
    "logo_icon": "&#xe87b",
    # Set the color and the accent color
    "color_primary": "deep-orange",
    "color_accent": "orange",
    # Set the repo location to get a badge with stats
    "repo_url": "https://github.com/jupyterlab-contrib/jupyterlab-contrib.github.io",
    "repo_name": "jupyterlab-contrib",
    # Visible levels of the global TOC; -1 means unlimited
    "globaltoc_depth": 2,
    # If False, expand all TOC entries
    "globaltoc_collapse": True,
    # If True, show hidden TOC entries
    "globaltoc_includehidden": False,
}
