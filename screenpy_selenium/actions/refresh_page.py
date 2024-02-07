"""Refresh the browser page."""

from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy.pacing import beat

from ..abilities import BrowseTheWeb

if TYPE_CHECKING:
    from screenpy import Actor


class RefreshPage:
    """Refresh the browser page!

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        the_actor.attempts_to(RefreshPage())
    """

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return "Refresh the page."

    @beat("{} refreshes the page.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to refresh the page."""
        browser = the_actor.ability_to(BrowseTheWeb).browser
        browser.refresh()
