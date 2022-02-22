"""
Hold down a specific key or the left mouse button, optionally on an element.
"""

import platform
from typing import Optional

from screenpy import Actor
from screenpy.exceptions import UnableToAct
from screenpy.pacing import beat
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from ..speech_tools import KEY_NAMES
from ..target import Target


class HoldDown:
    """Hold down the specified key or left mouse button.

    This Action can only be used with :class:`~screenpy_selenium.actions.Chain`,
    and it is expected that a :class:`~screenpy_selenium.actions.Release` Action
    occurs later in the Chain to release the held key or button.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        the_actor.attempts_to(Chain(HoldDown(Keys.SHIFT))

        the_actor.attempts_to(Chain(HoldDown.command_or_control_key()))

        the_actor.attempts_to(
            Chain(HoldDown.left_mouse_button().on_the(DRAGGABLE_BOX))
        )
    """

    target: Optional[Target]

    @staticmethod
    def command_or_control_key() -> "HoldDown":
        """
        A convenience method that figures out what operating system the Actor
        is using and directs the Actor which execution key to hold down.
        """
        if platform.system() == "Darwin":
            return HoldDown(Keys.COMMAND)
        return HoldDown(Keys.CONTROL)

    @staticmethod
    def left_mouse_button() -> "HoldDown":
        """Hold down the left mouse button."""
        return HoldDown(lmb=True)

    def on_the(self, target: Target) -> "HoldDown":
        """Target an element to hold down left click on."""
        self.target = target
        return self

    on = on_the

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return f"Hold down {self.description}."

    @beat("  Hold down {description}!")
    def add_to_chain(self, the_actor: Actor, the_chain: ActionChains) -> None:
        """Add the HoldDown Action to a Chain of Actions."""
        if self.lmb:
            element = self.target.found_by(the_actor) if self.target else None
            the_chain.click_and_hold(on_element=element)
        elif self.key is not None:
            the_chain.key_down(self.key)
        else:
            raise UnableToAct("HoldDown must be told what to hold down.")

    def __init__(self, key: Optional[str] = None, lmb: bool = False) -> None:
        self.key = key
        self.lmb = lmb
        self.target = None
        self.description = "LEFT MOUSE BUTTON" if lmb else KEY_NAMES[key]
