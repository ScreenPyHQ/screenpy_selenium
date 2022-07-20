import time
from unittest import mock

import pytest
from screenpy import settings
from screenpy.exceptions import DeliveryError, UnableToAct
from screenpy.protocols import Performable, Describable
from screenpy.test_utils import mock_settings

from screenpy_pyotp.abilities import AuthenticateWith2FA
from screenpy_selenium import Target
from screenpy_selenium.abilities import BrowseTheWeb
from screenpy_selenium.actions import (
    AcceptAlert,
    Chain,
    Clear,
    Click,
    DismissAlert,
    DoubleClick,
    Enter,
    Enter2FAToken,
    GoBack,
    GoForward,
    HoldDown,
    MoveMouse,
    Open,
    Pause,
    RefreshPage,
    Release,
    RespondToThePrompt,
    RightClick,
    SaveConsoleLog,
    SaveScreenshot,
    Select,
    SwitchTo,
    SwitchToTab,
    Wait,
)
from screenpy_selenium.actions.select import SelectByIndex, SelectByText, SelectByValue
from screenpy_selenium.protocols import Chainable

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select as SeleniumSelect, WebDriverWait


def get_mocked_target_and_element():
    """Get a mocked target which returns a mocked element."""
    target = mock.Mock(spec=Target)
    element = mock.Mock(spec=WebElement)
    target.found_by.return_value = element

    return target, element


class TestAcceptAlert:
    def test_can_be_instantiated(self):
        aa = AcceptAlert()

        assert isinstance(aa, AcceptAlert)

    def test_implements_protocol(self):
        a = AcceptAlert()
        assert isinstance(a, Performable)
        assert isinstance(a, Describable)

    def test_perform_accept_alert(self, Tester):
        browser = Tester.ability_to(BrowseTheWeb).browser

        AcceptAlert().perform_as(Tester)

        browser.switch_to.alert.accept.assert_called_once()

    def test_describe(self):
        assert AcceptAlert().describe() == f"Accept the alert."

class TestChain:
    def test_can_be_instantiated(self):
        c1 = Chain()

        assert isinstance(c1, Chain)

    def test_implements_protocol(self):
        c = Chain()
        assert isinstance(c, Performable)
        assert isinstance(c, Describable)

    @mock.patch("screenpy_selenium.actions.chain.ActionChains", spec=ActionChains)
    def test_perform_chain(self, mocked_chain, Tester):
        actions = [mock.Mock(add_to_chain=mock.Mock()) for _ in range(3)]

        Chain(*actions).perform_as(Tester)

        for action in actions:
            action.add_to_chain.assert_called_once_with(Tester, mocked_chain())

    def test_unchainable_action(self, Tester):
        with pytest.raises(UnableToAct):
            Chain(AcceptAlert()).perform_as(Tester)

    def test_describe(self):
        assert Chain().describe() == f"Perform a thrilling chain of actions."

class TestClear:
    def test_can_be_instantiated(self):
        c1 = Clear(None)
        c2 = Clear.the_text_from_the(None)

        assert isinstance(c1, Clear)
        assert isinstance(c2, Clear)

    def test_implements_protocol(self):
        c = Clear(None)
        assert isinstance(c, Performable)
        assert isinstance(c, Describable)

    def test_perform_clear(self, Tester):
        fake_target = Target.the("fake").located_by("//xpath")

        Clear.the_text_from(fake_target).perform_as(Tester)

        browser = Tester.ability_to(BrowseTheWeb).browser
        browser.find_element().clear.assert_called_once()

    def test_exception(self, Tester):
        target, element = get_mocked_target_and_element()
        element.clear.side_effect = WebDriverException()

        with pytest.raises(DeliveryError) as excinfo:
            Clear(target).perform_as(Tester)

        assert str(target) in str(excinfo.value)

    def test_describe(self):
        assert Clear(None).describe() == f"Clear the text from the None."


class TestClick:
    def test_can_be_instantiated(self):
        c1 = Click.on(None)
        c2 = Click.on_the(None)

        assert isinstance(c1, Click)
        assert isinstance(c2, Click)

    def test_implements_protocol(self):
        c = Click()
        assert isinstance(c, Performable)
        assert isinstance(c, Describable)
        assert isinstance(c, Chainable)

    def test_perform_click(self, Tester):
        target, element = get_mocked_target_and_element()

        Click.on(target).perform_as(Tester)

        target.found_by.assert_called_once_with(Tester)
        element.click.assert_called_once()

    def test_add_click_to_chain_without_target(self, Tester):
        chain = mock.Mock()

        Click().add_to_chain(Tester, chain)

        chain.click.assert_called_once_with(on_element=None)

    def test_add_click_to_chain_with_target(self, Tester):
        target, element = get_mocked_target_and_element()
        chain = mock.Mock()

        Click.on_the(target).add_to_chain(Tester, chain)

        chain.click.assert_called_once_with(on_element=element)

    def test_exception(self, Tester):
        target, element = get_mocked_target_and_element()
        element.click.side_effect = WebDriverException()
    
        with pytest.raises(DeliveryError) as excinfo:
            Click(target).perform_as(Tester)
    
        assert str(target) in str(excinfo.value)

    def test_no_target(self, Tester):
        with pytest.raises(UnableToAct):
            Click(None).perform_as(Tester)

    def test_describe(self):
        assert Click(None).describe() == f"Click on the None."

