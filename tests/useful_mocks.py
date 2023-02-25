from typing import Any, Tuple
from unittest import mock

from screenpy import Actor
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from screenpy_selenium import BrowseTheWeb, Target


def get_mocked_element() -> mock.Mock:
    return mock.create_autospec(WebElement, instance=True)


def get_mocked_chain() -> mock.Mock:
    return mock.create_autospec(ActionChains, instance=True)


def get_mock_target_class() -> Any:
    class FakeTarget(Target):
        def __new__(cls, *args, **kwargs):
            rt = mock.create_autospec(FakeTarget, instance=True)
            return rt
    return FakeTarget


def get_mocked_target_and_element() -> Tuple[mock.Mock, mock.Mock]:
    """Get a mocked target which returns a mocked element."""
    target = get_mock_target_class()()
    element = get_mocked_element()
    target.found_by.return_value = element

    return target, element


def get_mocked_browser(actor: Actor) -> mock.Mock:
    browser = actor.ability_to(BrowseTheWeb).browser
    return browser  # type: ignore


def get_mocked_webdriver() -> mock.Mock:
    return mock.create_autospec(WebDriver, instance=True)
