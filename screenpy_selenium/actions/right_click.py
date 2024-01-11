"""Right-click on an element, or wherever the cursor currently is."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type, TypeVar

from screenpy.pacing import beat
from selenium.webdriver.common.action_chains import ActionChains

from ..abilities import BrowseTheWeb

if TYPE_CHECKING:
    from screenpy import Actor

    from ..target import Target

SelfRightClick = TypeVar("SelfRightClick", bound="RightClick")


class RightClick:
    """Right-click on an element, or wherever the cursor currently is.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        the_actor.attempts_to(RightClick.on_the(HERO_IMAGE))

        the_actor.attempts_to(Chain(RightClick()))

    *Note*: Most of the time, the context menu that appears after a user
    right-clicks is not interactable through Selenium, because it is an
    application-level menu. A website will need to have implemented a custom
    context menu made of web elements to be able to interact with it.
    """

    target: Optional[Target]

    @classmethod
    def on_the(cls: Type[SelfRightClick], target: Target) -> SelfRightClick:
        """Target an element to right-click on.

        Aliases:
            * :meth:`~screenpy_selenium.actions.RightClick.on`
            * :meth:`~screenpy_selenium.actions.RightClick.on_the_first_of_the`
        """
        return cls(target=target)

    @classmethod
    def on(cls: Type[SelfRightClick], target: Target) -> SelfRightClick:
        """Alias for :meth:`~screenpy_selenium.actions.RightClick.on_the`."""
        return cls.on_the(target=target)

    @classmethod
    def on_the_first_of_the(
        cls: Type[SelfRightClick], target: Target
    ) -> SelfRightClick:
        """Alias for :meth:`~screenpy_selenium.actions.RightClick.on_the`."""
        return cls.on_the(target=target)

    def _add_action_to_chain(
        self: SelfRightClick, the_actor: Actor, the_chain: ActionChains
    ) -> None:
        """Private method to add this Action to the chain."""
        if self.target is not None:
            the_element = self.target.found_by(the_actor)
        else:
            the_element = None

        the_chain.context_click(on_element=the_element)

    def describe(self: SelfRightClick) -> str:
        """Describe the Action in present tense."""
        return f"Right-click{self.description}."

    @beat("{} right-clicks{description}.")
    def perform_as(self: SelfRightClick, the_actor: Actor) -> None:
        """Direct the Actor to right-click on the element."""
        browser = the_actor.ability_to(BrowseTheWeb).browser
        the_chain = ActionChains(browser)  # type: ignore[arg-type]
        self._add_action_to_chain(the_actor, the_chain)
        the_chain.perform()

    @beat("Right-click{description}!")
    def add_to_chain(
        self: SelfRightClick, the_actor: Actor, the_chain: ActionChains
    ) -> None:
        """Add the RightClick Action to a Chain of Actions."""
        self._add_action_to_chain(the_actor, the_chain)

    def __init__(self: SelfRightClick, target: Optional[Target] = None) -> None:
        self.target = target
        self.description = f" on the {target}" if target is not None else ""
