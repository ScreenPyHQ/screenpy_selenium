"""Investigate the selected option or options from a dropdown or multi-select field."""

from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy.pacing import beat
from selenium.webdriver.support.ui import Select as SeleniumSelect

from ..common import pos_args_deprecated

if TYPE_CHECKING:
    from screenpy import Actor
    from typing_extensions import Self

    from ..target import Target


class Selected:
    """Ask for the text of selected option(s) in a dropdown or multi-select field.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        the_actor.should(
            See.the(Selected.option_from(THE_STATE_DROPDOWN), ReadsExactly("Minnesota"))
        )

        the_actor.should(See.the(Selected.options_from(INDUSTRIES), HasLength(5)))
    """

    target: Target
    multi: bool

    @classmethod
    def option_from_the(cls, target: Target) -> Self:
        """
        Get the option.

        Get the option that is currently selected in a dropdown or the first
        option selected in a multi-select field.

        *Note*: if this method is used for a multi-select field, only the
        first selected option will be returned.

        Aliases:
            * :meth:`~screenpy_selenium.actions.Selected.option_from`
        """
        return cls(target=target)

    @classmethod
    def option_from(cls, target: Target) -> Self:
        """Alias of :meth:`~screenpy_selenium.actions.Selected.option_from_the`."""
        return cls.option_from_the(target=target)

    @classmethod
    def options_from_the(cls, multiselect_target: Target) -> Self:
        """
        Get all the options that are currently selected in a multi-select field.

        *Note*: this method should not be used for single-select dropdowns,
        that will cause a NotImplemented error to be raised from Selenium when
        answering this Question.

        Aliases:
            * :meth:`~screenpy_selenium.actions.Selected.options_from`
        """
        return cls(target=multiselect_target, multi=True)

    @classmethod
    def options_from(cls, multiselect_target: Target) -> Self:
        """Alias of :meth:`~screenpy_selenium.actions.Selected.options_from_the`."""
        return cls.options_from_the(multiselect_target=multiselect_target)

    def describe(self) -> str:
        """Describe the Question."""
        return f"The selected option(s) from the {self.target}."

    @beat("{} checks the selected option(s) from the {target}.")
    def answered_by(self, the_actor: Actor) -> str | list[str]:
        """Direct the Actor to name the selected option(s)."""
        select = SeleniumSelect(self.target.found_by(the_actor))

        if self.multi:
            return [e.text for e in select.all_selected_options]
        return select.first_selected_option.text

    @pos_args_deprecated("multi")
    def __init__(
        self, target: Target, multi: bool = False  # noqa: FBT001, FBT002
    ) -> None:
        self.target = target
        self.multi = multi
