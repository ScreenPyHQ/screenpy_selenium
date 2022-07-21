from unittest import mock

import pytest
from screenpy import AnActor
from screenpy_pyotp.abilities import AuthenticateWith2FA

from screenpy_selenium.abilities import BrowseTheWeb
from selenium.webdriver.remote.webdriver import WebDriver


@pytest.fixture(scope="function")
def Tester() -> AnActor:
    """Provide an Actor with mocked web browsing abilities."""
    AuthenticateWith2FA_Mocked = mock.create_autospec(AuthenticateWith2FA, instance=True)
    AuthenticateWith2FA_Mocked.otp = mock.Mock()
    BrowseTheWeb_Mocked = mock.create_autospec(BrowseTheWeb, instance=True)
    BrowseTheWeb_Mocked.browser = mock.create_autospec(WebDriver, instance=True)

    return AnActor.named("Tester").who_can(
        AuthenticateWith2FA_Mocked, BrowseTheWeb_Mocked
    )
