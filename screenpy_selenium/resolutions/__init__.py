"""Additional Resolutions to provide expected answers for Selenium tests."""

from .is_clickable import IsClickable
from .is_disabled import IsDisabled
from .is_enabled import IsEnabled
from .is_invisible import IsInvisible
from .is_present import IsPresent
from .is_visible import IsVisible

# Natural-language-enabling syntactic sugar
Clickable = IsClickable
Disabled = IsDisabled
Enabled = IsEnabled
IsDisplayed = Displayed = Visible = IsVisible
IsNotDisplayed = NotDisplayed = Invisible = IsInvisible
Exist = Exists = Present = IsPresent


__all__ = [
    "Clickable",
    "Disabled",
    "Displayed",
    "Enabled",
    "Exist",
    "Exists",
    "Invisible",
    "IsClickable",
    "IsDisabled",
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
