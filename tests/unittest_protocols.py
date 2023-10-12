from typing import Protocol, runtime_checkable

from screenpy import Answerable, Describable, Forgettable, Performable

from screenpy_selenium import Chainable


@runtime_checkable
class Question(Answerable, Describable, Protocol):
    ...


@runtime_checkable
class Action(Performable, Describable, Protocol):
    ...


@runtime_checkable
class ChainableAction(Chainable, Performable, Describable, Protocol):
    ...


@runtime_checkable
class Ability(Forgettable, Protocol):
    ...
