"""
Save the browser console log.
"""

import os
from typing import Any, Optional, Type, TypeVar

from screenpy import Actor
from screenpy.actions import AttachTheFile
from screenpy.pacing import beat

from ..abilities import BrowseTheWeb

SelfSaveConsoleLog = TypeVar("SelfSaveConsoleLog", bound="SaveConsoleLog")


class SaveConsoleLog:
    """Save the Actor's browser's console log.

    Note that you may need to set additional driver properties when creating
    the Actor's browser to enable the console log (e.g. setting
    ``capabilities["goog:loggingPrefs"] = {"browser": "ALL"}``.)

    Use the :meth:`~screenpy_selenium.actions.SaveConsoleLog.and_attach_it`
    method to indicate that this text file should be attached to all reports
    through the Narrator's adapters. This method also accepts any keyword
    arguments those adapters might require.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        the_actor.attempts_to(SaveConsoleLog("console_log.txt"))

        the_actor.attempts_to(SaveConsoleLog.as_(filepath))

        # attach file to the Narrator's reports (behavior depends on adapter).
        the_actor.attempts_to(SaveConsoleLog.as_(filepath).and_attach_it())

        # using screenpy_adapter_allure plugin!
        from allure_commons.types import AttachmentType
        the_actor.attempts_to(
            SaveConsoleLog.as_(filepath).and_attach_it_with(
                attachment_type=AttachmentTypes.TEXT,
            ),
        )
    """

    attach_kwargs: Optional[dict]
    path: str
    filename: str

    def describe(self: SelfSaveConsoleLog) -> str:
        """Describe the Action in present tense."""
        return f"Save browser console log as {self.filename}"

    @classmethod
    def as_(cls: Type[SelfSaveConsoleLog], path: str) -> SelfSaveConsoleLog:
        """Supply the name and/or filepath for the saved text file.

        If only a name is supplied, the text file will appear in the current
        working directory.
        """
        return cls(path=path)

    def and_attach_it(self: SelfSaveConsoleLog, **kwargs: Any) -> SelfSaveConsoleLog:
        """Indicate the console log file should be attached to any reports.

        This method accepts any additional keywords needed by any adapters
        attached for :external+screenpy:ref:`Narration`.
        """
        self.attach_kwargs = kwargs
        return self

    and_attach_it_with = and_attach_it

    @beat("{} saves their browser's console log as {filename}")
    def perform_as(self: SelfSaveConsoleLog, the_actor: Actor) -> None:
        """Direct the actor to save their browser's console log."""
        browser = the_actor.ability_to(BrowseTheWeb).browser
        js_log = "\n".join([str(entry) for entry in browser.get_log("browser")])

        with open(self.path, "w+", encoding="utf-8") as js_log_file:
            js_log_file.write(js_log)

        if self.attach_kwargs is not None:
            the_actor.attempts_to(AttachTheFile(self.path, **self.attach_kwargs))

    def __init__(self: SelfSaveConsoleLog, path: str) -> None:
        self.path = path
        self.filename = path.split(os.path.sep)[-1]
        self.attach_kwargs = None
