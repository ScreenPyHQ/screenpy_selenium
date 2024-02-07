"""
A beefed up locator!

Provides an object to store a locator with a human-readable string. The
human-readable string will be used in logging and reporting; the locator
will be used by Actors to find elements.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterator

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from typing_extensions import Self

from .abilities.browse_the_web import BrowseTheWeb
from .exceptions import TargetingError

if TYPE_CHECKING:
    from screenpy.actor import Actor
    from selenium.webdriver.remote.webdriver import WebElement


class Target:
    """Describe an element with a human-readable string and a locator.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        Target.the("header search bar").located_by("div.searchbar")

        Target.the("welcome message").located_by('//h2[@name = "welcome"]')

        Target().located_by((By.ID, "username-field"))
    """

    _description: str | None = None
    locator: tuple[str, str] | None = None

    @property
    def target_name(self) -> str | None:
        """Return the description when set or the 2nd half of the locator."""
        if self._description is not None:
            return self._description
        return self.locator[1] if self.locator else None

    @target_name.setter
    def target_name(self, value: str) -> None:
        self._description = value

    @target_name.deleter
    def target_name(self) -> None:
        del self._description

    @classmethod
    def the(cls, desc: str) -> Self:
        """Name this Target.

        Beginning with a lower-case letter makes the logs look the nicest.
        """
        return cls(desc=desc)

    def located_by(self, locator: tuple[str, str] | str) -> Self:
        """Set the locator for this Target.

        Possible values for locator:
            * A tuple of a By classifier and a string (e.g. ``(By.ID, "welcome")``)
            * An XPATH string (e.g. ``"//div/h3"``)
            * A CSS selector string (e.g. ``"div.confetti"``)

        Aliases:
            * :meth:`~screenpy_selenium.Target.located`
        """
        if not isinstance(locator, (tuple, str)):
            msg = "invalid locator type"
            raise TypeError(msg)

        if isinstance(locator, tuple):
            if len(locator) != 2:  # noqa: PLR2004
                msg = "locator tuple length should be 2"
                raise ValueError(msg)
            self.locator = locator
        elif locator[0] in ("(", "/"):
            self.locator = (By.XPATH, locator)
        else:
            self.locator = (By.CSS_SELECTOR, locator)

        return self

    def located(self, locator: tuple[str, str] | str) -> Self:
        """Alias for :meth:~screenpy_selenium.Target.located_by."""
        return self.located_by(locator)

    def get_locator(self) -> tuple[str, str]:
        """Return the stored locator.

        Raises:
            TargetingError: if no locator was set.
        """
        if self.locator is None:
            msg = (
                f"Locator was not supplied to the {self} target. Make sure to use "
                "either .located() or .located_by() to supply a locator."
            )
            raise TargetingError(msg)
        return self.locator

    def found_by(self, the_actor: Actor) -> WebElement:
        """Retrieve the |WebElement| as viewed by the Actor."""
        browser = the_actor.ability_to(BrowseTheWeb).browser
        try:
            return browser.find_element(*self)
        except WebDriverException as e:
            msg = f"{e} raised while trying to find {self}."
            raise TargetingError(msg) from e

    def all_found_by(self, the_actor: Actor) -> list[WebElement]:
        """Retrieve a list of |WebElement| objects as viewed by the Actor."""
        browser = the_actor.ability_to(BrowseTheWeb).browser
        try:
            return browser.find_elements(*self)
        except WebDriverException as e:
            msg = f"{e} raised while trying to find {self}."
            raise TargetingError(msg) from e

    def __repr__(self) -> str:
        """A Target is represented by its name."""
        return f"{self.target_name}"

    __str__ = __repr__

    def __iter__(self) -> Iterator[str]:
        """Allow Targets to be treated as ``(By, str)`` tuples."""
        return self.get_locator().__iter__()

    def __getitem__(self, index: int) -> str:
        """Allow Targets to be treated as ``(By, str)`` tuples."""
        return self.get_locator()[index]

    def __init__(
        self, desc: str | None = None, locator: tuple[str, str] | None = None
    ) -> None:
        self.target_name = desc
        self.locator = locator
