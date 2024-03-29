from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from screenpy_selenium import Target, TargetingError

from .useful_mocks import get_mocked_browser

if TYPE_CHECKING:
    from screenpy import Actor


def test_can_be_instantiated() -> None:
    t1 = Target.the("test")
    t2 = Target.the("test").located_by("test")
    t3 = Target.the("test").located("test")
    t4 = Target("test")
    t5 = Target().located_by("test")
    t6 = Target()

    assert isinstance(t1, Target)
    assert isinstance(t2, Target)
    assert isinstance(t3, Target)
    assert isinstance(t4, Target)
    assert isinstance(t5, Target)
    assert isinstance(t6, Target)


def test_auto_describe() -> None:
    """When no description is provided, automatically use the string of the locator"""
    t1 = Target().located_by((By.ID, "foo-id"))
    t2 = Target("blah").located_by("foo")
    t3 = Target()
    t4 = Target("").located("baz")

    assert t1.target_name == "foo-id"
    assert t2.target_name == "blah"
    assert t3.target_name is None
    assert t4.target_name == ""


def test_del_description() -> None:
    t1 = Target("test")
    del t1.target_name

    assert t1.target_name is None


def test_complains_for_no_locator() -> None:
    """Raises if no locator was supplied."""
    target = Target.the("test")

    with pytest.raises(TargetingError):
        target.get_locator()


def test_get_locator() -> None:
    """Returns the locator tuple when asked for it"""
    css_selector = "#id"
    xpath_locator = '//div[@id="id"]'
    xpath_locator_2 = "(//a)[5]"
    id_locator = "someID"

    css_target = Target.the("css element").located_by(css_selector)
    xpath_target = Target.the("xpath element").located_by(xpath_locator)
    xpath_target_2 = Target.the("xpath element 2").located_by(xpath_locator_2)
    id_target = Target.the("id element").located_by((By.ID, id_locator))

    assert css_target.get_locator() == (By.CSS_SELECTOR, css_selector)
    assert xpath_target.get_locator() == (By.XPATH, xpath_locator)
    assert xpath_target_2.get_locator() == (By.XPATH, xpath_locator_2)
    assert id_target.get_locator() == (By.ID, id_locator)


def test_located() -> None:
    """Uses the provided locator tuple, unaltered"""
    locator = (By.ID, "spam")
    target = Target.the("test").located(locator)

    assert target.get_locator() == locator


def test_can_be_indexed() -> None:
    locator = (By.ID, "eggs")
    target = Target.the("test").located(locator)

    assert target[0] == locator[0]
    assert target[1] == locator[1]


def test_locator_tuple_size() -> None:
    with pytest.raises(ValueError, match="locator tuple length should be 2"):
        Target("test").located((By.ID, "foo", "baz"))  # type: ignore[arg-type]

    with pytest.raises(ValueError, match="locator tuple length should be 2"):
        Target("test").located((By.ID,))  # type: ignore[arg-type]

    with pytest.raises(TypeError, match="invalid locator type"):  # type: ignore[assignment]
        Target("test").located_by([By.ID, "foo"])  # type: ignore[arg-type]


def test_found_by(Tester: Actor) -> None:
    test_locator = (By.ID, "eggs")
    Target.the("test").located(test_locator).found_by(Tester)

    mocked_browser = get_mocked_browser(Tester)
    mocked_browser.find_element.assert_called_once_with(*test_locator)


def test_found_by_raises(Tester: Actor) -> None:
    test_name = "frobnosticator"
    mocked_browser = get_mocked_browser(Tester)
    mocked_browser.find_element.side_effect = WebDriverException

    with pytest.raises(TargetingError) as excinfo:
        Target.the(test_name).located_by("*").found_by(Tester)
    assert test_name in str(excinfo.value)


def test_all_found_by(Tester: Actor) -> None:
    test_locator = (By.ID, "baked beans")
    Target.the("test").located(test_locator).all_found_by(Tester)

    mocked_browser = get_mocked_browser(Tester)
    mocked_browser.find_elements.assert_called_once_with(*test_locator)


def test_all_found_by_raises(Tester: Actor) -> None:
    test_name = "transmogrifier"
    mocked_browser = get_mocked_browser(Tester)
    mocked_browser.find_elements.side_effect = WebDriverException

    with pytest.raises(TargetingError) as excinfo:
        Target.the(test_name).located_by("*").all_found_by(Tester)
    assert test_name in str(excinfo.value)


def test_iterator() -> None:
    locator = (By.ID, "eggs")
    target = Target.the("test").located(locator)
    it1 = target.__iter__()

    assert next(it1) == locator[0]
    assert next(it1) == locator[1]
    with pytest.raises(StopIteration):
        next(it1)


def test_empty_target_iterator() -> None:
    nulltarget = Target("bogus")

    with pytest.raises(TargetingError):
        iter(nulltarget)


def test_repr() -> None:
    t1 = Target()
    t2 = Target("foo")

    assert repr(t1) == "None"
    assert repr(t2) == "foo"


def test_str() -> None:
    t1 = Target()
    t2 = Target("foo")

    assert str(t1) == "None"
    assert str(t2) == "foo"
