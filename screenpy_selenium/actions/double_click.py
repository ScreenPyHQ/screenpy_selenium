"""
Double-click on an element, or wherever the cursor currently is.
"""

from typing import Optional

from screenpy.actor import Actor
from screenpy.pacing import beat
from selenium.webdriver.common.action_chains import ActionChains

from ..abilities import BrowseTheWeb
from ..target import Target


class DoubleClick:
    """Double-click on an element, or wherever the cursor currently is.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        the_actor.attempts_to(DoubleClick.on_the(FILE_ICON))

        the_actor.attempts_to(Chain(DoubleClick()))
    """

    target: Optional[Target]

    @staticmethod
    def on_the(target: Target) -> "DoubleClick":
        """Target the element to double-click on."""
        return DoubleClick(target=target)

    on = on_the_first_of_the = on_the

    def _add_action_to_chain(self, the_actor: Actor, the_chain: ActionChains) -> None:
        """Private method to add this Action to the chain."""
        if self.target is not None:
            the_element = self.target.found_by(the_actor)
        else:
            the_element = None

        the_chain.double_click(on_element=the_element)

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return f"Double-click{self.description}."

    @beat("{} double-clicks{description}.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to double-click on the element."""
        browser = the_actor.ability_to(BrowseTheWeb).browser
        the_chain = ActionChains(browser)
        self._add_action_to_chain(the_actor, the_chain)
        the_chain.perform()

    @beat("  Double-click{description}!")
    def add_to_chain(self, the_actor: Actor, the_chain: ActionChains) -> None:
        """Add the DoubleClick Action to a Chain of Actions."""
        self._add_action_to_chain(the_actor, the_chain)

    def __init__(self, target: Optional[Target] = None) -> None:
        self.target = target
        self.description = f" on the {target}" if target is not None else ""
