"""
Matches against an invisible WebElement.
"""

from screenpy.resolutions.base_resolution import BaseResolution

from .custom_matchers import is_invisible_element
from .custom_matchers.is_invisible_element import IsInvisibleElement


class IsInvisible(BaseResolution):
    """Match on an invisible element.

    Examples::

        the_actor.should(See.the(Element(WELCOME_BANNER), IsInvisible()))
    """

    matcher: IsInvisibleElement
    line = "invisible"
    matcher_function = is_invisible_element

    def __init__(self) -> None:  # pylint: disable=useless-super-delegation
        super().__init__()
