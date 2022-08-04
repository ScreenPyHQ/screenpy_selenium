from typing_extensions import Protocol
from screenpy.protocols import Answerable, Forgettable, Performable, ErrorKeeper
from screenpy_selenium.protocols import Chainable

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


