"""Investigate the text of an alert."""

from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy.pacing import beat

from ..abilities import BrowseTheWeb

if TYPE_CHECKING:
    from screenpy.actor import Actor


class TextOfTheAlert:
    """Ask what text appears in the alert.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        the_actor.should(
            See.the(TextOfTheAlert(), ReadsExactly("Danger, Will Robinson!"))
        )
    """

    def describe(self) -> str:
        """Describe the Question."""
        return "The text of the alert."

    @beat("{} reads the text from the alert.")
    def answered_by(self, the_actor: Actor) -> str:
        """Direct the Actor to read off the alert's text."""
        browser = the_actor.uses_ability_to(BrowseTheWeb).browser
        return browser.switch_to.alert.text
