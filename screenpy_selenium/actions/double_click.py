"""Double-click on an element, or wherever the cursor currently is."""

from __future__ import annotations

from typing import Optional, Type, TypeVar

from screenpy.actor import Actor
from screenpy.pacing import beat
from selenium.webdriver.common.action_chains import ActionChains

from ..abilities import BrowseTheWeb
from ..target import Target

SelfDoubleClick = TypeVar("SelfDoubleClick", bound="DoubleClick")


class DoubleClick:
    """Double-click on an element, or wherever the cursor currently is.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        the_actor.attempts_to(DoubleClick.on_the(FILE_ICON))

        the_actor.attempts_to(Chain(DoubleClick()))
    """

    target: Optional[Target]

    @classmethod
    def on_the(cls: Type[SelfDoubleClick], target: Target) -> SelfDoubleClick:
        """
        Target the element to double-click on.

        Aliases:
            * :meth:`~screenpy_selenium.actions.DoubleClick.on`
            * :meth:`~screenpy_selenium.actions.DoubleClick.on_the_first_of_the`
        """
        return cls(target=target)

    @classmethod
    def on(cls: Type[SelfDoubleClick], target: Target) -> SelfDoubleClick:
        """Alias for :meth:`~screenpy_selenium.actions.DoubleClick.on_the`."""
        return cls.on_the(target=target)

    @classmethod
    def on_the_first_of_the(
        cls: Type[SelfDoubleClick], target: Target
    ) -> SelfDoubleClick:
        """Alias for :meth:`~screenpy_selenium.actions.DoubleClick.on_the`."""
        return cls.on_the(target=target)

    def _add_action_to_chain(
        self: SelfDoubleClick, the_actor: Actor, the_chain: ActionChains
    ) -> None:
        """Private method to add this Action to the chain."""
        if self.target is not None:
            the_element = self.target.found_by(the_actor)
        else:
            the_element = None

        the_chain.double_click(on_element=the_element)

    def describe(self: SelfDoubleClick) -> str:
        """Describe the Action in present tense."""
        return f"Double-click{self.description}."

    @beat("{} double-clicks{description}.")
    def perform_as(self: SelfDoubleClick, the_actor: Actor) -> None:
        """Direct the Actor to double-click on the element."""
        browser = the_actor.ability_to(BrowseTheWeb).browser
        the_chain = ActionChains(browser)  # type: ignore[arg-type]
        self._add_action_to_chain(the_actor, the_chain)
        the_chain.perform()

    @beat("Double-click{description}!")
    def add_to_chain(
        self: SelfDoubleClick, the_actor: Actor, the_chain: ActionChains
    ) -> None:
        """Add the DoubleClick Action to a Chain of Actions."""
        self._add_action_to_chain(the_actor, the_chain)

    def __init__(self: SelfDoubleClick, target: Optional[Target] = None) -> None:
        self.target = target
        self.description = f" on the {target}" if target is not None else ""