class TestDismissAlert:
    def test_can_be_instantiated(self):
        da = DismissAlert()

        assert isinstance(da, DismissAlert)

    def test_implements_protocol(self):
        d = DismissAlert()
        assert isinstance(d, Performable)
        assert isinstance(d, Describable)

    def test_perform_dismiss_alert(self, Tester):
        browser = Tester.ability_to(BrowseTheWeb).browser

        DismissAlert().perform_as(Tester)

        browser.switch_to.alert.dismiss.assert_called_once()

    def test_describe(self):
        assert DismissAlert().describe() == f"Dismiss the alert."

class TestDoubleClick:
    def test_can_be_instantiated(self):
        dc1 = DoubleClick()
        dc2 = DoubleClick.on_the(None)

        assert isinstance(dc1, DoubleClick)
        assert isinstance(dc2, DoubleClick)

    def test_implements_protocol(self):
        d = DoubleClick()
        assert isinstance(d, Performable)
        assert isinstance(d, Describable)
        assert isinstance(d, Chainable)

    @mock.patch("screenpy_selenium.actions.double_click.ActionChains", spec=ActionChains)
    def test_perform_double_click_without_target(self, mocked_chains, Tester):
        DoubleClick().perform_as(Tester)

        mocked_chains().double_click.assert_called_once_with(on_element=None)

    @mock.patch("screenpy_selenium.actions.double_click.ActionChains", spec=ActionChains)
    def test_perform_double_click_with_target(self, mocked_chains, Tester):
        target, element = get_mocked_target_and_element()

        DoubleClick.on_the(target).perform_as(Tester)

        target.found_by.assert_called_once_with(Tester)
        mocked_chains().double_click.assert_called_once_with(on_element=element)

    def test_chain_double_click_without_target(self, Tester):
        chain = mock.Mock(spec=ActionChains)

        DoubleClick().add_to_chain(Tester, chain)

        chain.double_click.assert_called_once_with(on_element=None)

    def test_chain_double_click_with_target(self, Tester):
        chain = mock.Mock(spec=ActionChains)
        target, element = get_mocked_target_and_element()

        DoubleClick.on_the(target).add_to_chain(Tester, chain)

        target.found_by.assert_called_once_with(Tester)
        chain.double_click.assert_called_once_with(on_element=element)

    def test_describe(self):
        assert DoubleClick(None).describe() == f"Double-click."
        assert DoubleClick(Target("blah")).describe() == f"Double-click on the blah."

class TestEnter:
    def test_can_be_instantiated(self):
        e1 = Enter.the_text("test")
        e2 = Enter.the_text("test").into(None)
        e3 = Enter.the_keys("test").into(None)
        e4 = Enter.the_text("test").into_the(None)
        e5 = Enter.the_text("test").on(None)
        e6 = Enter.the_keys("test").on(None)
        e7 = Enter.the_text("test").into(None).then_press(None)
        e8 = Enter.the_secret("test")

        assert isinstance(e1, Enter)
        assert isinstance(e2, Enter)
        assert isinstance(e3, Enter)
        assert isinstance(e4, Enter)
        assert isinstance(e5, Enter)
        assert isinstance(e6, Enter)
        assert isinstance(e7, Enter)
        assert isinstance(e8, Enter)

    def test_implements_protocol(self):
        e = Enter("")
        assert isinstance(e, Performable)
        assert isinstance(e, Describable)
        assert isinstance(e, Chainable)

    def test_secret_masks_text(self):
        """the_secret sets text_to_log to [CENSORED]"""
        text = "Keep it a secret to everybody"
        e = Enter.the_secret(text)

        assert e.text == text
        assert e.text_to_log == "[CENSORED]"

    def test_text_to_log_humanizes_keys(self):
        """unicode key values are turned into human-readable text"""
        e = Enter.the_text(Keys.ENTER)

        assert "ENTER" in e.text_to_log

    def test_perform_enter(self, Tester):
        target, element = get_mocked_target_and_element()
        text = 'Speak "Friend" and Enter'

        Enter.the_text(text).into_the(target).perform_as(Tester)

        target.found_by.assert_called_once_with(Tester)
        element.send_keys.assert_called_once_with(text)

    def test_perform_without_target_raises(self, Tester):
        with pytest.raises(UnableToAct):
            Enter.the_text("woops!").perform_as(Tester)

    def test_perform_with_then_hit(self, Tester):
        text = 'Speak "Friend" and...'
        additional = Keys.ENTER
        target, element = get_mocked_target_and_element()

        Enter.the_text(text).into_the(target).then_hit(additional).perform_as(Tester)

        assert element.send_keys.call_count == 2
        [call1_args, _], [call2_args, _] = element.send_keys.call_args_list
        assert text in call1_args
        assert additional in call2_args

    def test_chain_enter_with_target(self, Tester):
        chain = mock.Mock(spec=ActionChains)
        target, element = get_mocked_target_and_element()
        text = "Hello, Champion City."

        Enter.the_text(text).into_the(target).add_to_chain(Tester, chain)

        chain.send_keys_to_element.assert_called_once_with(element, text)

    def test_chain_enter_without_target(self, Tester):
        chain = mock.Mock(spec=ActionChains)
        text = "I am a super hero, Mother. An effete British super hero."

        Enter.the_text(text).add_to_chain(Tester, chain)

        chain.send_keys.assert_called_once_with(text)

    def test_chain_enter_with_additional_text(self, Tester):
        chain = mock.Mock(spec=ActionChains)
        text = "If just one person vomits in my pool, I'm divorcing you."
        additional = "That's fair."

        Enter.the_text(text).then_press(additional).add_to_chain(Tester, chain)

        assert chain.send_keys.call_count == 2
        [call1_args, _], [call2_args, _] = chain.send_keys.call_args_list
        assert text in call1_args
        assert additional in call2_args

    def test_exception(self, Tester):
        target, element = get_mocked_target_and_element()
        element.send_keys.side_effect = WebDriverException()

        with pytest.raises(DeliveryError) as excinfo:
            Enter("foo").into(target).perform_as(Tester)

        assert str(target) in str(excinfo.value)

    def test_describe(self):
        assert Enter("blah").into(None).describe() == f'Enter "blah" into the None.'
        assert Enter.the_secret("blah").into(None).describe() == f'Enter "[CENSORED]" into the None.'

