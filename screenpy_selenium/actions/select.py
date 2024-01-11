"""Select an item from a multi-selection field or dropdown."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional, TypeVar, Union

from screenpy.exceptions import DeliveryError, UnableToAct
from screenpy.pacing import beat
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import Select as SeleniumSelect

if TYPE_CHECKING:
    from screenpy import Actor

    from ..target import Target

SelfSelectByText = TypeVar("SelfSelectByText", bound="SelectByText")
SelfSelectByIndex = TypeVar("SelfSelectByIndex", bound="SelectByIndex")
SelfSelectByValue = TypeVar("SelfSelectByValue", bound="SelectByValue")


class Select:
    """Select an option from a dropdown menu.

    This is an entry point that will create the correct specific Select Action
    to be used, depending on how the option needs to be selected.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        the_actor.attempts_to(
            Select.the_option_named("January").from_the(MONTH_DROPDOWN)
        )

        the_actor.attempts_to(
            Select.the_option_at_index(0).from_the(MONTH_DROPDOWN)
        )

        the_actor.attempts_to(
            Select.the_option_with_value("jan").from_the(MONTH_DROPDOWN)
        )
    """

    @staticmethod
    def the_option_named(text: str) -> "SelectByText":
        """Select the option by its text."""
        return SelectByText(text)

    @staticmethod
    def the_option_at_index(index: Union[int, str]) -> "SelectByIndex":
        """Select the option by its index. This index is 0-based."""
        return SelectByIndex(index)

    @staticmethod
    def the_option_with_value(value: Union[int, str]) -> "SelectByValue":
        """Select the option by its value."""
        return SelectByValue(value)


class SelectByText:
    """Select an option in a dropdown or multi-select field by its text.

    This Action will probably not be used directly, rather it will be returned
    by calling :meth:`~screenpy_selenium.actions.Select.the_option_named`.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`
    """

    target: Optional[Target]
    text: str

    def from_the(self: SelfSelectByText, target: Target) -> SelfSelectByText:
        """Target the dropdown or multi-select field to select the option from."""
        self.target = target
        return self

    from_ = from_the_first_of_the = from_the

    def describe(self: SelfSelectByText) -> str:
        """Describe the Action in present tense."""
        return f'Select the option "{self.text}" from the {self.target}.'

    @beat('{} selects the option "{text}" from the {target}.')
    def perform_as(self: SelfSelectByText, the_actor: Actor) -> None:
        """Direct the Actor to select the option by its text."""
        if self.target is None:
            msg = (
                "Target was not provided for SelectByText. Provide a Target using the "
                ".from_() or .from_the() methods."
            )
            raise UnableToAct(msg)

        element = self.target.found_by(the_actor)
        select = SeleniumSelect(element)
        try:
            select.select_by_visible_text(self.text)
        except WebDriverException as e:
            msg = (
                "Encountered an issue while attempting to select the option with text "
                f"'{self.text}' from {self.target}: {e.__class__.__name__}"
            )
            raise DeliveryError(msg) from e

    def __init__(
        self: SelfSelectByText, text: str, target: Optional[Target] = None
    ) -> None:
        self.target = target
        self.text = text


class SelectByIndex:
    """Select an option in a dropdown or multi-select field by its index.

    This Action will probably not be used directly, rather it will be returned
    by calling :meth:`~screenpy_selenium.actions.Select.the_option_at_index`.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`
    """

    target: Optional[Target]
    index: int

    def from_the(self: SelfSelectByIndex, target: Target) -> SelfSelectByIndex:
        """Target the dropdown or multi-select field to select the option from."""
        self.target = target
        return self

    from_ = from_the_first_of_the = from_the

    def describe(self: SelfSelectByIndex) -> str:
        """Describe the Action in present tense."""
        return f"Select the option at index {self.index} from the {self.target}."

    @beat("{} selects the option at index {index} from the {target}.")
    def perform_as(self: SelfSelectByIndex, the_actor: Actor) -> None:
        """Direct the Actor to select the option using its index."""
        if self.target is None:
            msg = (
                "Target was not provided for SelectByIndex. Provide a Target using the "
                ".from_() or .from_the() methods."
            )
            raise UnableToAct(msg)

        element = self.target.found_by(the_actor)
        select = SeleniumSelect(element)
        try:
            select.select_by_index(self.index)
        except WebDriverException as e:
            msg = (
                "Encountered an issue while attempting to select the option at index "
                f"{self.index} from {self.target}: {e.__class__.__name__}"
            )
            raise DeliveryError(msg) from e

    def __init__(
        self: SelfSelectByIndex, index: Union[int, str], target: Optional[Target] = None
    ) -> None:
        self.target = target
        self.index = int(index)


class SelectByValue:
    """Select an option in a dropdown or multi-select field by its value.

    This Action will probably not be used directly, rather it will be returned
    by calling :meth:`~screenpy_selenium.actions.Select.the_option_with_value`.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`
    """

    target: Optional[Target]
    value: str

    def from_the(self: SelfSelectByValue, target: Target) -> SelfSelectByValue:
        """Target the dropdown or multi-select field to select the option from."""
        self.target = target
        return self

    from_ = from_the_first_of_the = from_the

    def describe(self: SelfSelectByValue) -> str:
        """Describe the Action in present tense."""
        return f'Select the option with value "{self.value}" from the {self.target}.'

    @beat('{} selects the option with value "{value}" from the {target}.')
    def perform_as(self: SelfSelectByValue, the_actor: Actor) -> None:
        """Direct the Actor to select the option by its value."""
        if self.target is None:
            msg = (
                "Target was not provided for SelectByValue. Provide a Target using the "
                ".from_() or .from_the() methods."
            )
            raise UnableToAct(msg)

        element = self.target.found_by(the_actor)
        select = SeleniumSelect(element)
        try:
            select.select_by_value(self.value)
        except WebDriverException as e:
            msg = (
                "Encountered an issue while attempting to select the option with value "
                f"{self.value} from {self.target}: {e.__class__.__name__}"
            )
            raise DeliveryError(msg) from e

    def __init__(
        self: SelfSelectByValue, value: Union[int, str], target: Optional[Target] = None
    ) -> None:
        self.target = target
        self.value = str(value)
