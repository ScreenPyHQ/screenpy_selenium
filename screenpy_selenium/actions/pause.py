"""
Pause just like in ScreenPy, but also be able to do it in a Chain!
"""

from screenpy import Actor
from screenpy.actions import Pause as BasePause
from screenpy.pacing import beat
from selenium.webdriver.common.action_chains import ActionChains


class Pause(BasePause):
    """An extension of ScreenPy's Pause which can also be Chained.

    The Actor will pause for a contemplative moment, taking no actions until
    the duration has expired.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        the_actor.attempts_to(
            Pause.for_(300).seconds_because("it's time for their break.")
        )

        the_actor.attempts_to(
            Chain(
                MoveMouse.to_the(DROPDOWN_MENU),
                Pause.for_(2).seconds_because(
                    "the fancy menu slide-in animation needs to finish."
                ),
                Click.on_the(SUBMENU_OPTION),
            )
        )
    """

    @beat("  Pause for {number} {unit} ({reason})!")
    def add_to_chain(self, _: Actor, the_chain: ActionChains) -> None:
        """Add the Pause Action to a Chain of Actions."""
        the_chain.pause(self.time)
