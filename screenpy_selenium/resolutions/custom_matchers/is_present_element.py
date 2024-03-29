"""
A matcher that matches a present element.

For example:

    assert_that(driver.find_element_by_id("search"), is_present_element())
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from hamcrest.core.base_matcher import BaseMatcher
from selenium.webdriver.remote.webelement import WebElement

if TYPE_CHECKING:
    from hamcrest.core.description import Description


class IsPresentElement(BaseMatcher[Optional[WebElement]]):
    """Matches an element to be a present WebElement."""

    def _matches(self, item: WebElement | None) -> bool:
        if item is None:
            return False
        return isinstance(item, WebElement)

    def describe_to(self, description: Description) -> None:
        """Describe the passing case."""
        description.append_text("the element is present")

    def describe_match(
        self, _: WebElement | None, match_description: Description
    ) -> None:
        """Describe the matching case."""
        match_description.append_text("it was present")

    def describe_mismatch(
        self, _: WebElement | None, mismatch_description: Description
    ) -> None:
        """Describe the failing case."""
        mismatch_description.append_text("was not present")


def is_present_element() -> IsPresentElement:
    """This matcher matches any element that is present."""
    return IsPresentElement()
