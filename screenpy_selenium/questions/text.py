"""Investigate the text of an element or many elements."""
from __future__ import annotations

from typing import List, Type, TypeVar, Union

from screenpy import Actor
from screenpy.pacing import beat

from ..target import Target

SelfText = TypeVar("SelfText", bound="Text")


class Text:
    """Ask what text appears in an element or elements.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        the_actor.should(
            See.the(Text.of(THE_WELCOME_HEADER), ReadsExactly("Welcome!"))
        )

        the_actor.should(
            See.the(Text.of_all(SEARCH_RESULTS), ContainsTheItem("Rear Window"))
        )
    """

    target: Target
    multi: bool

    @classmethod
    def of_the(cls: Type[SelfText], target: Target) -> SelfText:
        """Target the element to extract the text from.

        Aliases:
            * :meth:`~screenpy_selenium.actions.Text.of`
            * :meth:`~screenpy_selenium.actions.Text.of_the_first_of_the`
        """
        return cls(target=target)

    @classmethod
    def of(cls: Type[SelfText], target: Target) -> SelfText:
        """Alias of :meth:`~screenpy_selenium.actions.Text.of_the`."""
        return cls.of_the(target=target)

    @classmethod
    def of_the_first_of_the(cls: Type[SelfText], target: Target) -> SelfText:
        """Alias of :meth:`~screenpy_selenium.actions.Text.of_the`."""
        return cls.of_the(target=target)

    @classmethod
    def of_all(cls: Type[SelfText], multi_target: Target) -> SelfText:
        """Target the elements, plural, to extract the text from."""
        return cls(target=multi_target, multi=True)

    def describe(self: SelfText) -> str:
        """Describe the Question."""
        return f"The text from the {self.target}."

    @beat("{} reads the text from the {target}.")
    def answered_by(self: SelfText, the_actor: Actor) -> Union[str, List[str]]:
        """Direct the Actor to read off the text of the element(s)."""
        if self.multi:
            return [e.text for e in self.target.all_found_by(the_actor)]
        return self.target.found_by(the_actor).text

    def __init__(self: SelfText, target: Target, multi: bool = False) -> None:
        self.target = target
        self.multi = multi
