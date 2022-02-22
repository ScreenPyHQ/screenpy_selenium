"""
Actions an Actor can perform using their ability to BrowseTheWeb.
"""

from .accept_alert import AcceptAlert
from .chain import Chain
from .clear import Clear
from .click import Click
from .dismiss_alert import DismissAlert
from .double_click import DoubleClick
from .enter import Enter
from .enter_2fa_token import Enter2FAToken
from .go_back import GoBack
from .go_forward import GoForward
from .hold_down import HoldDown
from .move_mouse import MoveMouse
from .open import Open
from .pause import Pause
from .refresh_page import RefreshPage
from .release import Release
from .respond_to_the_prompt import RespondToThePrompt
from .right_click import RightClick
from .save_console_log import SaveConsoleLog
from .save_screenshot import SaveScreenshot
from .select import Select, SelectByIndex, SelectByText, SelectByValue
from .switch_to import SwitchTo
from .switch_to_tab import SwitchToTab
from .wait import Wait

# Natural-language-enabling syntactic sugar
ContextClick = RightClick
Hover = MoveMouse
Press = Enter
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
