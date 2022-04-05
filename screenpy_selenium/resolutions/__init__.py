"""
Additional Resolutions to provide expected answers for Selenium tests.
"""

from .is_clickable import IsClickable
from .is_invisible import IsInvisible
from .is_present import IsPresent
from .is_visible import IsVisible

# Natural-language-enabling syntactic sugar
IsEnabled = Enabled = Clickable = IsClickable
IsDisplayed = Displayed = Visible = IsVisible
IsNotDisplayed = NotDisplayed = Invisible = IsInvisible
Exists = Present = IsPresent

__all__ = [
    "Clickable",
    "Displayed",
    "Enabled",
    "Exists",
    "Invisible",
    "IsClickable",
    "IsDisplayed",
    "IsEnabled",
    "IsInvisible",
    "IsNotDisplayed",
    "IsPresent",
    "IsVisible",
    "NotDisplayed",
    "Present",
    "Visible",
]
