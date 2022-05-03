from unittest import mock

import pytest
from screenpy import AnActor
from screenpy_pyotp.abilities import AuthenticateWith2FA

from screenpy_selenium.abilities import BrowseTheWeb


@pytest.fixture(scope="function")
def Tester() -> AnActor:
    """Provide an Actor with mocked web browsing abilities."""
    AuthenticateWith2FA_Mocked = mock.Mock(spec=AuthenticateWith2FA)
    AuthenticateWith2FA_Mocked.otp = mock.Mock()
    BrowseTheWeb_Mocked = mock.Mock(spec=BrowseTheWeb)
    BrowseTheWeb_Mocked.browser = mock.Mock()

    return AnActor.named("Tester").who_can(
        AuthenticateWith2FA_Mocked, BrowseTheWeb_Mocked
    )
