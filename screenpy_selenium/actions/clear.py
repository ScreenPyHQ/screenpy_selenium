"""Clear text from an input."""
from typing import Type, TypeVar

from screenpy.actor import Actor
from screenpy.exceptions import DeliveryError
from screenpy.pacing import beat
from selenium.common.exceptions import WebDriverException

from ..target import Target

SelfClear = TypeVar("SelfClear", bound="Clear")


class Clear:
    """Clear the text from an input field.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        the_actor.attempts_to(Clear.the_text_from_the(NAME_INPUT))
    """

    @classmethod
    def the_text_from_the(cls: Type[SelfClear], target: Target) -> SelfClear:
        """
        Specify the Target from which to clear the text.

        Aliases:
            * :meth:`~screenpy_selenium.actions.Clear.the_text_from`
            * :meth:`~screenpy_selenium.actions.Clear.the_text_from_the_first_of_the`
        """
        return cls(target=target)

    @classmethod
    def the_text_from(cls: Type[SelfClear], target: Target) -> SelfClear:
        """Alias for :meth:`~screenpy_selenium.actions.Clear.the_text_from_the`."""
        return cls.the_text_from_the(target=target)

    @classmethod
    def the_text_from_the_first_of_the(
        cls: Type[SelfClear], target: Target
    ) -> SelfClear:
        """Alias for :meth:`~screenpy_selenium.actions.Clear.the_text_from_the`."""
        return cls.the_text_from_the(target=target)

    def describe(self: SelfClear) -> str:
        """Describe the Action in present tense."""
        return f"Clear the text from the {self.target}."

    @beat("{} clears text from the {target}.")
    def perform_as(self: SelfClear, the_actor: Actor) -> None:
        """Direct the Actor to clear the text from the input field."""
        element = self.target.found_by(the_actor)

        try:
            element.clear()
        except WebDriverException as e:
            msg = (
                "Encountered an issue while attempting to clear "
                f"{self.target}: {e.__class__.__name__}"
            )
            raise DeliveryError(msg) from e

    def __init__(self: SelfClear, target: Target) -> None:
        self.target = target
