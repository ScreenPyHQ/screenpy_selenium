from __future__ import annotations

from typing import TYPE_CHECKING, cast
from unittest import mock

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from screenpy_selenium import BrowseTheWeb, Target

if TYPE_CHECKING:
    from screenpy import Actor


def get_mocked_element() -> mock.Mock:
    return mock.create_autospec(WebElement, instance=True)


def get_mocked_chain() -> mock.Mock:
    return mock.create_autospec(ActionChains, instance=True)


def get_mock_target_class() -> type:
    class FakeTarget(Target):
        def __new__(cls, *args: object, **kwargs: object) -> FakeTarget:  # noqa: ARG003
            return mock.create_autospec(FakeTarget, instance=True)

    return FakeTarget


def get_mocked_target_and_element() -> tuple[mock.Mock, mock.Mock]:
    """Get a mocked target which returns a mocked element."""
    target = get_mock_target_class()()
    element = get_mocked_element()
    target.found_by.return_value = element

    return target, element


def get_mocked_browser(actor: Actor) -> mock.Mock:
    return cast(mock.Mock, actor.ability_to(BrowseTheWeb).browser)


def get_mocked_webdriver() -> mock.Mock:
    return mock.create_autospec(WebDriver, instance=True)
