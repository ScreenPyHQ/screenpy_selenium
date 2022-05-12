"""
Matches a present WebElement.
"""

from screenpy.resolutions.base_resolution import BaseResolution

from .custom_matchers import is_present_element
from .custom_matchers.is_present_element import IsPresentElement


class IsPresent(BaseResolution):
    """Match on a present element.

    Examples::

        the_actor.should(See.the(Element(HIDDEN_BUTTON), IsPresent()))
        the_actor.should(See.the(Element(DISABLED_BUTTON), Exists()))
        the_actor.should(See.the(Element(BUTTON), DoesNot(Exist())))
    """

    matcher: IsPresentElement
    line = "present"
    matcher_function = is_present_element

    def __init__(self) -> None:  # pylint: disable=useless-super-delegation
        super().__init__()
