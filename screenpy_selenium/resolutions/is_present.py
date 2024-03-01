"""Matches a present WebElement."""

from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy import beat

from .custom_matchers import is_present_element

if TYPE_CHECKING:
    from .custom_matchers.is_present_element import IsPresentElement


class IsPresent:
    """Match on a present element.

    Examples::

        the_actor.should(See.the(Element(HIDDEN_BUTTON), IsPresent()))
        the_actor.should(See.the(Element(DISABLED_BUTTON), Exists()))
        the_actor.should(See.the(Element(BUTTON), DoesNot(Exist())))
    """

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return "present"

    @beat("... hoping it's present.")
    def resolve(self) -> IsPresentElement:
        """Produce the Matcher to make the assertion."""
        return is_present_element()
