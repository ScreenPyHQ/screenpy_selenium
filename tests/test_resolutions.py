from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import pytest
from hamcrest.core.string_description import StringDescription

from screenpy_selenium import IsClickable, IsInvisible, IsPresent, IsVisible
from screenpy_selenium.resolutions.custom_matchers.is_clickable_element import (
    IsClickableElement,
)
from screenpy_selenium.resolutions.custom_matchers.is_invisible_element import (
    IsInvisibleElement,
)
from screenpy_selenium.resolutions.custom_matchers.is_present_element import (
    IsPresentElement,
)
from screenpy_selenium.resolutions.custom_matchers.is_visible_element import (
    IsVisibleElement,
)

from .useful_mocks import get_mocked_element

if TYPE_CHECKING:
    from hamcrest.core.matcher import Matcher
    from selenium.webdriver.remote.webelement import WebElement


@dataclass
class ExpectedDescriptions:
    describe_to: str
    describe_match: str
    describe_mismatch: str
    describe_none: str


def _assert_descriptions(
    obj: Matcher[Any], element: WebElement, expected: ExpectedDescriptions
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


class TestIsClickable:
    def test_can_be_instantiated(self) -> None:
        ic = IsClickable()

        assert isinstance(ic, IsClickable)

    def test_matches_a_clickable_element(self) -> None:
        element = get_mocked_element()
        element.is_enabled.return_value = True
        element.is_displayed.return_value = True
        ic = IsClickable().resolve()

        assert ic._matches(element)

    def test_does_not_match_unclickable_element(self) -> None:
        invisible_element = get_mocked_element()
        inactive_element = get_mocked_element()

        invisible_element.is_displayed.return_value = False
        invisible_element.is_enabled.return_value = True
        inactive_element.is_displayed.return_value = True
        inactive_element.is_enabled.return_value = False
        ic = IsClickable().resolve()

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
        ic = IsClickable()

        assert ic.describe() == "clickable"
        _assert_descriptions(ic.resolve(), element, expected)

    def test_type_hint(self) -> None:
        ic = IsClickable()
        annotation = ic.resolve.__annotations__["return"]
        assert annotation == "IsClickableElement"
        assert type(ic.resolve()) is IsClickableElement

    def test_beat_logging(self, caplog: pytest.LogCaptureFixture) -> None:
        caplog.set_level(logging.INFO)
        IsClickable().resolve()

        assert [r.msg for r in caplog.records] == [
            "... hoping it's clickable.",
            "    => the element is enabled/clickable",
        ]


class TestIsVisible:
    def test_can_be_instantiated(self) -> None:
        iv = IsVisible()

        assert isinstance(iv, IsVisible)

    def test_matches_a_visible_element(self) -> None:
        element = get_mocked_element()
        element.is_displayed.return_value = True
        iv = IsVisible().resolve()

        assert iv._matches(element)

    def test_does_not_match_invisible_element(self) -> None:
        element = get_mocked_element()
        element.is_displayed.return_value = False
        iv = IsVisible().resolve()

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
        iv = IsVisible()

        assert iv.describe() == "visible"
        _assert_descriptions(iv.resolve(), element, expected)

    def test_type_hint(self) -> None:
        iv = IsVisible()
        annotation = iv.resolve.__annotations__["return"]
        assert annotation == "IsVisibleElement"
        assert type(iv.resolve()) is IsVisibleElement

    def test_beat_logging(self, caplog: pytest.LogCaptureFixture) -> None:
        caplog.set_level(logging.INFO)
        IsVisible().resolve()

        assert [r.msg for r in caplog.records] == [
            "... hoping it's visible.",
            "    => the element is visible",
        ]


class TestIsInvisible:
    def test_can_be_instantiated(self) -> None:
        ii = IsInvisible()

        assert isinstance(ii, IsInvisible)

    def test_matches_an_invisible_element(self) -> None:
        element = get_mocked_element()
        element.is_displayed.return_value = False
        ii = IsInvisible().resolve()

        assert ii.matches(element)
        assert ii.matches(None)  # element was not found by Element()

    def test_does_not_match_visible_element(self) -> None:
        element = get_mocked_element()
        element.is_displayed.return_value = True
        ii = IsInvisible().resolve()

        assert not ii.matches(element)

    def test_descriptions(self) -> None:
        element = get_mocked_element()
        expected = ExpectedDescriptions(
            describe_to="the element is invisible",
            describe_match="it was invisible",
            describe_mismatch="was not invisible",
            describe_none="it was invisible",
        )

        obj = IsInvisible().resolve()
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

        ii = IsInvisible()

        assert ii.describe() == "invisible"

    def test_type_hint(self) -> None:
        ii = IsInvisible()
        annotation = ii.resolve.__annotations__["return"]
        assert annotation == "IsInvisibleElement"
        assert type(ii.resolve()) is IsInvisibleElement

    def test_beat_logging(self, caplog: pytest.LogCaptureFixture) -> None:
        caplog.set_level(logging.INFO)
        IsInvisible().resolve()

        assert [r.msg for r in caplog.records] == [
            "... hoping it's invisible.",
            "    => the element is invisible",
        ]


class TestIsPresent:
    def test_can_be_instantiated(self) -> None:
        ip = IsPresent()

        assert isinstance(ip, IsPresent)

    @pytest.mark.parametrize(
        ("enabled", "displayed"),
        [(False, False), (False, True), (True, False), (True, True)],
    )
    def test_matches_a_present_element(self, enabled: bool, displayed: bool) -> None:
        element = get_mocked_element()
        element.is_enabled.return_value = enabled
        element.is_displayed.return_value = displayed
        ic = IsPresent().resolve()

        assert ic._matches(element)

    def test_does_not_match_missing_element(self) -> None:
        ic = IsPresent().resolve()

        assert not ic._matches(None)

    def test_descriptions(self) -> None:
        element = get_mocked_element()
        expected = ExpectedDescriptions(
            describe_to="the element is present",
            describe_match="it was present",
            describe_mismatch="was not present",
            describe_none="was not present",
        )
        ip = IsPresent()

        assert ip.describe() == "present"
        _assert_descriptions(ip.resolve(), element, expected)

    def test_type_hint(self) -> None:
        ip = IsPresent()
        annotation = ip.resolve.__annotations__["return"]
        assert annotation == "IsPresentElement"
        assert type(ip.resolve()) is IsPresentElement

    def test_beat_logging(self, caplog: pytest.LogCaptureFixture) -> None:
        caplog.set_level(logging.INFO)
        IsPresent().resolve()

        assert [r.msg for r in caplog.records] == [
            "... hoping it's present.",
            "    => the element is present",
        ]
