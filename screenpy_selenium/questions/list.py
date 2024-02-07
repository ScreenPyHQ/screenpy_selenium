"""Investigate one or more elements."""

from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy.pacing import beat
from typing_extensions import Self

if TYPE_CHECKING:
    from screenpy import Actor
    from selenium.webdriver.remote.webdriver import WebElement

    from ..target import Target


class List:
    """Ask for a list of elements.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        the_actor.should(See.the(List.of(CONFETTI), IsEmpty()))
    """

    @classmethod
    def of_the(cls, target: Target) -> Self:
        """Target the element(s) to list.

        Aliases:
            * :meth:`~screenpy_selenium.actions.List.of_all_the`
            * :meth:`~screenpy_selenium.actions.List.of_all`
            * :meth:`~screenpy_selenium.actions.List.of`
        """
        return cls(target=target)

    @classmethod
    def of_all_the(cls, target: Target) -> Self:
        """Alias for :meth:`~screenpy_selenium.actions.List.of_the`."""
        return cls.of_the(target=target)

    @classmethod
    def of_all(cls, target: Target) -> Self:
        """Alias for :meth:`~screenpy_selenium.actions.List.of_the`."""
        return cls.of_the(target=target)

    @classmethod
    def of(cls, target: Target) -> Self:
        """Alias for :meth:`~screenpy_selenium.actions.List.of_the`."""
        return cls.of_the(target=target)

    def describe(self) -> str:
        """Describe the Question."""
        return f"The list of {self.target}."

    @beat("{} lists off the {target}.")
    def answered_by(self, the_actor: Actor) -> list[WebElement]:
        """Direct the Actor to rattle off the specified elements."""
        return self.target.all_found_by(the_actor)

    def __init__(self, target: Target) -> None:
        self.target = target
