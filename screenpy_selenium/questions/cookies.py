"""
Investigate the cookies on the Actor's web or API session.
"""

from screenpy import Actor
from screenpy.pacing import beat

from ..abilities import BrowseTheWeb


class Cookies:
    """Ask about the cookies on the Actor's web browsing session.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        the_actor.should(
            See.the(CookiesOnTheWebSession(), ContainTheEntry(type="oatmeal raisin"))
        )
    """

    def describe(self) -> str:
        """Describe the Question."""
        return "The browser's cookies."

    @beat("{} inspects their web browser's cookies...")
    def answered_by(self, the_actor: Actor) -> dict:
        """Direct the Actor to investigate their web browser's cookies."""
        cookies = the_actor.uses_ability_to(BrowseTheWeb).browser.get_cookies()
        return {c["name"]: c["value"] for c in cookies}
