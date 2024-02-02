from dataclasses import dataclass

import pytest
from hamcrest.core.string_description import StringDescription
from screenpy import BaseResolution
from selenium.webdriver.remote.webelement import WebElement

from screenpy_selenium import IsClickable, IsInvisible, IsPresent, IsVisible
from useful_mocks import get_mocked_element


@dataclass
class ExpectedDescriptions:
    describe_to: str
    describe_match: str
    describe_mismatch: str
    describe_none: str


def _assert_descriptions(
    obj: BaseResolution, element: WebElement, expected: ExpectedDescriptions
) -> None:
    describe_to = StringDescription()
    describe_match = StringDescription()
    describe_mismatch = StringDescription()
    describe_none = StringDescription()

    obj.describe_to(describe_to)
    obj.describe_match(element, describe_match)
    obj.describe_mismatch(element, describe_mismatch)
    obj.describe_mismatch(None, describe_none)

    assert describe_to.out == expected.describe_to
    assert describe_match.out == expected.describe_match
    assert describe_mismatch.out == expected.describe_mismatch
    assert describe_none.out == expected.describe_none


def assert_matcher_annotation(obj: BaseResolution) -> None:
    assert type(obj.matcher) is obj.__annotations__["matcher"]


class TestIsClickable:
    def test_can_be_instantiated(self) -> None:
        ic = IsClickable()

        assert isinstance(ic, IsClickable)

    def test_matches_a_clickable_element(self) -> None:
        element = get_mocked_element()
        element.is_enabled.return_value = True
        element.is_displayed.return_value = True
        ic = IsClickable()

        assert ic._matches(element)

    def test_does_not_match_unclickable_element(self) -> None:
        invisible_element = get_mocked_element()
        inactive_element = get_mocked_element()

        invisible_element.is_displayed.return_value = False
        invisible_element.is_enabled.return_value = True
        inactive_element.is_displayed.return_value = True
        inactive_element.is_enabled.return_value = False
        ic = IsClickable()

        assert not ic._matches(None)  # element was not found by Element()
        assert not ic._matches(invisible_element)
        assert not ic._matches(inactive_element)

    def test_descriptions(self) -> None:
        element = get_mocked_element()
        expected = ExpectedDescriptions(
            describe_to="the element is enabled/clickable",
            describe_match="it was enabled/clickable",
            describe_mismatch="was not enabled/clickable",
            describe_none="was not even present",
        )

        _assert_descriptions(IsClickable(), element, expected)

    def test_type_hint(self) -> None:
        assert_matcher_annotation(IsClickable())


class TestIsVisible:
    def test_can_be_instantiated(self) -> None:
        iv = IsVisible()

        assert isinstance(iv, IsVisible)

    def test_matches_a_visible_element(self) -> None:
        element = get_mocked_element()
        element.is_displayed.return_value = True
        iv = IsVisible()

        assert iv._matches(element)

    def test_does_not_match_invisible_element(self) -> None:
        element = get_mocked_element()
        element.is_displayed.return_value = False
        iv = IsVisible()

        assert not iv._matches(None)  # element was not found by Element()
        assert not iv._matches(element)

    def test_descriptions(self) -> None:
        element = get_mocked_element()
        expected = ExpectedDescriptions(
            describe_to="the element is visible",
            describe_match="it was visible",
            describe_mismatch="was not visible",
            describe_none="was not even present",
        )

        _assert_descriptions(IsVisible(), element, expected)

    def test_type_hint(self) -> None:
        assert_matcher_annotation(IsVisible())


class TestIsInvisible:
    def test_can_be_instantiated(self) -> None:
        ii = IsInvisible()

        assert isinstance(ii, IsInvisible)

    def test_matches_an_invisible_element(self) -> None:
        element = get_mocked_element()
        element.is_displayed.return_value = False
        ii = IsInvisible()

        assert ii._matches(element)
        assert ii._matches(None)  # element was not found by Element()

    def test_does_not_match_visible_element(self) -> None:
        element = get_mocked_element()
        element.is_displayed.return_value = True
        ii = IsInvisible()

        assert not ii._matches(element)

    def test_descriptions(self) -> None:
        element = get_mocked_element()
        expected = ExpectedDescriptions(
            describe_to="the element is invisible",
            describe_match="it was invisible",
            describe_mismatch="was not invisible",
            describe_none="it was invisible",
        )

        obj = IsInvisible()
        describe_to = StringDescription()
        describe_match = StringDescription()
        describe_mismatch = StringDescription()
        describe_none = StringDescription()

        obj.describe_to(describe_to)
        obj.describe_match(element, describe_match)
        obj.describe_mismatch(element, describe_mismatch)
        obj.describe_match(None, describe_none)

        assert describe_to.out == expected.describe_to
        assert describe_match.out == expected.describe_match
        assert describe_mismatch.out == expected.describe_mismatch
        assert describe_none.out == expected.describe_none

    def test_type_hint(self) -> None:
        assert_matcher_annotation(IsInvisible())


class TestIsPresent:
    def test_can_be_instantiated(self) -> None:
        ip = IsPresent()

        assert isinstance(ip, IsPresent)

    @pytest.mark.parametrize(
        "enabled, displayed",
        ((False, False), (False, True), (True, False), (True, True)),
    )
    def test_matches_a_present_element(self, enabled: bool, displayed: bool) -> None:
        element = get_mocked_element()
        ic = IsPresent()

        element.is_enabled.return_value = enabled
        element.is_displayed.return_value = displayed
        assert ic._matches(element)

    def test_does_not_match_missing_element(self) -> None:
        ic = IsPresent()

        assert not ic._matches(None)

    def test_descriptions(self) -> None:
        element = get_mocked_element()
        expected = ExpectedDescriptions(
            describe_to="the element is present",
            describe_match="it was present",
            describe_mismatch="was not present",
            describe_none="was not present",
        )

        _assert_descriptions(IsPresent(), element, expected)

    def test_type_hint(self) -> None:
        assert_matcher_annotation(IsPresent())
