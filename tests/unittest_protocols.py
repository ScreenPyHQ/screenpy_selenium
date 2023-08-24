from typing import Protocol

from screenpy import Answerable, ErrorKeeper, Forgettable, Performable

from screenpy_selenium import Chainable


class Describable(Protocol):
    def describe(self) -> str:
        ...


class Question(Answerable, Describable, Protocol):
    ...


class ErrorQuestion(Answerable, Describable, ErrorKeeper, Protocol):
    ...


class Action(Performable, Describable, Protocol):
    ...


class ChainableAction(Chainable, Performable, Describable, Protocol):
    ...


class Ability(Forgettable, Protocol):
    ...