class TestEnter2FAToken:
    def test_can_be_instantiated(self):
        e1 = Enter2FAToken.into(None)
        e2 = Enter2FAToken.into_the(None)

        assert isinstance(e1, Enter2FAToken)
        assert isinstance(e2, Enter2FAToken)

    def test_implements_protocol(self):
        e = Enter2FAToken(None)
        assert isinstance(e, Performable)
        assert isinstance(e, Describable)
        assert isinstance(e, Chainable)

    def test_perform_enter2fatoken(self, Tester):
        target, element = get_mocked_target_and_element()
        mfa_token = "12345"  # The kind of thing an idiot would have on his luggage!
        mocked_2fa = Tester.ability_to(AuthenticateWith2FA)
        mocked_2fa.to_get_token.return_value = mfa_token

        Enter2FAToken.into_the(target).perform_as(Tester)

        target.found_by.assert_called_once_with(Tester)
        element.send_keys.assert_called_once_with(mfa_token)

    def test_chain_enter2fatoken(self, Tester):
        chain = mock.Mock(spec=ActionChains)
        target, element = get_mocked_target_and_element()
        mfa_token = "12345"  # Hey, I've got the same combination on my luggage!
        mocked_2fa = Tester.ability_to(AuthenticateWith2FA)
        mocked_2fa.to_get_token.return_value = mfa_token

        Enter2FAToken.into_the(target).add_to_chain(Tester, chain)

        chain.send_keys_to_element.assert_called_once_with(element, mfa_token)

    def test_describe(self):
        assert Enter2FAToken("blah").into(None).describe() == f'Enter a 2FA token into the None.'

class TestGoBack:
    def test_can_be_instantiated(self):
        gb = GoBack()

        assert isinstance(gb, GoBack)

    def test_implements_protocol(self):
        g = GoBack()
        assert isinstance(g, Performable)
        assert isinstance(g, Describable)

    def test_perform_go_back(self, Tester):
        browser = Tester.ability_to(BrowseTheWeb).browser

        GoBack().perform_as(Tester)

        browser.back.assert_called_once()

    def test_describe(self):
        assert GoBack().describe() == f'Go back.'

class TestGoForward:
    def test_can_be_instantiated(self):
        gf = GoForward()

        assert isinstance(gf, GoForward)

    def test_implements_protocol(self):
        g = GoForward()
        assert isinstance(g, Performable)
        assert isinstance(g, Describable)

    def test_perform_go_forward(self, Tester):
        browser = Tester.ability_to(BrowseTheWeb).browser

        GoForward().perform_as(Tester)

        browser.forward.assert_called_once()

    def test_describe(self):
        assert GoForward().describe() == f'Go forward.'

