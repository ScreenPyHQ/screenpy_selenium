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
AcceptsAlert = AcceptAlert
Chains = Chain
Clears = Clear
Clicks = Click
ContextClick = ContextClicks = RightClick
DismissesAlert = DismissAlert
DismissTheAlert = DismissesTheAlert = DismissAlert
DoubleClicks = DoubleClick
Enters = Enter
Enters2FAToken = Enter2FAToken
GoesBack = GoBack
GoesForward = GoForward
HoldsDown = HoldDown
Hover = Hovers = MoveMouse
MovesMouse = MoveMouse
Press = Presses = Enter
Pauses = Pause
Refresh = Refreshes = RefreshPage
Reload = Reloads = RefreshPage
ReloadPage = ReloadsPage = RefreshPage
RefreshesPage = RefreshPage
Releases = Release
RespondToPrompt = RespondsToPrompt = RespondToThePrompt
RespondsToThePrompt = RespondToThePrompt
RightClicks = RightClick
SavesConsoleLog = SaveConsoleLog
SavesScreenshot = SaveScreenshot
Selects = Select
SelectsByIndex = SelectByIndex
SelectsByText = SelectByText
SelectsByValue = SelectByValue
SwitchesTo = SwitchTo
SwitchesToTab = SwitchToTab
SwitchToWindow = SwitchesToWindow = SwitchToTab
TakeScreenshot = TakesScreenshot = SaveScreenshot
Visit = Visits = Open
Opens = Open
Waits = Wait

__all__ = [
    "AcceptAlert",
    "AcceptsAlert",
    "Chain",
    "Chains",
    "Clear",
    "Clears",
    "Click",
    "Clicks",
    "ContextClick",
    "ContextClicks",
    "DismissAlert",
    "DismissesAlert",
    "DoubleClick",
    "DoubleClicks",
    "Enter",
    "Enter2FAToken",
    "Enters",
    "Enters2FAToken",
    "GoBack",
    "GoesBack",
    "GoesForward",
    "GoForward",
    "HoldDown",
    "HoldsDown",
    "Hover",
    "Hovers",
    "MoveMouse",
    "MovesMouse",
    "Open",
    "Opens",
    "Pause",
    "Pauses",
    "Press",
    "Presses",
    "Refresh",
    "Refreshes",
    "RefreshesPage",
    "RefreshPage",
    "Release",
    "Releases",
    "Reload",
    "ReloadPage",
    "Reloads",
    "ReloadsPage",
    "RespondsToPrompt",
    "RespondsToThePrompt",
    "RespondToPrompt",
    "RespondToThePrompt",
    "RightClick",
    "RightClicks",
    "SaveConsoleLog",
    "SavesConsoleLog",
    "SaveScreenshot",
    "SavesScreenshot",
    "Select",
    "SelectByIndex",
    "SelectByText",
    "SelectByValue",
    "Selects",
    "SelectsByIndex",
    "SelectsByText",
    "SelectsByValue",
    "SwitchesTo",
    "SwitchesToTab",
    "SwitchesToWindow",
    "SwitchTo",
    "SwitchToTab",
    "SwitchToWindow",
    "TakeScreenshot",
    "TakesScreenshot",
    "Visit",
    "Visits",
    "Wait",
    "Waits",
]
