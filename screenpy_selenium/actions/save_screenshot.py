"""
Save a screenshot.
"""

import os
from typing import Any, Optional, Type, TypeVar

from screenpy import Actor
from screenpy.actions import AttachTheFile
from screenpy.pacing import beat

from ..abilities import BrowseTheWeb

SelfSaveScreenshot = TypeVar("SelfSaveScreenshot", bound="SaveScreenshot")


class SaveScreenshot:
    """Save a screenshot from the actor's browser.

    Use the :meth:`~screenpy_selenium.actions.SaveScreenshot.and_attach_it`
    method to indicate that this screenshot should be attached to all reports
    through the Narrator's adapters. This method also accepts any keyword
    arguments those adapters might require.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        the_actor.attempts_to(SaveScreenshot("screenshot.png"))

        the_actor.attempts_to(SaveScreenshot.as_(filepath))

        # attach file to the Narrator's reports (behavior depends on adapter).
        the_actor.attempts_to(SaveScreenshot.as_(filepath).and_attach_it())

        # using screenpy_adapter_allure plugin!
        from allure_commons.types import AttachmentType
        the_actor.attempts_to(
            SaveScreenshot.as_(filepath).and_attach_it_with(
                attachment_type=AttachmentTypes.PNG,
            ),
        )
    """

    attach_kwargs: Optional[dict]
    path: str
    filename: str

    def describe(self: SelfSaveScreenshot) -> str:
        """Describe the Action in present tense."""
        return f"Save screenshot as {self.filename}"

    @classmethod
    def as_(cls: Type[SelfSaveScreenshot], path: str) -> SelfSaveScreenshot:
        """Supply the name and/or filepath for the screenshot.

        If only a name is supplied, the screenshot will appear in the current
        working directory.
        """
        return cls(path=path)

    def and_attach_it(self: SelfSaveScreenshot, **kwargs: Any) -> SelfSaveScreenshot:
        """Indicate the screenshot should be attached to any reports.

        This method accepts any additional keywords needed by any adapters
        attached for :external+screenpy:ref:`Narration`.
        """
        self.attach_kwargs = kwargs
        return self

    and_attach_it_with = and_attach_it

    @beat("{} saves a screenshot as {filename}")
    def perform_as(self: SelfSaveScreenshot, the_actor: Actor) -> None:
        """Direct the actor to save a screenshot."""
        browser = the_actor.ability_to(BrowseTheWeb).browser
        screenshot = browser.get_screenshot_as_png()

        with open(self.path, "wb+") as screenshot_file:
            screenshot_file.write(screenshot)

        if self.attach_kwargs is not None:
            the_actor.attempts_to(AttachTheFile(self.path, **self.attach_kwargs))

    def __init__(self: SelfSaveScreenshot, path: str) -> None:
        self.path = path
        self.filename = path.split(os.path.sep)[-1]
        self.attach_kwargs = None
