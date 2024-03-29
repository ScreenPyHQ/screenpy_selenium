"""A meta-Action to group a series of chainable Actions together."""

from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy.exceptions import UnableToAct
from screenpy.pacing import beat
from selenium.webdriver.common.action_chains import ActionChains

from ..abilities import BrowseTheWeb
from ..configuration import settings
from ..protocols import Chainable

if TYPE_CHECKING:
    from screenpy.actor import Actor


class Chain:
    """Group a series of chainable Actions together.

    A Chain Action is expected to be instantiated with a list of Actions to
    perform in a series.

    *Note*: Several Actions cannot be Chained, and will raise an exception.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        the_actor.attempts_to(
            Chain(Hover.on_the(MENU_ICON), Click.on_the(SUBMENU_LINK))
        )
    """

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return "Perform a thrilling chain of actions."

    @beat("{} performs a thrilling chain of Actions!")
    def perform_as(self, the_actor: Actor) -> None:
        """Choreograph the Actions and direct the Actor to perform the chain."""
        browser = the_actor.ability_to(BrowseTheWeb).browser
        the_chain = ActionChains(browser, duration=settings.CHAIN_DURATION)

        for action in self.actions:
            if not isinstance(action, Chainable):
                msg = f"The {action.__class__.__name__} Action cannot be chained."
                raise UnableToAct(msg)
            action.add_to_chain(the_actor, the_chain)
        the_chain.perform()

    def __init__(self, *actions: Chainable) -> None:
        self.actions = actions
