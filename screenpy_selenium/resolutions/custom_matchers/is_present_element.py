"""
A matcher that matches a present element. For example:

    assert_that(driver.find_element_by_id("search"), is_present_element())
"""

from typing import Optional

from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description
from selenium.webdriver.remote.webelement import WebElement


class IsPresentElement(BaseMatcher[Optional[WebElement]]):
    """
    Matches an element to be a present WebElement.
    """

    def _matches(self, item: Optional[WebElement]) -> bool:
        if item is None:
            return False
        return isinstance(item, WebElement)

    def describe_to(self, description: Description) -> None:
        """Describe the passing case."""
        description.append_text("the element is present")

    def describe_match(
        self, item: Optional[WebElement], match_description: Description
    ) -> None:
        match_description.append_text("it was present")

    def describe_mismatch(
        self, item: Optional[WebElement], mismatch_description: Description
    ) -> None:
        """Describe the failing case."""
        mismatch_description.append_text("was not present")


def is_present_element() -> IsPresentElement:
    """This matcher matches any element that is present"""
    return IsPresentElement()
