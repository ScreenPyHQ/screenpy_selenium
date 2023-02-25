import screenpy_selenium


def test_screenpy_selenium_namespace():
    expected = [
        "AcceptAlert",
        "Attribute",
        "BrowseTheWeb",
        "BrowserTitle",
        "BrowserURL",
        "Chain",
        "Clear",
        "Click",
        "Clickable",
        "ContextClick",
        "Cookies",
        "DismissAlert",
        "Displayed",
        "DoubleClick",
        "Element",
        "Enabled",
        "Enter",
        "Enter2FAToken",
        "Exist",
        "Exists",
        "GoBack",
        "GoForward",
        "HoldDown",
        "Hover",
        "Invisible",
        "IsClickable",
        "IsDisplayed",
        "IsEnabled",
        "IsInvisible",
        "IsNotDisplayed",
        "IsPresent",
        "IsVisible",
        "List",
        "MoveMouse",
        "NotDisplayed",
        "Number",
        "Open",
        "Pause",
        "Present",
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
        "Selected",
        "SwitchTo",
        "SwitchToTab",
        "SwitchToWindow",
        "TakeScreenshot",
        "Target",
        "Text",
        "TextOfTheAlert",
        "TheAttribute",
        "TheBrowserTitle",
        "TheBrowserURL",
        "TheCookies",
        "TheElement",
        "TheList",
        "TheNumber",
        "TheSelected",
        "TheText",
        "TheTextOfTheAlert",
        "Visible",
        "Visit",
        "Wait",
        "Actor",
        "DoesNot",
        "Eventually",
    ]

    assert all(item in screenpy_selenium.__all__ for item in expected)
    return


def test_abilities_namespace():
    expected = [
        "BrowseTheWeb",
    ]
    assert sorted(screenpy_selenium.abilities.__all__) == sorted(expected)


def test_actions_namespace():
    expected = [
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
        "Eventually",
        "See",
        "SeeAnyOf",
        "SeeAllOf",
    ]
    assert all(item in screenpy_selenium.actions.__all__ for item in expected)


def test_questions_namespace():
    expected = [
        "Attribute",
        "BrowserTitle",
        "BrowserURL",
        "Cookies",
        "Element",
        "List",
        "Number",
        "Selected",
        "Text",
        "TextOfTheAlert",
        "TheAttribute",
        "TheBrowserTitle",
        "TheBrowserURL",
        "TheCookies",
        "TheElement",
        "TheList",
        "TheNumber",
        "TheSelected",
        "TheText",
        "TheTextOfTheAlert",
    ]
    assert all(item in screenpy_selenium.questions.__all__ for item in expected)


def test_resolutions_namespace():
    expected = [
        "Clickable",
        "Displayed",
        "Enabled",
        "Exist",
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
        "Equal",
        "ContainsTheText",
        "DoesNot",
    ]
    assert all(item in screenpy_selenium.resolutions.__all__ for item in expected)