"""Matches a disabled WebElement."""

from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy import beat

from .custom_matchers import is_disabled_element

if TYPE_CHECKING:
    from .custom_matchers.is_disabled_element import IsDisabledElement


class IsDisabled:
    """Match on a disabled element.

    Examples::

        the_actor.will(See.the(Element(LOGIN_BUTTON), IsDisabled()))
    """

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return "disabled"

    @beat("... hoping it's disabled.")
    def resolve(self) -> IsDisabledElement:
        """Produce the Matcher to make the assertion."""
        return is_disabled_element()
