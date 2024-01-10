"""Investigate how many of an element are present on the page."""

from typing import Type, TypeVar

from screenpy import Actor
from screenpy.pacing import beat

from ..target import Target

SelfNumber = TypeVar("SelfNumber", bound="Number")


class Number:
    """Ask how many of a certain element are on the page.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        the_actor.should(See.the(Number.of(SEARCH_RESULTS), IsEqualTo(4)))
    """

    @classmethod
    def of(cls: Type[SelfNumber], target: Target) -> SelfNumber:
        """Target the element to be counted."""
        return cls(target=target)

    def describe(self: SelfNumber) -> str:
        """Describe the Question."""
        return f"The number of {self.target}."

    @beat("{} counts the number of {target}.")
    def answered_by(self: SelfNumber, the_actor: Actor) -> int:
        """Direct the Actor to count the elements."""
        return len(self.target.all_found_by(the_actor))

    def __init__(self: SelfNumber, target: Target) -> None:
        self.target = target
