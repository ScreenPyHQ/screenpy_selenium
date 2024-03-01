"""Matches against an invisible WebElement."""

from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy import beat

from .custom_matchers import is_invisible_element

if TYPE_CHECKING:
    from .custom_matchers.is_invisible_element import IsInvisibleElement


class IsInvisible:
    """Match on an invisible element.

    Examples::

        the_actor.should(See.the(Element(WELCOME_BANNER), IsInvisible()))
    """

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return "invisible"

    @beat("... hoping it's invisible.")
    def resolve(self) -> IsInvisibleElement:
        """Produce the Matcher to make the assertion."""
        return is_invisible_element()
