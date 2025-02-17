"""
A matcher that matches an disabled element.

For example:

    assert_that(driver.find_element_by_id("search"), is_disabled_element())
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from hamcrest.core.base_matcher import BaseMatcher
from selenium.webdriver.remote.webelement import WebElement

if TYPE_CHECKING:
    from hamcrest.core.description import Description


class IsDisabledElement(BaseMatcher[Optional[WebElement]]):
    """Matches an element which is not ``is_enabled``."""

    def _matches(self, item: WebElement | None) -> bool:
        if item is None:
            return False
        return item.is_enabled() is False

    def describe_to(self, description: Description) -> None:
        """Describe the passing case."""
        description.append_text("the element is disabled")

    def describe_match(
        self, _: WebElement | None, match_description: Description
    ) -> None:
        """Describe the matching case."""
        match_description.append_text("it was disabled")

    def describe_mismatch(
        self, item: WebElement | None, mismatch_description: Description
    ) -> None:
        """Describe the failing case."""
        if item is None:
            mismatch_description.append_text("was not even present")
            return
        mismatch_description.append_text("was not disabled")


def is_disabled_element() -> IsDisabledElement:
    """This matcher matches any element that is disabled."""
    return IsDisabledElement()
