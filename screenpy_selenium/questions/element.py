"""
Investigate an element on the browser page.
"""

from typing import Optional

from screenpy import Actor
from screenpy.pacing import beat
from selenium.webdriver.remote.webelement import WebElement

from ..exceptions import TargetingError
from ..target import Target


class Element:
    """Ask to retrieve a specific element.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        the_actor.should(See.the(Element(WELCOME_BANNER), IsVisible()))
    """

    def describe(self) -> str:
        """Describe the Question."""
        return f"The {self.target}."

    @beat("{} inspects the {target}.")
    def answered_by(self, the_actor: Actor) -> Optional[WebElement]:
        """Direct the Actor to find the element."""
        try:
            return self.target.found_by(the_actor)
        except TargetingError:
            return None

    def __init__(self, target: Target) -> None:
        self.target = target
