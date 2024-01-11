"""Investigate an element on the browser page."""

from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy.pacing import beat

from ..exceptions import TargetingError

if TYPE_CHECKING:
    from screenpy import Actor
    from selenium.webdriver.remote.webelement import WebElement

    from ..target import Target


class Element:
    """Ask to retrieve a specific element.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        the_actor.should(See.the(Element(WELCOME_BANNER), IsVisible()))
    """

    caught_exception: TargetingError | None

    def describe(self) -> str:
        """Describe the Question."""
        return f"The {self.target}."

    @beat("{} inspects the {target}.")
    def answered_by(self, the_actor: Actor) -> WebElement | None:
        """Direct the Actor to find the element."""
        try:
            return self.target.found_by(the_actor)
        except TargetingError as exc:
            self.caught_exception = exc
            return None

    def __init__(self, target: Target) -> None:
        self.target = target
        self.caught_exception = None
