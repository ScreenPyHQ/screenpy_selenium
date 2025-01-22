"""Enable the actor to browse the web."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from selenium.webdriver import Chrome, Firefox, Remote, Safari
from selenium.webdriver.common.options import ArgOptions

from ..exceptions import BrowsingError

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from typing_extensions import Self

DEFAULT_APPIUM_HUB_URL = "http://localhost:4723/wd/hub"


class BrowseTheWeb:
    """Use Selenium to enable browsing the web with a web browser.

    Examples::

        Perry = AnActor.named("Perry").who_can(
            BrowseTheWeb.using_firefox()
        )

        Perry = AnActor.named("Perry").who_can(
            BrowseTheWeb.using(driver)
        )
    """

    browser: WebDriver

    @classmethod
    def using_chrome(cls) -> Self:
        """Create and use a default Chrome Selenium webdriver instance."""
        return cls.using(browser=Chrome())

    @classmethod
    def using_firefox(cls) -> Self:
        """Create and use a default Firefox Selenium webdriver instance."""
        return cls.using(browser=Firefox())

    @classmethod
    def using_safari(cls) -> Self:
        """Create and use a default Safari Selenium webdriver instance."""
        return cls.using(browser=Safari())

    @classmethod
    def using_ios(cls) -> Self:
        """
        Create and use a default Remote driver instance.

        Connects to a running Appium server and open Safari on iOS.

        Note that Appium requires non-trivial setup to be able to connect
        to iPhone simulators. See the Appium documentation to get started:
        http://appium.io/docs/en/writing-running-appium/running-tests/

        Environment Variables:
            APPIUM_HUB_URL: the URL to look for the Appium server. Default
                is "http://localhost:4723/wd/hub"
            IOS_DEVICE_VERSION: the version of the device to put in the
                desired capabilities. This must be set.
            IOS_DEVICE_NAME: the device name to request in the desired
                capabilities. Default is "iPhone Simulator"
        """
        hub_url = os.getenv("APPIUM_HUB_URL", DEFAULT_APPIUM_HUB_URL)

        opts = ArgOptions()
        opts.set_capability("platformName", "iOS")
        opts.set_capability("platformVersion", os.getenv("IOS_DEVICE_VERSION"))
        opts.set_capability(
            "deviceName", os.getenv("IOS_DEVICE_NAME", "iPhone Simulator")
        )
        opts.set_capability("automationName", "xcuitest")
        opts.set_capability("browserName", "Safari")

        IOS_CAPABILITIES = opts.to_capabilities()

        if IOS_CAPABILITIES["platformVersion"] is None:
            msg = "IOS_DEVICE_VERSION Environment variable must be set."
            raise BrowsingError(msg)

        return cls.using(browser=Remote(hub_url, options=opts))

    @classmethod
    def using_android(cls) -> Self:
        """
        Create and use a default Remote driver instance.

        Connects to a running Appium server and open Chrome on Android.

        Note that Appium requires non-trivial setup to be able to connect
        to Android emulators. See the Appium documentation to get started:
        http://appium.io/docs/en/writing-running-appium/running-tests/

        Environment Variables:
            APPIUM_HUB_URL: the URL to look for the Appium server. Default
                is "http://localhost:4723/wd/hub"
            ANDROID_DEVICE_VERSION: the version of the device to put in
                the desired capabilities. This must be set.
            ANDROID_DEVICE_NAME: the device name to request in the desired
                capabilities. Default is "Android Emulator"
        """
        hub_url = os.getenv("APPIUM_HUB_URL", DEFAULT_APPIUM_HUB_URL)

        opts = ArgOptions()
        opts.set_capability("platformName", "Android")
        opts.set_capability("platformVersion", os.getenv("ANDROID_DEVICE_VERSION"))
        opts.set_capability(
            "deviceName", os.getenv("ANDROID_DEVICE_NAME", "Android Emulator")
        )
        opts.set_capability("automationName", "UIAutomator2")
        opts.set_capability("browserName", "Chrome")

        ANDROID_CAPABILITIES = opts.to_capabilities()

        if ANDROID_CAPABILITIES["platformVersion"] is None:
            msg = "ANDROID_DEVICE_VERSION environment variable must be set."
            raise BrowsingError(msg)

        return cls.using(browser=Remote(hub_url, options=opts))

    @classmethod
    def using(cls, browser: WebDriver) -> Self:
        """Provide an already-set-up WebDriver to use to browse the web."""
        return cls(browser=browser)

    def forget(self) -> None:
        """Quit the attached browser."""
        self.browser.quit()

    def __repr__(self) -> str:
        """Repr."""
        return "Browse the Web"

    __str__ = __repr__

    def __init__(self, browser: WebDriver) -> None:
        self.browser = browser
