========
Settings
========

To configure ScreenPy Selenium,
we provide some settings
through `Pydantic's settings management <https://docs.pydantic.dev/usage/settings/>`__.

Settings can be configured through these ways:

  * In your test configuration file (like conftest.py).
  * Using environment variables.
  * In the ``[tool.screenpy.selenium]`` section in your ``pyproject.toml``.

The above options are in order of precedence;
that is,
setting the values directly in your configuration file will override environment variables,
any environment variables will override any ``pyproject.toml`` settings,
and any ``pyproject.toml`` settings will override the defaults.

To demonstrate,
here is how we can change the default actionchain duration
used by things like :class:`screenpy_selenium.actions.Chain`::

    # in your conftest.py
    from screenpy_selenium import settings

    settings.CHAIN_DURATION = 50

.. code-block:: bash

    $ # environment variables in your shell
    $ SCREENPY_SELENIUM_CHAIN_DURATION=50 pytest

.. code-block:: toml

    # in your pyproject.toml file
    [tool.screenpy.selenium]
    CHAIN_DURATION = 50

The environment variable approach
works particularly well with `python-dotenv <https://pypi.org/project/python-dotenv/>`__!



Default Settings
----------------

These are the default settings included in ScreenPy Selenium.

ScreenPy Default Settings
+++++++++++++++++++++++++

.. autopydantic_settings:: screenpy_selenium.configuration.ScreenPySeleniumSettings

