"""
Provides an object to store a locator with a human-readable string. The
human-readable string will be used in logging and reporting; the locator
will be used by Actors to find elements.
"""

from typing import Iterator, List, Optional, Tuple, Union

from screenpy.actor import Actor
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebElement

from .abilities.browse_the_web import BrowseTheWeb
from .exceptions import TargetingError


class Target:
    """Describe an element with a human-readable string and a locator.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        Target.the("header search bar").located_by("div.searchbar")

        Target.the("welcome message").located_by('//h2[@name = "welcome"]')

        Target().located_by((By.ID, "username-field"))
    """

    _description: Optional[str] = None
    locator: Optional[Tuple[str, str]] = None

    @property
    def target_name(self):
        if self._description is not None:
            return self._description
        return self.locator[1] if self.locator else None

    @target_name.setter
    def target_name(self, value):
        self._description = value

    @target_name.deleter
    def target_name(self):
        del self._description

    @staticmethod
    def the(desc: str) -> "Target":
        """Name this Target.

        Beginning with a lower-case letter makes the logs look the nicest.
        """
        return Target(desc)

    def located_by(self, locator: Union[Tuple[str, str], str]) -> "Target":
        """Set the locator for this Target.

        Possible values for locator:
            * A tuple of a By classifier and a string (e.g. ``(By.ID, "welcome")``)
            * An XPATH string (e.g. ``"//div/h3"``)
            * A CSS selector string (e.g. ``"div.confetti"``)

        Aliases:
            * :meth:`~screenpy_selenium.Target.located`
        """
        if not isinstance(locator, (tuple, str)):
            raise TypeError("invalid locator type")

        if isinstance(locator, tuple):
            if len(locator) != 2:
                raise ValueError("locator tuple length should be 2")
            self.locator = locator
        elif locator[0] in ("(", "/"):
            self.locator = (By.XPATH, locator)
        else:
            self.locator = (By.CSS_SELECTOR, locator)

        return self

    def located(self, locator: Union[Tuple[str, str], str]) -> "Target":
        """Alias for :meth:~screenpy_selenium.Target.located_by"""
        return self.located_by(locator)

    def get_locator(self) -> Tuple[str, str]:
        """Return the stored locator.

        Raises:
            TargetingError: if no locator was set.
        """
        if self.locator is None:
            raise TargetingError(
                f"Locator was not supplied to the {self} target. Make sure to use "
                "either .located() or .located_by() to supply a locator."
            )
        return self.locator

    def found_by(self, the_actor: Actor) -> WebElement:
        """Retrieve the |WebElement| as viewed by the Actor."""
        browser = the_actor.ability_to(BrowseTheWeb).browser
        try:
            return browser.find_element(*self)
        except WebDriverException as e:
            raise TargetingError(f"{e} raised while trying to find {self}.") from e

    def all_found_by(self, the_actor: Actor) -> List[WebElement]:
        """Retrieve a list of |WebElement| objects as viewed by the Actor."""
        browser = the_actor.ability_to(BrowseTheWeb).browser
        try:
            return browser.find_elements(*self)
        except WebDriverException as e:
            raise TargetingError(f"{e} raised while trying to find {self}.") from e

    def __repr__(self) -> str:
        return f"{self.target_name}"

    __str__ = __repr__

    def __iter__(self) -> Iterator[str]:
        return self.get_locator().__iter__()

    def __getitem__(self, index: int) -> str:
        return self.get_locator()[index]

    def __init__(self, desc: str = None, locator: Tuple[str, str] = None) -> None:
        self.target_name = desc
        self.locator = locator