class TestHoldDown:
    def test_can_be_instantiated(self):
        hd1 = HoldDown.left_mouse_button()
        hd2 = HoldDown.left_mouse_button().on_the(None)
        hd3 = HoldDown(Keys.ALT)
        hd4 = HoldDown.command_or_control_key()

        assert isinstance(hd1, HoldDown)
        assert isinstance(hd2, HoldDown)
        assert isinstance(hd3, HoldDown)
        assert isinstance(hd4, HoldDown)

    def test_implements_protocol(self):
        h = HoldDown.left_mouse_button()
        assert isinstance(h, Describable)
        assert isinstance(h, Chainable)

    @pytest.mark.parametrize(
        "platform,expected_key", [["Windows", Keys.CONTROL], ["Darwin", Keys.COMMAND]]
    )
    def test_command_or_control_key(self, platform, expected_key):
        """HoldDown figures out which key to use based on platform"""
        system_path = "screenpy_selenium.actions.hold_down.platform.system"
        with mock.patch(system_path, return_value=platform):
            hd = HoldDown.command_or_control_key()

        assert hd.key == expected_key

    def test_description_is_correct(self):
        """description is set based on the button or key"""
        hd1 = HoldDown.left_mouse_button()
        hd2 = HoldDown(Keys.LEFT_ALT)
        hd3 = HoldDown(Keys.SHIFT)

        assert hd1.description == "LEFT MOUSE BUTTON"
        assert hd2.description == "ALT"
        assert hd3.description == "SHIFT"

    def test_chain_hold_down_key(self, Tester):
        chain = mock.Mock(spec=ActionChains)
        key = Keys.PAGE_UP

        HoldDown(key).add_to_chain(Tester, chain)

        chain.key_down.assert_called_once_with(key)

    def test_chain_hold_down_mouse_button(self, Tester):
        chain = mock.Mock(spec=ActionChains)

        HoldDown.left_mouse_button().add_to_chain(Tester, chain)

        chain.click_and_hold.assert_called_once_with(on_element=None)

    def test_chain_hold_down_mouse_button_on_target(self, Tester):
        chain = mock.Mock(spec=ActionChains)
        target, element = get_mocked_target_and_element()

        HoldDown.left_mouse_button().on(target).add_to_chain(Tester, chain)

        target.found_by.assert_called_once_with(Tester)
        chain.click_and_hold.assert_called_once_with(on_element=element)

    def test_without_params_raises(self, Tester):
        chain = mock.Mock(spec=ActionChains)
        hd = HoldDown(Keys.SPACE)
        hd.description = "blah"
        hd.key = None
        with pytest.raises(UnableToAct) as excinfo:
            hd.add_to_chain(Tester, chain)

    def test_describe(self):
        assert HoldDown.left_mouse_button().describe() == f'Hold down LEFT MOUSE BUTTON.'
        assert HoldDown(Keys.SPACE).describe() == f'Hold down SPACE.'


class TestMoveMouse:
    def test_can_be_instantiated(self):
        mm1 = MoveMouse.to_the(None)
        mm2 = MoveMouse.on_the(None)
        mm3 = MoveMouse.by_offset(1, 1)
        mm4 = MoveMouse.to_the(None).with_offset(1, 1)

        assert isinstance(mm1, MoveMouse)
        assert isinstance(mm2, MoveMouse)
        assert isinstance(mm3, MoveMouse)
        assert isinstance(mm4, MoveMouse)

    def test_implements_protocol(self):
        m = MoveMouse()
        assert isinstance(m, Performable)
        assert isinstance(m, Describable)
        assert isinstance(m, Chainable)

    def test_description_is_set_by_method(self):
        """Description is built by what is included"""
        element_name = "test_element"
        coords = (1, 2)
        target = Target.the(element_name).located_by("*")
        mm1 = MoveMouse.to_the(target)
        mm2 = MoveMouse.by_offset(*coords)
        mm3 = MoveMouse.to_the(target).with_offset(*coords)

        assert element_name in mm1.description
        assert str(coords) in mm2.description
        assert element_name in mm3.description and str(coords) in mm3.description

    @mock.patch("screenpy_selenium.actions.move_mouse.ActionChains", spec=ActionChains)
    def test_perform_move_mouse_with_target(self, MockedActionChains, Tester):
        target, element = get_mocked_target_and_element()

        MoveMouse.to_the(target).perform_as(Tester)

        MockedActionChains().move_to_element.assert_called_once_with(element)

    @mock.patch("screenpy_selenium.actions.move_mouse.ActionChains", spec=ActionChains)
    def test_perform_move_mouse_by_offset(self, MockedActionChains, Tester):
        offset = (1, 2)

        MoveMouse.by_offset(*offset).perform_as(Tester)

        MockedActionChains().move_by_offset.assert_called_once_with(*offset)

    @mock.patch("screenpy_selenium.actions.move_mouse.ActionChains", spec=ActionChains)
    def test_calls_move_to_element_by_offset(self, MockedActionChains, Tester):
        target, element = get_mocked_target_and_element()
        offset = (1, 2)

        MoveMouse.to_the(target).with_offset(*offset).perform_as(Tester)

        MockedActionChains().move_to_element_with_offset.assert_called_once_with(
            element, *offset
        )

    def test_can_be_chained(self, Tester):
        offset = (1, 2)
        chain = mock.Mock(spec=ActionChains)

        MoveMouse.by_offset(*offset).add_to_chain(Tester, chain)

        chain.move_by_offset.assert_called_once_with(*offset)

    def test_without_params_raises(self, Tester):
        chain = mock.Mock(spec=ActionChains)
        with pytest.raises(UnableToAct) as excinfo:
            MoveMouse().add_to_chain(Tester, chain)

    def test_describe(self):
        assert MoveMouse().describe() == f'Move the mouse .'
        assert MoveMouse(description="over").describe() == f'Move the mouse over.'

class TestOpen:
    def test_can_be_instantiated(self):
        o1 = Open.browser_on(None)
        o2 = Open.their_browser_on(None)

        assert isinstance(o1, Open)
        assert isinstance(o2, Open)

    def test_implements_protocol(self):
        o = Open("")
        assert isinstance(o, Performable)
        assert isinstance(o, Describable)

    def test_perform_open(self, Tester):
        url = "https://localtest.test"
        browser = Tester.ability_to(BrowseTheWeb).browser

        Open.their_browser_on(url).perform_as(Tester)

        browser.get.assert_called_once_with(url)

    def test_describe(self):
        assert Open("place.com").describe() == f'Visit place.com.'

