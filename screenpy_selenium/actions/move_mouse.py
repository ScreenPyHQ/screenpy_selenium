"""Move the mouse to a specific element, or by an offset."""

from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy.exceptions import UnableToAct
from screenpy.pacing import beat
from selenium.webdriver.common.action_chains import ActionChains

from ..abilities import BrowseTheWeb
from ..configuration import settings

if TYPE_CHECKING:
    from screenpy.actor import Actor
    from typing_extensions import Self

    from ..target import Target


class MoveMouse:
    """Move the mouse to a specific element or by a pixel offset.

    The x and y offsets are measured in pixels, with the "origin" at the top
    left of the screen.

    * To move left, give a negative x_offset.
    * To move right, give a positive x_offset.
    * To move up, give a negative y_offset.
    * To move down, give a positive y_offset.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        the_actor.attempts_to(MoveMouse.to_the(HAMBURGER_MENU))

        the_actor.attempts_to(MoveMouse.by_offset(500, -200))

        the_actor.attempts_to(
            Chain(MoveMouse.to_the(HAMBURGER_MENU).with_offset(500, -200))
        )
    """

    offset: tuple[int, int] | None
    target: Target | None
    description: str

    @classmethod
    def to_the(cls, target: Target) -> Self:
        """
        Target an element to move the mouse to.

        Aliases:
            * :meth:`~screenpy_selenium.actions.MoveMouse.on_the`
            * :meth:`~screenpy_selenium.actions.MoveMouse.over_the`
            * :meth:`~screenpy_selenium.actions.MoveMouse.over_the_first_of_the`
            * :meth:`~screenpy_selenium.actions.MoveMouse.to_the_first_of_the`
        """
        return cls(target=target, description=f"to the {target}")

    @classmethod
    def on_the(cls, target: Target) -> Self:
        """Alias for :meth:`~screenpy_selenium.actions.MoveMouse.to_the`."""
        return cls.to_the(target=target)

    @classmethod
    def over_the(cls, target: Target) -> Self:
        """Alias for :meth:`~screenpy_selenium.actions.MoveMouse.to_the`."""
        return cls.to_the(target=target)

    @classmethod
    def over_the_first_of_the(cls, target: Target) -> Self:
        """Alias for :meth:`~screenpy_selenium.actions.MoveMouse.to_the`."""
        return cls.to_the(target=target)

    @classmethod
    def to_the_first_of_the(cls, target: Target) -> Self:
        """Alias for :meth:`~screenpy_selenium.actions.MoveMouse.to_the`."""
        return cls.to_the(target=target)

    @classmethod
    def by_offset(cls, x_offset: int, y_offset: int) -> Self:
        """Specify the offset by which to move the mouse."""
        return cls(
            offset=(x_offset, y_offset),
            description=f"by an offset of ({x_offset}, {y_offset})",
        )

    def with_offset(self, x_offset: int, y_offset: int) -> Self:
        """Specify the mouse should be moved to the element with an offset."""
        self.offset = (x_offset, y_offset)
        self.description += f" offset by ({x_offset}, {y_offset})"
        return self

    def _add_action_to_chain(self, the_actor: Actor, the_chain: ActionChains) -> None:
        """Private method to add this Action to the chain."""
        if self.target is not None and self.offset is not None:
            the_chain.move_to_element_with_offset(
                self.target.found_by(the_actor), *self.offset
            )
        elif self.target is not None:
            the_chain.move_to_element(self.target.found_by(the_actor))
        elif self.offset is not None:
            the_chain.move_by_offset(*self.offset)
        else:
            msg = (
                "MoveMouse was given neither coordinates nor a Target. "
                "Supply one of these using MoveMouse.by_offset or MoveMouse.to_the."
            )
            raise UnableToAct(msg)

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return f"Move the mouse {self.description}."

    @beat("{} moves the mouse {description}.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to move the mouse."""
        browser = the_actor.ability_to(BrowseTheWeb).browser
        the_chain = ActionChains(browser, duration=settings.CHAIN_DURATION)
        self._add_action_to_chain(the_actor, the_chain)
        the_chain.perform()

    @beat("Move the mouse {description}!")
    def add_to_chain(self, the_actor: Actor, the_chain: ActionChains) -> None:
        """Add the MoveMouse Action to a Chain of Actions."""
        self._add_action_to_chain(the_actor, the_chain)

    def __init__(
        self,
        offset: tuple[int, int] | None = None,
        target: Target | None = None,
        description: str = "",
    ) -> None:
        self.offset = offset
        self.target = target
        self.description = description
