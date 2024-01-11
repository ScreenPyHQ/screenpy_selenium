"""Enable the actor to browse the web."""
from __future__ import annotations

import os
from typing import Type, TypeVar

from selenium.webdriver import Chrome, Firefox, Remote, Safari
from selenium.webdriver.remote.webdriver import WebDriver

from ..exceptions import BrowsingError

DEFAULT_APPIUM_HUB_URL = "http://localhost:4723/wd/hub"


SelfBrowseTheWeb = TypeVar("SelfBrowseTheWeb", bound="BrowseTheWeb")


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
    def using_chrome(cls: Type[SelfBrowseTheWeb]) -> SelfBrowseTheWeb:
        """Create and use a default Chrome Selenium webdriver instance."""
        return cls.using(browser=Chrome())

    @classmethod
    def using_firefox(cls: Type[SelfBrowseTheWeb]) -> SelfBrowseTheWeb:
        """Create and use a default Firefox Selenium webdriver instance."""
        return cls.using(browser=Firefox())

    @classmethod
    def using_safari(cls: Type[SelfBrowseTheWeb]) -> SelfBrowseTheWeb:
        """Create and use a default Safari Selenium webdriver instance."""
        return cls.using(browser=Safari())

    @classmethod
    def using_ios(cls: Type[SelfBrowseTheWeb]) -> SelfBrowseTheWeb:
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
        IOS_CAPABILITIES = {
            "platformName": "iOS",
            "platformVersion": os.getenv("IOS_DEVICE_VERSION"),
            "deviceName": os.getenv("IOS_DEVICE_NAME", "iPhone Simulator"),
            "automationName": "xcuitest",
            "browserName": "Safari",
        }
        if IOS_CAPABILITIES["platformVersion"] is None:
            msg = "IOS_DEVICE_VERSION Environment variable must be set."
            raise BrowsingError(msg)

        return cls.using(browser=Remote(hub_url, IOS_CAPABILITIES))

    @classmethod
    def using_android(cls: Type[SelfBrowseTheWeb]) -> SelfBrowseTheWeb:
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
        ANDROID_CAPABILITIES = {
            "platformName": "Android",
            "platformVersion": os.getenv("ANDROID_DEVICE_VERSION"),
            "deviceName": os.getenv("ANDROID_DEVICE_NAME", "Android Emulator"),
            "automationName": "UIAutomator2",
            "browserName": "Chrome",
        }
        if ANDROID_CAPABILITIES["platformVersion"] is None:
            msg = "ANDROID_DEVICE_VERSION environment variable must be set."
            raise BrowsingError(msg)

        return cls.using(browser=Remote(hub_url, ANDROID_CAPABILITIES))

    @classmethod
    def using(cls: Type[SelfBrowseTheWeb], browser: WebDriver) -> SelfBrowseTheWeb:
        """Provide an already-set-up WebDriver to use to browse the web."""
        return cls(browser=browser)

    def forget(self: SelfBrowseTheWeb) -> None:
        """Quit the attached browser."""
        self.browser.quit()

    def __repr__(self: SelfBrowseTheWeb) -> str:
        """Repr."""
        return "Browse the Web"

    __str__ = __repr__

    def __init__(self: SelfBrowseTheWeb, browser: WebDriver) -> None:
        self.browser = browser
