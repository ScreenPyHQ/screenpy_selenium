"""Press the browser forward button."""

from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy.pacing import beat

from ..abilities import BrowseTheWeb

if TYPE_CHECKING:
    from screenpy.actor import Actor


class GoForward:
    """Press the browser forward button.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        the_actor.attempts_to(GoForward())
    """

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return "Go forward."

    @beat("{} goes forward.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to press their browser's forward button."""
        browser = the_actor.ability_to(BrowseTheWeb).browser
        browser.forward()
