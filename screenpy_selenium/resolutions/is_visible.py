"""
Matches against a visible WebElement.
"""

from screenpy.resolutions.base_resolution import BaseResolution

from .custom_matchers import is_visible_element
from .custom_matchers.is_visible_element import IsVisibleElement


class IsVisible(BaseResolution):
    """Match on a visible element.

    Examples::

        the_actor.should(See.the(Element(WELCOME_BANNER), IsVisible()))
    """

    matcher: IsVisibleElement
    line = "visible"
    matcher_function = is_visible_element

    def __init__(self) -> None:  # pylint: disable=useless-super-delegation
        super().__init__()
