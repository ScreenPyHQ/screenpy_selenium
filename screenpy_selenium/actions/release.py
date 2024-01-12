"""Release the left mouse button or a held modifier key."""

from __future__ import annotations

import platform
from typing import TYPE_CHECKING, TypeVar

from screenpy.exceptions import UnableToAct
from screenpy.pacing import beat
from selenium.webdriver.common.keys import Keys

from ..common import pos_args_deprecated
from ..speech_tools import KEY_NAMES

if TYPE_CHECKING:
    from screenpy import Actor
    from selenium.webdriver.common.action_chains import ActionChains

SelfRelease = TypeVar("SelfRelease", bound="Release")


class Release:
    """Release the specified key or left mouse button.

    This Action can only be used with :class:`~screenpy_selenium.actions.Chain`,
    and it expects that a corresponding :class:`~screenpy_selenium.actions.HoldDown`
    Action was called earlier in the Chain.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        the_actor.attempts_to(Release.left_mouse_button())

        the_actor.attempts_to(Release(Keys.SHIFT))

        the_actor.attempts_to(Release.command_or_control_key())
    """

    key: str | None
    lmb: bool
    description: str
    the_kraken: str

    @classmethod
    def command_or_control_key(cls: type[SelfRelease]) -> SelfRelease:
        """
        A convenience method for supporting multiple operating systems.

        Figures out what operating system the Actor is using and tells the Actor which
        execution key to release.
        """
        if platform.system() == "Darwin":
            return cls(key=Keys.COMMAND)
        return cls(key=Keys.CONTROL)

    @classmethod
    def left_mouse_button(cls: type[SelfRelease]) -> SelfRelease:
        """Release the left mouse button."""
        return cls(lmb=True)

    def describe(self: SelfRelease) -> str:
        """Describe the Action in present tense."""
        # darn, it doesn't work quite as well here. :P
        return f"Release {self.the_kraken}."

    @beat("Release {the_kraken}!")
    def add_to_chain(self: SelfRelease, _: Actor, the_chain: ActionChains) -> None:
        """Add the Release Action to a Chain of Actions."""
        if self.lmb:
            the_chain.release()
        elif self.key is not None:
            the_chain.key_up(self.key)
        else:
            msg = "Release must be told what to release."
            raise UnableToAct(msg)

    @pos_args_deprecated("lmb")
    def __init__(
        self: SelfRelease,
        key: str | None = None,
        lmb: bool = False,  # noqa: FBT001, FBT002
    ) -> None:
        self.key = key
        self.lmb = lmb
        self.description = "LEFT MOUSE BUTTON" if lmb else KEY_NAMES[key]
        self.the_kraken = self.description  # i can't help myself
