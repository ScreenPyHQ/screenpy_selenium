import os
from unittest import mock

import pytest

from screenpy_selenium import BrowseTheWeb, BrowsingError, Forgettable
from useful_mocks import get_mocked_webdriver


class TestBrowseTheWeb:
    def test_can_be_instantiated(self) -> None:
        b = BrowseTheWeb.using(get_mocked_webdriver())

        assert isinstance(b, BrowseTheWeb)

    def test_implements_protocol(self) -> None:
        b = BrowseTheWeb(get_mocked_webdriver())

        assert isinstance(b, Forgettable)

    @mock.patch("screenpy_selenium.abilities.browse_the_web.Firefox", autospec=True)
    def test_using_firefox(self, mocked_firefox) -> None:
        BrowseTheWeb.using_firefox()

        mocked_firefox.assert_called_once()

    @mock.patch("screenpy_selenium.abilities.browse_the_web.Chrome", autospec=True)
    def test_using_chrome(self, mocked_chrome) -> None:
        BrowseTheWeb.using_chrome()

        mocked_chrome.assert_called_once()

    @mock.patch("screenpy_selenium.abilities.browse_the_web.Safari", autospec=True)
    def test_using_safari(self, mocked_safari) -> None:
        BrowseTheWeb.using_safari()

        mocked_safari.assert_called_once()

    @mock.patch.dict(os.environ, {"IOS_DEVICE_VERSION": "1"})
    @mock.patch("screenpy_selenium.abilities.browse_the_web.Remote", autospec=True)
    def test_using_ios(self, mocked_remote) -> None:
        BrowseTheWeb.using_ios()

        mocked_remote.assert_called_once()

    def test_using_ios_without_env_var(self) -> None:
        with pytest.raises(BrowsingError):
            BrowseTheWeb.using_ios()

    @mock.patch.dict(os.environ, {"ANDROID_DEVICE_VERSION": "1"})
    @mock.patch("screenpy_selenium.abilities.browse_the_web.Remote", autospec=True)
    def test_using_android(self, mocked_android) -> None:
        BrowseTheWeb.using_android()

        mocked_android.assert_called_once()

    def test_using_android_without_env_var(self) -> None:
        with pytest.raises(BrowsingError):
            BrowseTheWeb.using_android()

    @mock.patch("screenpy_selenium.abilities.browse_the_web.Chrome", autospec=True)
    def test_forget_calls_quit(self, mocked_chrome) -> None:
        b = BrowseTheWeb(mocked_chrome)

        b.forget()

        mocked_chrome.quit.assert_called_once()

    def test_repr(self) -> None:
        assert repr(BrowseTheWeb(get_mocked_webdriver())) == "Browse the Web"

    def test_subclass(self) -> None:
        """test code for mypy to scan without issue"""
        class SubBrowseTheWeb(BrowseTheWeb):
            def new_method(self):
                return True

        assert SubBrowseTheWeb.using(get_mocked_webdriver()).new_method() == True
