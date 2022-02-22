"""
Additional Resolutions to provide expected answers for Selenium tests.
"""

from .is_clickable import IsClickable
from .is_visible import IsVisible

# Natural-language-enabling syntactic sugar
IsEnabled = Enabled = Clickable = IsClickable
IsDisplayed = Displayed = Visible = IsVisible


__all__ = [
    "Clickable",
    "Displayed",
    "Enabled",
    "IsClickable",
    "IsDisplayed",
    "IsEnabled",
    "IsVisible",
    "Visible",
]
