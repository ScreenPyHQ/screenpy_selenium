"""
Dismiss a javascript alert.
"""

from screenpy.actor import Actor
from screenpy.pacing import aside, beat

from ..abilities import BrowseTheWeb


class DismissAlert:
    """Dismiss an alert.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        the_actor.attempts_to(DismissAlert())
    """

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return "Dismiss the alert."

    @beat("{} dismisses the alert.")
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to dismiss the alert."""
        browser = the_actor.uses_ability_to(BrowseTheWeb).browser
        alert = browser.switch_to.alert
        aside(f'... the alert says "{alert.text}"')
        alert.dismiss()
