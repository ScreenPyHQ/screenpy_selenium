"""
Matches a present WebElement.
"""

from screenpy.resolutions.base_resolution import BaseResolution

from .custom_matchers import is_present_element


class IsPresent(BaseResolution):
    """Match on a clickable element.

    Examples::

        the_actor.should(See.the(Element(HIDDEN_BUTTON), IsPresent()))
    """

    line = "present"
    matcher_function = is_present_element
