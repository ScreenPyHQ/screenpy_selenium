ScreenPy Selenium
=================

[![Build Status](../../actions/workflows/tests.yml/badge.svg)](../../actions/workflows/tests.yml)
[![Build Status](../../actions/workflows/lint.yml/badge.svg)](../../actions/workflows/lint.yml)

[![Supported Versions](https://img.shields.io/pypi/pyversions/screenpy_selenium.svg)](https://pypi.org/project/screenpy_selenium)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

```
TITLE CARD:
                              "ScreenPy Selenium"                               
TITLE DISAPPEARS.
                                                                      FADE IN:
EXT. DOCUMENTATION - AFTERNOON, CLOUDY

AUDIENCE appears through a wrought-iron gate, looking around. NARRATOR's
muffled voice can be heard growing louder as AUDIENCE approaches center.
Inside is a menagerie of loud, exotic-looking birds and animals. NARRATOR
speaks louder to be heard over the din.

                              NARRATOR (V.O.)
            You've wandered into ScreenPy Selenium. It allows
            Actors to test web applications using Selenium.

                              AUDIENCE
                              (shouting)
            What?? I can barely hear you!! Speak up! Why are there
            so many??

                              NARRATOR (V.O.)
            Selenium was the first extension for ScreenPy, so it is
            the most mature, and the largest.

                              AUDIENCE
                              (shouting, louder)
            I still can't hear you!! I'm going to find somewhere
            quieter!

                              NARRATOR (V.O.)
            Lead the way...

                                                                      FADE OUT
```


Installation
------------
    pip install screenpy_selenium

or

    pip install screenpy[selenium]


Documentation
-------------
Please check out the [Read The Docs documentation](https://screenpy-selenium-docs.readthedocs.io/en/latest/) for the latest information about this module!

You can also read the [ScreenPy Docs](https://screenpy-docs.readthedocs.io/en/latest/) for more information about ScreenPy in general.


Contributing
------------
You want to contribute? Great! Here are the things you should do before submitting your PR:

1. Fork the repo and git clone your fork.
1. `dev` install the project package:
    1. `pip install -e .[dev]`
    1. Optional (poetry users):
        1. `poetry install --extras dev`
1. Run `pre-commit install` once.
1. Run `tox` to perform tests frequently.
1. Create pull-request from your branch.

That's it! :)
