from typing import Tuple
from unittest import mock

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver

from screenpy import Actor
from screenpy_selenium import Target
from screenpy_selenium.abilities import BrowseTheWeb


def get_mocked_element() -> mock.Mock:
    return mock.create_autospec(WebElement, instance=True)


def get_mocked_chain() -> mock.Mock:
    return mock.create_autospec(ActionChains, instance=True)


def get_mocked_target() -> mock.Mock:
    return mock.create_autospec(Target, instance=True)


def get_mocked_target_and_element() -> Tuple[mock.Mock, mock.Mock]:
    """Get a mocked target which returns a mocked element."""
    target = get_mocked_target()
    element = get_mocked_element()
    target.found_by.return_value = element

    return target, element


def get_mocked_browser(actor: Actor) -> mock.Mock:
    browser = actor.ability_to(BrowseTheWeb).browser
    return browser  # type: ignore


def get_mocked_webdriver() -> mock.Mock:
    return mock.create_autospec(WebDriver, instance=True)