class TestPause:
    def test_can_be_instantiated(self):
        p1 = Pause(1)

        assert isinstance(p1, Pause)

    def test_implements_protocol(self):
        a = Pause(1)
        assert isinstance(a, Performable)
        assert isinstance(a, Describable)
        assert isinstance(a, Chainable)

    @mock.patch("screenpy.actions.pause.sleep", spec=time.sleep)
    def test_perform_pause(self, MockedSleep, Tester):
        length = 20

        Pause.for_(length).seconds_because("Ah ha! Testing!").perform_as(Tester)

        MockedSleep.assert_called_once_with(length)

    def test_chain_pause(self, Tester):
        length = 20
        chain = mock.Mock(spec=ActionChains)

        Pause.for_(length).seconds_because("... reasons").add_to_chain(Tester, chain)

        chain.pause.assert_called_once_with(length)

    def test_describe(self):
        assert Pause(1).second_because("moo").describe() == f"Pause for 1 second because moo."

class TestRefreshPage:
    def test_can_be_instantiated(self):
        r = RefreshPage()

        assert isinstance(r, RefreshPage)

    def test_implements_protocol(self):
        r = RefreshPage()
        assert isinstance(r, Performable)
        assert isinstance(r, Describable)

    def test_perform_refresh(self, Tester):
        browser = Tester.ability_to(BrowseTheWeb).browser

        RefreshPage().perform_as(Tester)

        browser.refresh.assert_called_once()

    def test_describe(self):
        assert RefreshPage().describe() == f"Refresh the page."

class TestRelease:
    def test_can_be_instantiated(self):
        r1 = Release.left_mouse_button()
        r2 = Release(Keys.ALT)
        r3 = Release.command_or_control_key()

        assert isinstance(r1, Release)
        assert isinstance(r2, Release)
        assert isinstance(r3, Release)

    def test_implements_protocol(self):
        r = Release.left_mouse_button()
        assert isinstance(r, Describable)
        assert isinstance(r, Chainable)

    @pytest.mark.parametrize(
        "platform,expected_key", [["Windows", Keys.CONTROL], ["Darwin", Keys.COMMAND]]
    )
    def test_command_or_control_key(self, platform, expected_key):
        """Release figures out which key to use based on platform"""
        system_path = "screenpy_selenium.actions.hold_down.platform.system"
        with mock.patch(system_path, return_value=platform):
            r = Release.command_or_control_key()

        assert r.key == expected_key

    def test_description_is_correct(self):
        """description is set based on the button or key"""
        r1 = Release.left_mouse_button()
        r2 = Release(Keys.LEFT_ALT)
        r3 = Release(Keys.SHIFT)

        assert r1.description == "LEFT MOUSE BUTTON"
        assert r2.description == "ALT"
        assert r3.description == "SHIFT"

    def test_calls_key_down(self, Tester):
        chain = mock.Mock(spec=ActionChains)
        key = Keys.ALT

        Release(key).add_to_chain(Tester, chain)

        chain.key_up.assert_called_once_with(key)

    def test_calls_release(self, Tester):
        chain = mock.Mock(spec=ActionChains)

        Release.left_mouse_button().add_to_chain(Tester, chain)

        chain.release.assert_called_once()

    def test_without_params_raises(self, Tester):
        chain = mock.Mock(spec=ActionChains)
        r = Release.left_mouse_button()
        r.lmb = False
        with pytest.raises(UnableToAct) as excinfo:
            r.add_to_chain(Tester, chain)

    def test_describe(self):
        assert Release.left_mouse_button().describe() == f"Release LEFT MOUSE BUTTON."
        assert Release(Keys.SPACE).describe() == f'Release SPACE.'

class TestRespondToThePrompt:
    def test_can_be_instantiated(self):
        rttp = RespondToThePrompt.with_("test")

        assert isinstance(rttp, RespondToThePrompt)

    def test_implements_protocol(self):
        r = RespondToThePrompt("")
        assert isinstance(r, Performable)
        assert isinstance(r, Describable)

    def test_perform_responed_to_the_prompt(self, Tester):
        text = "Hello. My name is Inigo Montoya. You killed my father. Prepare to die."
        mocked_alert = Tester.ability_to(BrowseTheWeb).browser.switch_to.alert

        RespondToThePrompt.with_(text).perform_as(Tester)

        mocked_alert.send_keys.assert_called_once_with(text)
        mocked_alert.accept.assert_called_once()

    def test_describe(self):
        assert RespondToThePrompt("baz").describe() == f'Respond to the prompt with "baz".'

class TestRightClick:
    def test_can_be_instantiated(self):
        rc1 = RightClick()
        rc2 = RightClick.on_the(None)

        assert isinstance(rc1, RightClick)
        assert isinstance(rc2, RightClick)

    def test_implements_protocol(self):
        r = RightClick()
        assert isinstance(r, Performable)
        assert isinstance(r, Describable)
        assert isinstance(r, Chainable)

    @mock.patch("screenpy_selenium.actions.right_click.ActionChains", spec=ActionChains)
    def test_can_be_performed(self, MockedActionChains, Tester):
        Tester.attempts_to(RightClick())

        MockedActionChains().context_click.assert_called_once_with(on_element=None)

    def test_add_right_click_to_chain(self, Tester):
        target, element = get_mocked_target_and_element()
        chain = mock.Mock(spec=ActionChains)

        RightClick.on_the(target).add_to_chain(Tester, chain)

        chain.context_click.assert_called_once_with(on_element=element)

    def test_chain_right_click_without_target(self, Tester):
        chain = mock.Mock(spec=ActionChains)

        RightClick().add_to_chain(Tester, chain)

        chain.context_click.assert_called_once_with(on_element=None)

    def test_describe(self):
        assert RightClick().describe() == f'Right-click.'
        assert RightClick(Target("foo")).describe() == f'Right-click on the foo.'

