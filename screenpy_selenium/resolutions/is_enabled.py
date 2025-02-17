"""Matches a enabled WebElement."""

from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy import beat

from .custom_matchers import is_enabled_element

if TYPE_CHECKING:
    from .custom_matchers.is_enabled_element import IsEnabledElement


class IsEnabled:
    """Match on a enabled element.

    Examples::

        the_actor.will(See.the(Element(LOGIN_BUTTON), IsEnabled()))
    """

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return "enabled"

    @beat("... hoping it's enabled.")
    def resolve(self) -> IsEnabledElement:
        """Produce the Matcher to make the assertion."""
        return is_enabled_element()
