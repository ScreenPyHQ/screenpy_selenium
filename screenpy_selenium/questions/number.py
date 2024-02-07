"""Investigate how many of an element are present on the page."""

from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy.pacing import beat
from typing_extensions import Self

if TYPE_CHECKING:
    from screenpy import Actor

    from ..target import Target


class Number:
    """Ask how many of a certain element are on the page.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        the_actor.should(See.the(Number.of(SEARCH_RESULTS), IsEqualTo(4)))
    """

    @classmethod
    def of(cls, target: Target) -> Self:
        """Target the element to be counted."""
        return cls(target=target)

    def describe(self) -> str:
        """Describe the Question."""
        return f"The number of {self.target}."

    @beat("{} counts the number of {target}.")
    def answered_by(self, the_actor: Actor) -> int:
        """Direct the Actor to count the elements."""
        return len(self.target.all_found_by(the_actor))

    def __init__(self, target: Target) -> None:
        self.target = target
