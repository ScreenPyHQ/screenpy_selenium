"""
Matches against a visible WebElement.
"""

from screenpy.resolutions.base_resolution import BaseResolution

from .custom_matchers import is_invisible_element


class IsInvisible(BaseResolution):
    """Match on a visible element.

    Examples::

        the_actor.should(See.the(Element(WELCOME_BANNER), IsInvisible()))
    """

    line = "invisible"
    matcher_function = is_invisible_element
