# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys


sys.path.insert(0, os.path.abspath("./ext"))
sys.path.insert(0, os.path.abspath("../"))

from screenpy_selenium.__version__ import __version__, __author__, __copyright__  # noqa: need the path first

autodoc_mock_imports = ["selenium", "screenpy", "screenpy_pyotp"]


# -- Project information -----------------------------------------------------

project = 'screenpy_selenium'
copyright = __copyright__
author = __author__

# The full version, including alpha/beta/rc tags
release = __version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.intersphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "autodoc_skip_protocols",
]

intersphinx_mapping = {
    "screenpy": ("https://screenpy-docs.readthedocs.io/en/latest/", None),
    "selenium": ("https://selenium-python.readthedocs.io/", None),
    "screenpy_pyotp": ("https://screenpy-pyotp-docs.readthedocs.io/en/latest/", None),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

rst_prolog = """.. Substitutions

.. .. External
.. |Keys| replace:: :external+selenium:class:`~selenium.webdriver.common.keys.Keys`
.. |By| replace:: :external+selenium:class:`~selenium.webdriver.common.by.By`
.. |WebElement| replace:: :external+selenium:class:`~selenium.webdriver.remote.webelement.WebElement`
.. |ActionChains| replace:: :external+selenium:class:`~selenium.webdriver.common.action_chains.ActionChains`
"""

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'default'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Other HTML settings
autodoc_member_order = "bysource"
add_module_names = False
