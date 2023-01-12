"""
Respond to a prompt.
"""
from typing import Type, TypeVar

from screenpy.actor import Actor
from screenpy.pacing import aside, beat

from ..abilities import BrowseTheWeb

SelfRespondToThePrompt = TypeVar("SelfRespondToThePrompt", bound="RespondToThePrompt")


class RespondToThePrompt:
    """Enter text into and accept a javascript prompt.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        the_actor.attempts_to(
            RespondToThePrompt.with_("Roger, Roger. What's your vector, Victor?")
        )
    """

    @classmethod
    def with_(cls: Type[SelfRespondToThePrompt], text: str) -> SelfRespondToThePrompt:
        """Provide the text to enter into the prompt."""
        return cls(text)

    def describe(self: SelfRespondToThePrompt) -> str:
        """Describe the Action in present tense."""
        return f'Respond to the prompt with "{self.text}".'

    @beat('{} responds to the prompt with "{text}".')
    def perform_as(self: SelfRespondToThePrompt, the_actor: Actor) -> None:
        """Direct the Actor to respond to the prompt using the given text."""
        browser = the_actor.uses_ability_to(BrowseTheWeb).browser
        alert = browser.switch_to.alert
        aside(f"... the alert says {alert.text}")
        alert.send_keys(self.text)
        alert.accept()

    def __init__(self: SelfRespondToThePrompt, text: str) -> None:
        self.text = text
