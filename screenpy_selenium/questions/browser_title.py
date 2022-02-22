"""
Investigate the title of an Actor's active browser window.
"""

from screenpy import Actor
from screenpy.pacing import beat

from ..abilities import BrowseTheWeb


class BrowserTitle:
    """Ask what the title of the browser's active window is.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        the_actor.should(See.the(BrowserTitle(), ReadsExactly("Welcome!")))
    """

    def describe(self) -> str:
        """Describe the Question."""
        return "The current page's title."

    @beat("{} reads the title of the page from their browser.")
    def answered_by(self, the_actor: Actor) -> str:
        """Direct the Actor to investigate the browser's title."""
        browser = the_actor.ability_to(BrowseTheWeb).browser
        return browser.title
