"""Matches against a visible WebElement."""

from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy import beat

from .custom_matchers import is_visible_element

if TYPE_CHECKING:
    from .custom_matchers.is_visible_element import IsVisibleElement


class IsVisible:
    """Match on a visible element.

    Examples::

        the_actor.should(See.the(Element(WELCOME_BANNER), IsVisible()))
    """

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return "visible"

    @beat("... hoping it's visible.")
    def resolve(self) -> IsVisibleElement:
        """Produce the Matcher to make the assertion."""
        return is_visible_element()