class TestSaveConsoleLog:
    def test_can_be_instantiated(self):
        scl1 = SaveConsoleLog("")
        scl2 = SaveConsoleLog.as_("")
        scl3 = SaveConsoleLog.as_("").and_attach_it()
        scl4 = SaveConsoleLog.as_("").and_attach_it(witch_weight="duck_weight")

        assert isinstance(scl1, SaveConsoleLog)
        assert isinstance(scl2, SaveConsoleLog)
        assert isinstance(scl3, SaveConsoleLog)
        assert isinstance(scl4, SaveConsoleLog)

    def test_implements_protocol(self):
        r = SaveConsoleLog("")
        assert isinstance(r, Performable)
        assert isinstance(r, Describable)

    def test_filepath_vs_filename(self):
        test_name = "cmcmanus.png"
        test_path = f"boondock/saints/{test_name}"

        scl = SaveConsoleLog.as_(test_path)

        assert scl.path == test_path
        assert scl.filename == test_name

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_perform_save_console_log_calls_open(self, mocked_open, Tester):
        test_path = "jhowlett/images/a_wolverine.py"
        browser = Tester.ability_to(BrowseTheWeb).browser
        browser.get_log.return_value = ["logan"]

        SaveConsoleLog(test_path).perform_as(Tester)

        mocked_open.assert_called_once_with(test_path, "w+", encoding="utf-8")

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_perform_save_console_log_writes_log(self, mocked_open, Tester):
        test_path = "ssummers/images/a_cyclops.py"
        test_log = ["shot a beam", "shot a second beam", "closed my eyes"]
        browser = Tester.ability_to(BrowseTheWeb).browser
        browser.get_log.return_value = test_log

        SaveConsoleLog(test_path).perform_as(Tester)

        file_descriptor = mocked_open()
        file_descriptor.write.assert_called_once_with("\n".join(test_log))

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    @mock.patch("screenpy_selenium.actions.save_console_log.AttachTheFile")
    def test_sends_kwargs_to_attach(self, mocked_atf, mocked_open, Tester):
        test_path = "doppelganger.png"
        test_kwargs = {"name": "Mystique"}
        browser = Tester.ability_to(BrowseTheWeb).browser
        browser.get_log.return_value = [1, 2, 3]

        SaveConsoleLog(test_path).and_attach_it(**test_kwargs).perform_as(Tester)

        mocked_atf.assert_called_once_with(test_path, **test_kwargs)

    def test_describe(self):
        assert SaveConsoleLog("pth").describe() == f'Save browser console log as pth'

class TestSaveScreenshot:
    def test_can_be_instantiated(self):
        ss1 = SaveScreenshot("")
        ss2 = SaveScreenshot.as_("")
        ss3 = SaveScreenshot.as_("").and_attach_it()
        ss4 = SaveScreenshot.as_("").and_attach_it(me="newt")

        assert isinstance(ss1, SaveScreenshot)
        assert isinstance(ss2, SaveScreenshot)
        assert isinstance(ss3, SaveScreenshot)
        assert isinstance(ss4, SaveScreenshot)

    def test_implements_protocol(self):
        r = SaveScreenshot("")
        assert isinstance(r, Performable)
        assert isinstance(r, Describable)

    def test_filepath_vs_filename(self):
        test_name = "mmcmanus.png"
        test_path = f"boondock/saints/{test_name}"

        ss = SaveScreenshot.as_(test_path)

        assert ss.path == test_path
        assert ss.filename == test_name

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_perform_calls_open_with_path(self, mocked_open, Tester):
        test_path = "bwayne/images/a_bat.py"

        SaveScreenshot(test_path).perform_as(Tester)

        mocked_open.assert_called_once_with(test_path, "wb+")

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    @mock.patch("screenpy_selenium.actions.save_screenshot.AttachTheFile")
    def test_perform_sends_kwargs_to_attach(self, mocked_atf, mocked_open, Tester):
        test_path = "souiiie.png"
        test_kwargs = {"color": "Red", "weather": "Tornado"}

        SaveScreenshot(test_path).and_attach_it(**test_kwargs).perform_as(Tester)

        mocked_atf.assert_called_once_with(test_path, **test_kwargs)

    def test_describe(self):
        assert SaveScreenshot("pth").describe() == f'Save screenshot as pth'
        
