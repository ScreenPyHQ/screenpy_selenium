"""
Additional protocols for ScreenPy+Selenium.
"""

from screenpy import Actor
from selenium.webdriver.common.action_chains import ActionChains
from typing_extensions import Protocol


class Chainable(Protocol):
    """Actions that can be added to a chain are Chainable."""

    def add_to_chain(self, the_actor: Actor, the_chain: ActionChains) -> None:
        """
        Add this chainable Action to a chain of Actions.

        Args:
            the_actor: the Actor who will be performing the Action chain.
            the_chain: the |ActionChains| instance that is being built.
        """
        ...
