"""
Matches against an invisible WebElement.
"""

from typing import TYPE_CHECKING

from screenpy.resolutions.base_resolution import BaseResolution

from .custom_matchers import is_invisible_element

if TYPE_CHECKING:
    from .custom_matchers.is_invisible_element import IsInvisibleElement


class IsInvisible(BaseResolution):
    """Match on an invisible element.

    Examples::

        the_actor.should(See.the(Element(WELCOME_BANNER), IsInvisible()))
    """

    matcher: "IsInvisibleElement"
    line = "invisible"
    matcher_function = is_invisible_element
