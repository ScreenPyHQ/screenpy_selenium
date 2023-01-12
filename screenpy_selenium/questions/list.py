"""
Investigate one or more elements.
"""

from typing import List as ListType
from typing import Type, TypeVar

from screenpy import Actor
from screenpy.pacing import beat
from selenium.webdriver.remote.webdriver import WebElement

from ..target import Target

SelfList = TypeVar("SelfList", bound="List")


class List:
    """Ask for a list of elements.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        the_actor.should(See.the(List.of(CONFETTI), IsEmpty()))
    """

    @classmethod
    def of_the(cls: Type[SelfList], target: Target) -> SelfList:
        """Target the element(s) to list.

        Aliases:
            * :meth:`~screenpy_selenium.actions.List.of_all_the`
            * :meth:`~screenpy_selenium.actions.List.of_all`
            * :meth:`~screenpy_selenium.actions.List.of`
        """
        return cls(target=target)

    @classmethod
    def of_all_the(cls: Type[SelfList], target: Target) -> SelfList:
        """Alias for :meth:`~screenpy_selenium.actions.List.of_the`"""
        return cls.of_the(target=target)

    @classmethod
    def of_all(cls: Type[SelfList], target: Target) -> SelfList:
        """Alias for :meth:`~screenpy_selenium.actions.List.of_the`"""
        return cls.of_the(target=target)

    @classmethod
    def of(cls: Type[SelfList], target: Target) -> SelfList:
        """Alias for :meth:`~screenpy_selenium.actions.List.of_the`"""
        return cls.of_the(target=target)

    def describe(self: SelfList) -> str:
        """Describe the Question."""
        return f"The list of {self.target}."

    @beat("{} lists off the {target}.")
    def answered_by(self: SelfList, the_actor: Actor) -> ListType[WebElement]:
        """Direct the Actor to rattle off the specified elements."""
        return self.target.all_found_by(the_actor)

    def __init__(self: SelfList, target: Target) -> None:
        self.target = target