class TestSelect:
    def test_specifics_can_be_instantiated(self):
        by_index1 = Select.the_option_at_index(0)
        by_index2 = Select.the_option_at_index(0).from_(None)
        by_index3 = Select.the_option_at_index(0).from_the(None)
        by_text1 = Select.the_option_named("Option")
        by_text2 = Select.the_option_named("Option").from_(None)
        by_text3 = Select.the_option_named("Option").from_the(None)
        by_value1 = Select.the_option_with_value(1)
        by_value2 = Select.the_option_with_value(1).from_(None)
        by_value3 = Select.the_option_with_value(1).from_the(None)

        assert isinstance(by_index1, SelectByIndex)
        assert isinstance(by_index2, SelectByIndex)
        assert isinstance(by_index3, SelectByIndex)
        assert isinstance(by_text1, SelectByText)
        assert isinstance(by_text2, SelectByText)
        assert isinstance(by_text3, SelectByText)
        assert isinstance(by_value1, SelectByValue)
        assert isinstance(by_value2, SelectByValue)
        assert isinstance(by_value3, SelectByValue)


class TestSelectByIndex:
    def test_can_be_instantiated(self):
        sbi = SelectByIndex(1)

        assert isinstance(sbi, SelectByIndex)

    def test_implements_protocol(self):
        r = SelectByIndex(0)
        assert isinstance(r, Performable)
        assert isinstance(r, Describable)

    @mock.patch("screenpy_selenium.actions.select.SeleniumSelect", spec=SeleniumSelect)
    def test_perform_select_by_index(self, mocked_selselect, Tester):
        index = 1
        fake_target = Target.the("fake").located_by("//xpath")

        SelectByIndex(index).from_the(fake_target).perform_as(Tester)

        mocked_selselect().select_by_index.assert_called_once_with(str(index))

    def test_perform_complains_for_no_target(self, Tester):
        with pytest.raises(UnableToAct):
            SelectByIndex(1).perform_as(Tester)

    @mock.patch("screenpy_selenium.actions.select.SeleniumSelect", spec=SeleniumSelect)
    def test_exception(self, mocked_selselect, Tester):
        target, element = get_mocked_target_and_element()
        # element.tag_name = "select"
        mocked_selselect().select_by_index.side_effect = WebDriverException()
        
        with pytest.raises(DeliveryError) as excinfo:
            SelectByIndex(1).from_(target).perform_as(Tester)

        assert str(target) in str(excinfo.value)

    def test_describe(self):
        assert SelectByIndex(1, None).describe() == f'Select the option at index 1 from the None.'

class TestSelectByText:
    def test_can_be_instantiated(self):
        sbt = SelectByText("")

        assert isinstance(sbt, SelectByText)

    def test_implements_protocol(self):
        r = SelectByText("")
        assert isinstance(r, Performable)
        assert isinstance(r, Describable)

    @mock.patch("screenpy_selenium.actions.select.SeleniumSelect", spec=SeleniumSelect)
    def test_perform_select_by_text(self, mocked_selselect, Tester):
        text = "test"
        fake_target = Target.the("fake").located_by("//xpath")

        SelectByText(text).from_the(fake_target).perform_as(Tester)

        mocked_selselect().select_by_visible_text.assert_called_once_with(text)

    def test_perform_complains_for_no_target(self, Tester):
        with pytest.raises(UnableToAct):
            SelectByText("text").perform_as(Tester)

    @mock.patch("screenpy_selenium.actions.select.SeleniumSelect", spec=SeleniumSelect)
    def test_exception(self, mocked_selselect, Tester):
        target, element = get_mocked_target_and_element()
        mocked_selselect().select_by_visible_text.side_effect = WebDriverException()

        with pytest.raises(DeliveryError) as excinfo:
            SelectByText("blah").from_(target).perform_as(Tester)

        assert str(target) in str(excinfo.value)

    def test_describe(self):
        assert SelectByText("bar", None).describe() == f'Select the option "bar" from the None.'

class TestSelectByValue:
    def test_can_be_instantiated(self):
        sbv = SelectByValue(None)

        assert isinstance(sbv, SelectByValue)

    def test_implements_protocol(self):
        r = SelectByValue(None)
        assert isinstance(r, Performable)
        assert isinstance(r, Describable)

    @mock.patch("screenpy_selenium.actions.select.SeleniumSelect", spec=SeleniumSelect)
    def test_perform_select_by_value(self, mocked_selselect, Tester):
        value = 1337
        fake_target = Target.the("fake").located_by("//xpath")

        SelectByValue(value).from_the(fake_target).perform_as(Tester)

        mocked_selselect().select_by_value.assert_called_once_with(str(value))

    def test_perform_complains_for_no_target(self, Tester):
        with pytest.raises(UnableToAct):
            SelectByValue("value").perform_as(Tester)

    @mock.patch("screenpy_selenium.actions.select.SeleniumSelect", spec=SeleniumSelect)
    def test_exception(self, mocked_selselect, Tester):
        target, element = get_mocked_target_and_element()
        mocked_selselect().select_by_value.side_effect = WebDriverException()

        with pytest.raises(DeliveryError) as excinfo:
            SelectByValue("2").from_(target).perform_as(Tester)

        assert str(target) in str(excinfo.value)

    def test_describe(self):
        assert SelectByValue("baz", None).describe() == f'Select the option with value "baz" from the None.'

