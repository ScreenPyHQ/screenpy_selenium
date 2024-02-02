"""Open a browser on a URL."""

from __future__ import annotations

import os
from typing import Type, TypeVar, Union

from screenpy import Actor
from screenpy.pacing import beat

from ..abilities import BrowseTheWeb

SelfOpen = TypeVar("SelfOpen", bound="Open")


class Open:
    """Go to a specific URL!

    This Action supports using the BASE_URL environment variable to
    set a base URL. If you set BASE_URL, the url passed in to this
    Action will be appended to the end of it. For example, if you
    have ``BASE_URL=http://localhost``, then ``Open("/home")`` will send
    your browser to "http://localhost/home".

    If you pass in an object, make sure the object has a ``url`` property
    that can be referenced by this Action.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        the_actor.attempts_to(Open.their_browser_on(HOMEPAGE_URL))

        # using environment variable BASE_URL
        the_actor.attempts_to(Open.their_browser_on("/login"))

        # using a page object with HomepageObject.url
        the_actor.attempts_to(Open.browser_on(HomepageObject))
    """

    @classmethod
    def their_browser_on(cls: Type[SelfOpen], location: Union[str, object]) -> SelfOpen:
        """
        Provide a URL to visit.

        Aliases:
            * :meth:`~screenpy_selenium.actions.Open.browser_on`
        """
        return cls(location=location)

    @classmethod
    def browser_on(cls: Type[SelfOpen], location: Union[str, object]) -> SelfOpen:
        """Alias for :meth:`~screenpy_selenium.actions.Open.their_browser_on`."""
        return cls.their_browser_on(location=location)

    def describe(self: SelfOpen) -> str:
        """Describe the Action in present tense."""
        return f"Visit {self.url}."

    @beat("{} visits {url}")
    def perform_as(self: SelfOpen, the_actor: Actor) -> None:
        """Direct the Actor to visit the specified URL."""
        browser = the_actor.ability_to(BrowseTheWeb).browser
        browser.get(self.url)

    def __init__(self: SelfOpen, location: Union[str, object]) -> None:
        url = getattr(location, "url", location)
        url = f'{os.getenv("BASE_URL", "")}{url}'
        self.url = url
