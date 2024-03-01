import os
from unittest import mock

from screenpy_selenium import settings as screenpy_selenium_settings
from screenpy_selenium.configuration import ScreenPySeleniumSettings


class TestSettings:
    def test_pyproject_overwrites_initial(self) -> None:
        mock_open = mock.mock_open(
            read_data=b"[tool.screenpy.selenium]\nCHAIN_DURATION = 500"
        )

        with mock.patch("pathlib.Path.open", mock_open):
            settings = ScreenPySeleniumSettings()

        assert settings.CHAIN_DURATION == 500

    def test_env_overwrites_pyproject(self) -> None:
        mock_open = mock.mock_open(
            read_data=b"[tool.screenpy.selenium]\nCHAIN_DURATION = 500"
        )
        mock_env = {"SCREENPY_SELENIUM_CHAIN_DURATION": "1337"}

        with mock.patch("pathlib.Path.open", mock_open):  # noqa: SIM117
            with mock.patch.dict(os.environ, mock_env):
                settings = ScreenPySeleniumSettings()

        assert settings.CHAIN_DURATION == 1337

    def test_init_overwrites_env(self) -> None:
        mock_env = {"SCREENPY_SELENIUM_CHAIN_DURATION": "1337"}

        with mock.patch.dict(os.environ, mock_env):
            settings = ScreenPySeleniumSettings(CHAIN_DURATION=9001)

        assert settings.CHAIN_DURATION == 9001

    def test_can_be_changed_at_runtime(self) -> None:
        try:
            screenpy_selenium_settings.CHAIN_DURATION = 100
        except TypeError as exc:
            msg = "ScreenPySeleniumSettings could not be changed at runtime."
            raise AssertionError(msg) from exc
