"""Define settings for the StdOutAdapter."""

from pydantic_settings import SettingsConfigDict
from screenpy.configuration import ScreenPySettings


class ScreenPySeleniumSettings(ScreenPySettings):
    """Settings for the ScreenPySelenium.

    To change these settings using environment variables, use the prefix
    ``SCREENPY_SELENIUM_``, like so::

        SCREENPY_SELENIUM_CHAIN_DURATION=50  # sets the indent char to 50
    """

    _tool_path = "screenpy_selenium"
    model_config = SettingsConfigDict(env_prefix="SCREENPY_SELENIUM_")

    CHAIN_DURATION: int = 10
    """Whether or not to use indentation in logging."""


# initialized instance
settings = ScreenPySeleniumSettings()
