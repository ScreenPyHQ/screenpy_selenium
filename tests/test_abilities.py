import os
from unittest import mock

import pytest
from screenpy.protocols import Forgettable

from screenpy_selenium.abilities import BrowseTheWeb
from screenpy_selenium.exceptions import BrowsingError


class TestBrowseTheWeb:
    def test_can_be_instantiated(self):
        b = BrowseTheWeb.using(None)

        assert isinstance(b, BrowseTheWeb)

    def test_implements_protocol(self):
        b = BrowseTheWeb(None)
        assert isinstance(b, Forgettable)

    @mock.patch("screenpy_selenium.abilities.browse_the_web.Firefox", autospec=True)
    def test_using_firefox(self, mocked_firefox):
        BrowseTheWeb.using_firefox()

        mocked_firefox.assert_called_once()

    @mock.patch("screenpy_selenium.abilities.browse_the_web.Chrome", autospec=True)
    def test_using_chrome(self, mocked_chrome):
        BrowseTheWeb.using_chrome()

        mocked_chrome.assert_called_once()

    @mock.patch("screenpy_selenium.abilities.browse_the_web.Safari", autospec=True)
    def test_using_safari(self, mocked_safari):
        BrowseTheWeb.using_safari()

        mocked_safari.assert_called_once()

    @mock.patch.dict(os.environ, {"IOS_DEVICE_VERSION": "1"})
    @mock.patch("screenpy_selenium.abilities.browse_the_web.Remote", autospec=True)
    def test_using_ios(self, mocked_remote):
        BrowseTheWeb.using_ios()

        mocked_remote.assert_called_once()

    def test_using_ios_without_env_var(self):
        with pytest.raises(BrowsingError):
            BrowseTheWeb.using_ios()

    @mock.patch.dict(os.environ, {"ANDROID_DEVICE_VERSION": "1"})
    @mock.patch("screenpy_selenium.abilities.browse_the_web.Remote", autospec=True)
    def test_using_android(self, mocked_android):
        BrowseTheWeb.using_android()

        mocked_android.assert_called_once()

    def test_using_android_without_env_var(self):
        with pytest.raises(BrowsingError):
            BrowseTheWeb.using_android()

    @mock.patch("screenpy_selenium.abilities.browse_the_web.Chrome", autospec=True)
    def test_forget_calls_quit(self, mocked_chrome):
        b = BrowseTheWeb(mocked_chrome)
        b.forget()
        mocked_chrome.quit.assert_called_once()

    def test_repr(self):
        assert repr(BrowseTheWeb(None)) == "Browse the Web"
