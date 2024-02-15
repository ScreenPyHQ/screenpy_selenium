"""Module to hold shared objects."""

from __future__ import annotations

import warnings
from functools import wraps
from typing import TYPE_CHECKING, Callable, TypeVar

if TYPE_CHECKING:
    from typing_extensions import ParamSpec

    P = ParamSpec("P")
    T = TypeVar("T")
    Function = Callable[P, T]


def pos_args_deprecated(*keywords: str) -> Function:
    """Warn users which positional arguments should be called via keyword."""

    def deprecated(func: Function) -> Function:
        argnames = func.__code__.co_varnames[: func.__code__.co_argcount]
        i = min([argnames.index(kw) for kw in keywords])
        kw_argnames = argnames[i:]

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Function:
            # call the function first, to make sure the signature matches
            ret_value = func(*args, **kwargs)

            args_that_should_be_kw = args[i:]
            if args_that_should_be_kw:
                posargnames = ", ".join(kw_argnames)

                msg = (
                    f"Warning: positional arguments `{posargnames}` for "
                    f"`{func.__qualname__}` are deprecated "
                    f"and will be removed in version 5. "
                    f"Please use keyword arguments instead."
                )
                warnings.warn(msg, DeprecationWarning, stacklevel=2)

            return ret_value

        return wrapper

    return deprecated