class TestSwitchTo:
    def test_can_be_instantiated(self):
        st1 = SwitchTo.the(None)
        st2 = SwitchTo.default()

        assert isinstance(st1, SwitchTo)
        assert isinstance(st2, SwitchTo)

    def test_implements_protocol(self):
        r = SwitchTo(None, "")
        assert isinstance(r, Performable)
        assert isinstance(r, Describable)

    def test_perform_switch_to_frame(self, Tester):
        target, element = get_mocked_target_and_element()
        browser = Tester.ability_to(BrowseTheWeb).browser

        SwitchTo.the(target).perform_as(Tester)

        browser.switch_to.frame.assert_called_once_with(element)

    def test_perform_switch_to_default(self, Tester):
        browser = Tester.ability_to(BrowseTheWeb).browser

        SwitchTo.default().perform_as(Tester)

        browser.switch_to.default_content.assert_called_once()

    def test_describe(self):
        assert SwitchTo.default().describe() == f'Switch to the default frame.'


class TestSwitchToTab:
    def test_can_be_instantiated(self):
        stt = SwitchToTab(1)

        assert isinstance(stt, SwitchToTab)

    def test_implements_protocol(self):
        r = SwitchToTab(0)
        assert isinstance(r, Performable)
        assert isinstance(r, Describable)

    def test_perform_switch_to_tab(self, Tester):
        number = 3
        browser = Tester.ability_to(BrowseTheWeb).browser
        browser.window_handles = range(number + 1)

        SwitchToTab(number).perform_as(Tester)

        browser.switch_to.window.assert_called_once_with(number - 1)

    def test_describe(self):
        assert SwitchToTab(2).describe() == f'Switch to tab #2.'

class TestWait:
    def test_can_be_instantiated(self):
        def foo():
            pass

        w1 = Wait.for_the(mock.Mock(spec=Target))
        w2 = Wait(0).seconds_for_the(mock.Mock(spec=Target))
        w3 = Wait().using(foo)
        w4 = Wait().using(foo).with_(mock.Mock(spec=Target))

        assert isinstance(w1, Wait)
        assert isinstance(w2, Wait)
        assert isinstance(w3, Wait)
        assert isinstance(w4, Wait)

    def test_implements_protocol(self):
        r = Wait(1)
        assert isinstance(r, Performable)
        assert isinstance(r, Describable)

    def test_default_log_message(self):
        target_name = "spam"
        w = Wait.for_the(Target.the(target_name).located_by("//eggs"))

        assert "visibility_of_element_located" in w.log_message
        assert target_name in w.log_message

    def test_custom_log_message(self):
        args = [1, Target.the("baked").located_by("//beans"), "and spam"]
        w = Wait().using(mock.Mock(), "{0}, {1}, {2}").with_(*args)

        assert all([str(arg) in w.log_message for arg in args])

    def test_set_timeout(self):
        timeout = 1000

        w = Wait(timeout).seconds_for_the(None)

        assert w.timeout == timeout

    @mock_settings(TIMEOUT=8)
    def test_adjusting_settings_timeout(self):
        w1 = Wait.for_the(mock.Mock(spec=Target))
        w2 = Wait()

        assert w1.timeout == 8
        assert w2.timeout == 8

    @mock.patch("screenpy_selenium.actions.wait.EC", spec=EC)
    @mock.patch("screenpy_selenium.actions.wait.WebDriverWait", spec=WebDriverWait)
    def test_defaults(self, mocked_webdriverwait, mocked_ec, Tester):
        test_target = Target.the("foo").located_by("//bar")
        mocked_ec.visibility_of_element_located.__name__ = "foo"
        mocked_browser = Tester.ability_to(BrowseTheWeb).browser

        Wait.for_the(test_target).perform_as(Tester)

        mocked_webdriverwait.assert_called_once_with(mocked_browser, settings.TIMEOUT)
        mocked_ec.visibility_of_element_located.assert_called_once_with(test_target)
        mocked_webdriverwait().until.assert_called_once_with(
            mocked_ec.visibility_of_element_located()
        )

    @mock.patch("screenpy_selenium.actions.wait.WebDriverWait", spec=WebDriverWait)
    def test_custom(self, mocked_webdriverwait, Tester):
        test_func = mock.Mock()
        test_func.__name__ = "foo"

        Wait().using(test_func).perform_as(Tester)

        mocked_webdriverwait().until.assert_called_once_with(test_func())

    @mock.patch("screenpy_selenium.actions.wait.EC", spec=EC)
    @mock.patch("screenpy_selenium.actions.wait.WebDriverWait", spec=WebDriverWait)
    def test_exception(self, mocked_webdriverwait, mocked_ec, Tester):
        test_target = Target.the("foo").located_by("//bar")
        mocked_ec.visibility_of_element_located.__name__ = "foo"
        mocked_webdriverwait().until.side_effect = WebDriverException

        with pytest.raises(DeliveryError) as excinfo:
            Wait.for_the(test_target).perform_as(Tester)

        assert str(test_target) in str(excinfo.value)

    def test_helpful_methods(self):
        assert Wait(1).to_appear().condition == EC.visibility_of_element_located
        assert Wait(1).to_be_clickable().condition == EC.element_to_be_clickable
        assert Wait(1).to_disappear().condition == EC.invisibility_of_element_located
        assert Wait(1).to_contain_text("").condition == EC.text_to_be_present_in_element
        

    def test_describe(self):
        assert Wait(2).describe() == f'Wait 2 seconds using visibility_of_element_located with [].'
        assert Wait(5).seconds_for_the(None).to_contain_text("foo").describe() == f'Wait 5 seconds for "foo" to appear in the None....'
