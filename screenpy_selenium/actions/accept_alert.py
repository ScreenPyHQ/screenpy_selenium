"""Accept a javascript alert."""

from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy.pacing import aside, beat

from ..abilities import BrowseTheWeb

if TYPE_CHECKING:
    from screenpy.actor import Actor


class AcceptAlert:
    """Accept an alert!

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        the_actor.attempts_to(AcceptAlert())
    """

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return "Accept the alert."

    @beat("{} accepts the alert.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to accept the alert."""
        browser = the_actor.ability_to(BrowseTheWeb).browser
        alert = browser.switch_to.alert
        aside(f'... the alert says "{alert.text}"')
        alert.accept()
