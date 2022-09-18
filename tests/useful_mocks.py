from unittest import mock

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement

from screenpy_selenium import Target


def get_mocked_element():
    return mock.create_autospec(WebElement, instance=True)


def get_mocked_chain():
    return mock.create_autospec(ActionChains, instance=True)


def get_mocked_target_and_element():
    """Get a mocked target which returns a mocked element."""
    target = mock.create_autospec(Target, instance=True)
    element = get_mocked_element()
    target.found_by.return_value = element

    return target, element
