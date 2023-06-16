"""
Actions an Actor can perform using their ability to BrowseTheWeb.
"""

from .accept_alert import AcceptAlert  # noqa
from .chain import Chain  # noqa
from .clear import Clear  # noqa
from .click import Click  # noqa
from .dismiss_alert import DismissAlert  # noqa
from .double_click import DoubleClick  # noqa
from .enter import Enter
from .enter_2fa_token import Enter2FAToken  # noqa
from .go_back import GoBack  # noqa
from .go_forward import GoForward  # noqa
from .hold_down import HoldDown  # noqa
from .move_mouse import MoveMouse
from .open import Open
from .pause import Pause  # noqa
from .refresh_page import RefreshPage
from .release import Release  # noqa
from .respond_to_the_prompt import RespondToThePrompt
from .right_click import RightClick
from .save_console_log import SaveConsoleLog  # noqa
from .save_screenshot import SaveScreenshot
from .select import Select, SelectByIndex, SelectByText, SelectByValue  # noqa
from .switch_to import SwitchTo  # noqa
from .switch_to_tab import SwitchToTab
from .wait import Wait  # noqa

# Natural-language-enabling syntactic sugar
ContextClick = RightClick
Hover = MoveMouse
Press = Enter
Pauses = Pause
Refresh = Reload = ReloadPage = RefreshPage
RespondToPrompt = RespondToThePrompt
SwitchToWindow = SwitchToTab
TakeScreenshot = SaveScreenshot
Visit = Open

__all__ = [
    "AcceptAlert",
    "Chain",
    "Clear",
    "Click",
    "ContextClick",
    "DismissAlert",
    "DoubleClick",
    "Enter",
    "Enter2FAToken",
    "GoBack",
    "GoForward",
    "HoldDown",
    "Hover",
    "MoveMouse",
    "Open",
    "Pause",
    "Pauses",
    "Press",
    "Refresh",
    "RefreshPage",
    "Release",
    "Reload",
    "ReloadPage",
    "RespondToPrompt",
    "RespondToThePrompt",
    "RightClick",
    "SaveConsoleLog",
    "SaveScreenshot",
    "Select",
    "SelectByIndex",
    "SelectByText",
    "SelectByValue",
    "SwitchTo",
    "SwitchToTab",
    "SwitchToWindow",
    "TakeScreenshot",
    "Visit",
    "Wait",
]
