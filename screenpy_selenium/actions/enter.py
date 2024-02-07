"""Enter text into an input field, or press keys."""

from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING

from screenpy.exceptions import DeliveryError, UnableToAct
from screenpy.pacing import aside, beat
from selenium.common.exceptions import WebDriverException
from typing_extensions import Self

from ..common import pos_args_deprecated
from ..speech_tools import KEY_NAMES

if TYPE_CHECKING:
    from screenpy import Actor
    from selenium.webdriver.common.action_chains import ActionChains

    from ..target import Target


class Enter:
    """Enter text into an input field, or press specific keys.

    Abilities Required:
        :class:`~screenpy_selenium.abilities.BrowseTheWeb`

    Examples::

        the_actor.attempts_to(
            Enter.the_text("Hello world!").into_the(COMMENT_FIELD)
        )
    """

    target: Target | None
    following_keys: list[str]
    text: str
    text_to_log: str

    @classmethod
    def the_text(cls, text: str) -> Self:
        """Provide the text to enter into the field.

        Aliases:
            * :meth:`~screenpy_selenium.actions.Enter.the_keys`
        """
        return cls(text=text)

    @classmethod
    def the_keys(cls, text: str) -> Self:
        """Alias for :meth:`~screenpy_selenium.actions.Enter.the_text`."""
        return cls.the_text(text=text)

    @classmethod
    def the_secret(cls, text: str) -> Self:
        """
        Provide the text to enter into the field, but mask it in logging.

        The text will appear as "[CENSORED]".

        Aliases:
            * :meth:`~screenpy_selenium.actions.Enter.the_password`
        """
        return cls(text=text, mask=True)

    @classmethod
    def the_password(cls, text: str) -> Self:
        """Alias for :meth:`~screenpy_selenium.actions.Enter.the_secret`."""
        return cls.the_secret(text=text)

    def into_the(self, target: Target) -> Self:
        """Target the element to enter text into.

        Aliases:
            * :meth:`~screenpy_selenium.actions.Enter.into`
            * :meth:`~screenpy_selenium.actions.Enter.on`
            * :meth:`~screenpy_selenium.actions.Enter.into_the_first_of_the`
        """
        self.target = target
        return self

    def into(self, target: Target) -> Self:
        """Alias for :meth:`~screenpy_selenium.actions.Enter.into_the`."""
        return self.into_the(target)

    def on(self, target: Target) -> Self:
        """Alias for :meth:`~screenpy_selenium.actions.Enter.into_the`."""
        return self.into_the(target)

    def into_the_first_of_the(self, target: Target) -> Self:
        """Alias for :meth:`~screenpy_selenium.actions.Enter.into_the`."""
        return self.into_the(target)

    def then_hit(self, *keys: str) -> Self:
        """Supply additional keys to hit after entering the text.

        Args:
            keys: the keys to hit afterwards. These are probably the
                constants from Selenium's |Keys|.

        Aliases:
            * :meth:`~screenpy_selenium.actions.Enter.then_press`
        """
        self.following_keys.extend(keys)
        return self

    def then_press(self, *keys: str) -> Self:
        """Alias for :meth:`~screenpy_selenium.actions.Enter.then_hit`."""
        return self.then_hit(*keys)

    def describe(self) -> str:
        """Describe the Action in present tense."""
        return f'Enter "{self.text_to_log}" into the {self.target}.'

    @beat('{} enters "{text_to_log}" into the {target}.')
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to enter the text into the element."""
        if self.target is None:
            msg = (
                "Target was not supplied for Enter. Provide a Target by using either "
                "the .into(), .into_the(), or .on() method."
            )
            raise UnableToAct(msg)

        element = self.target.found_by(the_actor)

        try:
            element.send_keys(self.text)
            for key in self.following_keys:
                aside(f"then hits the {KEY_NAMES[key]} key")
                element.send_keys(key)
        except WebDriverException as e:
            msg = (
                "Encountered an issue while attempting to enter text into "
                f"{self.target}: {e.__class__.__name__}"
            )
            raise DeliveryError(msg) from e

    @beat('  Enter "{text_to_log}" into the {target}!')
    def add_to_chain(self, the_actor: Actor, the_chain: ActionChains) -> None:
        """Add the Enter Action to a Chain of Actions."""
        if self.target is None:
            send_keys = the_chain.send_keys
        else:
            element = self.target.found_by(the_actor)
            send_keys = partial(the_chain.send_keys_to_element, element)

        send_keys(self.text)
        for key in self.following_keys:
            send_keys(key)

    @pos_args_deprecated("mask")
    def __init__(
        self, text: str, mask: bool = False  # noqa: FBT001, FBT002
    ) -> None:
        self.text = text
        self.target = None
        self.following_keys = []

        if mask:
            self.text_to_log = "[CENSORED]"
        else:
            altered_text = text
            for value, keyname in KEY_NAMES.items():
                altered_text = altered_text.replace(value, keyname)
            self.text_to_log = altered_text
