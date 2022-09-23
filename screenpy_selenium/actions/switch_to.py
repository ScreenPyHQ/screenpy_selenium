"""
Switch the driver's frame of reference.
"""

from typing import Optional, Type, TypeVar

from screenpy.actor import Actor
from screenpy.pacing import beat

from ..abilities import BrowseTheWeb
from ..target import Target

SelfSwitchTo = TypeVar("SelfSwitchTo", bound="SwitchTo")


class SwitchTo:
    """Switch to an element, most likely an iframe, or back to default.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        the_actor.attempts_to(SwitchTo(THE_ORDERS_FRAME))

        the_actor.attempts_to(SwitchTo.the(ORDERS_FRAME))

        the_actor.attempts_to(SwitchTo.default())
    """

    @classmethod
    def the(cls: Type[SelfSwitchTo], target: Target) -> SelfSwitchTo:
        """Target an element, probably an iframe, to switch to."""
        return cls(target=target, frame_to_log=str(target))

    @classmethod
    def default(cls: Type[SelfSwitchTo]) -> SelfSwitchTo:
        """Switch back to the default frame, the browser window."""
        return cls(target=None, frame_to_log="default frame")

    def describe(self: SelfSwitchTo) -> str:
        """Describe the Action in present tense."""
        return f"Switch to the {self.frame_to_log}."

    @beat("{} switches to the {frame_to_log}.")
    def perform_as(self: SelfSwitchTo, the_actor: Actor) -> None:
        """Direct the Actor to switch to an element or back to default."""
        browser = the_actor.ability_to(BrowseTheWeb).browser
        if self.target is None:
            browser.switch_to.default_content()
        else:
            browser.switch_to.frame(self.target.found_by(the_actor))

    def __init__(
        self: SelfSwitchTo, target: Optional[Target], frame_to_log: str
    ) -> None:
        self.target = target
        self.frame_to_log = frame_to_log
