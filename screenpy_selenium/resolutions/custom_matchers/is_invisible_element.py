"""
A matcher that matches an invisible element.

For example:

    assert_that(driver.find_element_by_id("search"), is_invisible_element())
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from hamcrest.core.base_matcher import BaseMatcher
from selenium.webdriver.remote.webelement import WebElement

if TYPE_CHECKING:
    from hamcrest.core.description import Description


class IsInvisibleElement(BaseMatcher[Optional[WebElement]]):
    """Matches an element whose ``is_displayed`` method returns False."""

    def _matches(self, item: WebElement | None) -> bool:
        if item is None:
            return True
        return item.is_displayed() is False

    def describe_to(self, description: Description) -> None:
        """Describe the passing case."""
        description.append_text("the element is invisible")

    def describe_match(
        self, _: WebElement | None, match_description: Description
    ) -> None:
        """Describe the matching case."""
        match_description.append_text("it was invisible")

    def describe_mismatch(
        self, _: WebElement | None, mismatch_description: Description
    ) -> None:
        """Describe the failing case."""
        mismatch_description.append_text("was not invisible")


def is_invisible_element() -> IsInvisibleElement:
    """This matcher matches any element that is invisible."""
    return IsInvisibleElement()
