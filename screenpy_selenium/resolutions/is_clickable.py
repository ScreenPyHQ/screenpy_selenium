"""Matches a clickable WebElement."""

from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy import beat

from .custom_matchers import is_clickable_element

if TYPE_CHECKING:
    from .custom_matchers.is_clickable_element import IsClickableElement


class IsClickable:
    """Match on a clickable element.

    Examples::

        the_actor.should(See.the(Element(LOGIN_BUTTON), IsClickable()))
    """

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return "clickable"

    @beat("... hoping it's clickable.")
    def resolve(self) -> IsClickableElement:
        """Produce the Matcher to make the assertion."""
        return is_clickable_element()
