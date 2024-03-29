"""Click on an element."""

from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy.exceptions import DeliveryError, UnableToAct
from screenpy.pacing import beat
from selenium.common.exceptions import WebDriverException

if TYPE_CHECKING:
    from screenpy.actor import Actor
    from selenium.webdriver.common.action_chains import ActionChains
    from typing_extensions import Self

    from ..target import Target


class Click:
    """Click on an element!

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        the_actor.attempts_to(Click.on_the(PROFILE_LINK))

        the_actor.attempts_to(Click.on(THE_LOGIN_LINK))

        the_actor.attempts_to(Chain(Click(THE_LOGIN_LINK)))
    """

    @classmethod
    def on_the(cls, target: Target) -> Self:
        """
        Target the element to click on.

        Aliases:
            * :meth:`~screenpy_selenium.actions.Click.on`
            * :meth:`~screenpy_selenium.actions.Click.on_the_first_of_the`
        """
        return cls(target=target)

    @classmethod
    def on(cls, target: Target) -> Self:
        """Alias for :meth:`~screenpy_selenium.actions.Click.on_the`."""
        return cls.on_the(target=target)

    @classmethod
    def on_the_first_of_the(cls, target: Target) -> Self:
        """Alias for :meth:`~screenpy_selenium.actions.Click.on_the`."""
        return cls.on_the(target=target)

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return f"Click on the {self.target}."

    @beat("{} clicks on the {target}.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to click on the element."""
        if self.target is None:
            msg = (
                "Target was not supplied for Click. "
                "Provide a Target by using the .on() or .on_the() method."
            )
            raise UnableToAct(msg)

        element = self.target.found_by(the_actor)

        try:
            element.click()
        except WebDriverException as e:
            msg = (
                "Encountered an issue while attempting to click "
                f"{self.target}: {e.__class__.__name__}"
            )
            raise DeliveryError(msg) from e

    @beat("Click{description}!")
    def add_to_chain(self, the_actor: Actor, the_chain: ActionChains) -> None:
        """Add the Click Action to a Chain of Actions."""
        if self.target is not None:
            the_element = self.target.found_by(the_actor)
        else:
            the_element = None

        the_chain.click(on_element=the_element)

    def __init__(self, target: Target | None = None) -> None:
        self.target = target
        self.description = f" on the {target}" if target is not None else ""
