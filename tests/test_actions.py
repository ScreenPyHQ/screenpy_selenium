from unittest import mock

import pytest
from screenpy import Actor, settings
from screenpy.exceptions import DeliveryError, UnableToAct
from screenpy.protocols import Describable, Performable
from screenpy.test_utils import mock_settings
from screenpy_pyotp.abilities import AuthenticateWith2FA
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from unittest_protocols import ChainableAction
from useful_mocks import (
    get_mocked_chain,
    get_mocked_target,
    get_mocked_target_and_element,
    get_mocked_browser,
)

from screenpy_selenium import Target
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

TARGET = get_mocked_target()


class TestAcceptAlert:
    def test_can_be_instantiated(self) -> None:
        aa = AcceptAlert()

        assert isinstance(aa, AcceptAlert)

    def test_implements_protocol(self) -> None:
        a = AcceptAlert()

        assert isinstance(a, Performable)
        assert isinstance(a, Describable)

    def test_perform_accept_alert(self, Tester) -> None:
        browser = get_mocked_browser(Tester)

        AcceptAlert().perform_as(Tester)

        browser.switch_to.alert.accept.assert_called_once()

    def test_describe(self) -> None:
        assert AcceptAlert().describe() == "Accept the alert."


class TestChain:
    def test_can_be_instantiated(self) -> None:
        c1 = Chain()

        assert isinstance(c1, Chain)

    def test_implements_protocol(self) -> None:
        c = Chain()

        assert isinstance(c, Performable)
        assert isinstance(c, Describable)

    @mock.patch("screenpy_selenium.actions.chain.ActionChains", autospec=True)
    def test_perform_chain(self, mocked_chain, Tester) -> None:
        actions = [
            mock.create_autospec(ChainableAction, instance=True) for _ in range(3)
        ]
        browser = get_mocked_browser(Tester)

        Chain(*actions).perform_as(Tester)

        for action in actions:
            action.add_to_chain.assert_called_once_with(Tester, mocked_chain(browser))

    def test_unchainable_action(self, Tester) -> None:
        with pytest.raises(UnableToAct):
            Chain(AcceptAlert()).perform_as(Tester)  # type: ignore

    def test_describe(self) -> None:
        assert Chain().describe() == "Perform a thrilling chain of actions."


class TestClear:
    def test_can_be_instantiated(self) -> None:
        c1 = Clear(TARGET)
        c2 = Clear.the_text_from_the(TARGET)

        assert isinstance(c1, Clear)
        assert isinstance(c2, Clear)

    def test_implements_protocol(self) -> None:
        c = Clear(TARGET)
        assert isinstance(c, Performable)
        assert isinstance(c, Describable)

    def test_perform_clear(self, Tester) -> None:
        fake_target = Target.the("fake").located_by("//xpath")

        Clear.the_text_from(fake_target).perform_as(Tester)

        browser = get_mocked_browser(Tester)
        browser.find_element().clear.assert_called_once()

    def test_exception(self, Tester) -> None:
        target, element = get_mocked_target_and_element()
        element.clear.side_effect = WebDriverException()

        with pytest.raises(DeliveryError) as excinfo:
            Clear(target).perform_as(Tester)

        assert str(target) in str(excinfo.value)

    def test_describe(self) -> None:
        assert Clear(TARGET).describe() == f"Clear the text from the {TARGET}."


class TestClick:
    def test_can_be_instantiated(self) -> None:
        c1 = Click.on(TARGET)
        c2 = Click.on_the(TARGET)

        assert isinstance(c1, Click)
        assert isinstance(c2, Click)

    def test_implements_protocol(self) -> None:
        c = Click()

        assert isinstance(c, Performable)
        assert isinstance(c, Describable)
        assert isinstance(c, Chainable)

    def test_perform_click(self, Tester: Actor) -> None:
        target, element = get_mocked_target_and_element()

        Click.on(target).perform_as(Tester)

        target.found_by.assert_called_once_with(Tester)
        element.click.assert_called_once()

    def test_add_click_to_chain_without_target(self, Tester) -> None:
        chain = get_mocked_chain()

        Click().add_to_chain(Tester, chain)

        chain.click.assert_called_once_with(on_element=None)

    def test_add_click_to_chain_with_target(self, Tester) -> None:
        target, element = get_mocked_target_and_element()
        chain = get_mocked_chain()

        Click.on_the(target).add_to_chain(Tester, chain)

        chain.click.assert_called_once_with(on_element=element)

    def test_exception(self, Tester) -> None:
        target, element = get_mocked_target_and_element()
        element.click.side_effect = WebDriverException()

        with pytest.raises(DeliveryError) as excinfo:
            Click(target).perform_as(Tester)

        assert str(target) in str(excinfo.value)

    def test_no_target(self, Tester) -> None:
        with pytest.raises(UnableToAct):
            Click(None).perform_as(Tester)

    def test_describe(self) -> None:
        assert Click(None).describe() == "Click on the None."


class TestDismissAlert:
    def test_can_be_instantiated(self) -> None:
        da = DismissAlert()

        assert isinstance(da, DismissAlert)

    def test_implements_protocol(self) -> None:
        d = DismissAlert()

        assert isinstance(d, Performable)
        assert isinstance(d, Describable)

    def test_perform_dismiss_alert(self, Tester) -> None:
        browser = get_mocked_browser(Tester)

        DismissAlert().perform_as(Tester)

        browser.switch_to.alert.dismiss.assert_called_once()

    def test_describe(self) -> None:
        assert DismissAlert().describe() == "Dismiss the alert."


class TestDoubleClick:
    def test_can_be_instantiated(self) -> None:
        dc1 = DoubleClick()
        dc2 = DoubleClick.on_the(TARGET)

        assert isinstance(dc1, DoubleClick)
        assert isinstance(dc2, DoubleClick)

    def test_implements_protocol(self) -> None:
        d = DoubleClick()

        assert isinstance(d, Performable)
        assert isinstance(d, Describable)
        assert isinstance(d, Chainable)

    @mock.patch("screenpy_selenium.actions.double_click.ActionChains", autospec=True)
    def test_perform_double_click_without_target(self, mocked_chains, Tester) -> None:
        DoubleClick().perform_as(Tester)

        browser = get_mocked_browser(Tester)
        mocked_chains(browser).double_click.assert_called_once_with(on_element=None)

    @mock.patch("screenpy_selenium.actions.double_click.ActionChains", autospec=True)
    def test_perform_double_click_with_target(self, mocked_chains, Tester) -> None:
        target, element = get_mocked_target_and_element()
        browser = get_mocked_browser(Tester)
        DoubleClick.on_the(target).perform_as(Tester)

        target.found_by.assert_called_once_with(Tester)
        mocked_chains(browser).double_click.assert_called_once_with(on_element=element)

    def test_chain_double_click_without_target(self, Tester) -> None:
        chain = get_mocked_chain()

        DoubleClick().add_to_chain(Tester, chain)

        chain.double_click.assert_called_once_with(on_element=None)

    def test_chain_double_click_with_target(self, Tester) -> None:
        chain = get_mocked_chain()
        target, element = get_mocked_target_and_element()

        DoubleClick.on_the(target).add_to_chain(Tester, chain)

        target.found_by.assert_called_once_with(Tester)
        chain.double_click.assert_called_once_with(on_element=element)

    def test_describe(self) -> None:
        assert DoubleClick(None).describe() == "Double-click."
        assert DoubleClick(Target("blah")).describe() == "Double-click on the blah."


class TestEnter:
    def test_can_be_instantiated(self) -> None:
        e1 = Enter.the_text("test")
        e2 = Enter.the_text("test").into(TARGET)
        e3 = Enter.the_keys("test").into(TARGET)
        e4 = Enter.the_text("test").into_the(TARGET)
        e5 = Enter.the_text("test").on(TARGET)
        e6 = Enter.the_keys("test").on(TARGET)
        e7 = Enter.the_text("test").into(TARGET).then_press("A")
        e8 = Enter.the_secret("test")

        assert isinstance(e1, Enter)
        assert isinstance(e2, Enter)
        assert isinstance(e3, Enter)
        assert isinstance(e4, Enter)
        assert isinstance(e5, Enter)
        assert isinstance(e6, Enter)
        assert isinstance(e7, Enter)
        assert isinstance(e8, Enter)

    def test_implements_protocol(self) -> None:
        e = Enter("")

        assert isinstance(e, Performable)
        assert isinstance(e, Describable)
        assert isinstance(e, Chainable)

    def test_secret_masks_text(self) -> None:
        """the_secret sets text_to_log to [CENSORED]"""
        text = "Keep it a secret to everybody"
        e = Enter.the_secret(text)

        assert e.text == text
        assert e.text_to_log == "[CENSORED]"

    def test_text_to_log_humanizes_keys(self) -> None:
        """unicode key values are turned into human-readable text"""
        e = Enter.the_text(Keys.ENTER)

        assert "ENTER" in e.text_to_log

    def test_perform_enter(self, Tester) -> None:
        target, element = get_mocked_target_and_element()
        text = 'Speak "Friend" and Enter'

        Enter.the_text(text).into_the(target).perform_as(Tester)

        target.found_by.assert_called_once_with(Tester)
        element.send_keys.assert_called_once_with(text)

    def test_perform_without_target_raises(self, Tester) -> None:
        with pytest.raises(UnableToAct):
            Enter.the_text("woops!").perform_as(Tester)

    def test_perform_with_then_hit(self, Tester) -> None:
        text = 'Speak "Friend" and...'
        additional = Keys.ENTER
        target, element = get_mocked_target_and_element()

        Enter.the_text(text).into_the(target).then_hit(additional).perform_as(Tester)

        assert element.send_keys.call_count == 2
        [call1_args, _], [call2_args, _] = element.send_keys.call_args_list
        assert text in call1_args
        assert additional in call2_args

    def test_chain_enter_with_target(self, Tester) -> None:
        chain = get_mocked_chain()
        target, element = get_mocked_target_and_element()
        text = "Hello, Champion City."

        Enter.the_text(text).into_the(target).add_to_chain(Tester, chain)

        chain.send_keys_to_element.assert_called_once_with(element, text)

    def test_chain_enter_without_target(self, Tester) -> None:
        chain = get_mocked_chain()
        text = "I am a super hero, Mother. An effete British super hero."

        Enter.the_text(text).add_to_chain(Tester, chain)

        chain.send_keys.assert_called_once_with(text)

    def test_chain_enter_with_additional_text(self, Tester) -> None:
        chain = get_mocked_chain()
        text = "If just one person vomits in my pool, I'm divorcing you."
        additional = "That's fair."

        Enter.the_text(text).then_press(additional).add_to_chain(Tester, chain)

        assert chain.send_keys.call_count == 2
        [call1_args, _], [call2_args, _] = chain.send_keys.call_args_list
        assert text in call1_args
        assert additional in call2_args

    def test_exception(self, Tester) -> None:
        target, element = get_mocked_target_and_element()
        element.send_keys.side_effect = WebDriverException()

        with pytest.raises(DeliveryError) as excinfo:
            Enter("foo").into(target).perform_as(Tester)

        assert str(target) in str(excinfo.value)

    def test_describe(self) -> None:
        assert (
            Enter("blah").into(TARGET).describe() == f'Enter "blah" into the {TARGET}.'
        )
        assert (
            Enter.the_secret("blah").into(TARGET).describe()
            == f'Enter "[CENSORED]" into the {TARGET}.'
        )


class TestEnter2FAToken:
    def test_can_be_instantiated(self) -> None:
        e1 = Enter2FAToken.into(TARGET)
        e2 = Enter2FAToken.into_the(TARGET)

        assert isinstance(e1, Enter2FAToken)
        assert isinstance(e2, Enter2FAToken)

    def test_implements_protocol(self) -> None:
        e = Enter2FAToken(TARGET)
        assert isinstance(e, Performable)
        assert isinstance(e, Describable)
        assert isinstance(e, Chainable)

    def test_perform_enter2fatoken(self, Tester) -> None:
        target, element = get_mocked_target_and_element()
        mfa_token = "12345"  # The kind of thing an idiot would have on his luggage!
        mocked_2fa = Tester.ability_to(AuthenticateWith2FA)
        mocked_2fa.to_get_token.return_value = mfa_token

        Enter2FAToken.into_the(target).perform_as(Tester)

        target.found_by.assert_called_once_with(Tester)
        element.send_keys.assert_called_once_with(mfa_token)

    def test_chain_enter2fatoken(self, Tester) -> None:
        chain = get_mocked_chain()
        target, element = get_mocked_target_and_element()
        mfa_token = "12345"  # Hey, I've got the same combination on my luggage!
        mocked_2fa = Tester.ability_to(AuthenticateWith2FA)
        mocked_2fa.to_get_token.return_value = mfa_token

        Enter2FAToken.into_the(target).add_to_chain(Tester, chain)

        chain.send_keys_to_element.assert_called_once_with(element, mfa_token)

    def test_describe(self) -> None:
        assert (
            Enter2FAToken(TARGET).describe() == f"Enter a 2FA token into the {TARGET}."
        )


class TestGoBack:
    def test_can_be_instantiated(self) -> None:
        gb = GoBack()

        assert isinstance(gb, GoBack)

    def test_implements_protocol(self) -> None:
        g = GoBack()

        assert isinstance(g, Performable)
        assert isinstance(g, Describable)

    def test_perform_go_back(self, Tester) -> None:
        browser = get_mocked_browser(Tester)

        GoBack().perform_as(Tester)

        browser.back.assert_called_once()

    def test_describe(self) -> None:
        assert GoBack().describe() == "Go back."


class TestGoForward:
    def test_can_be_instantiated(self) -> None:
        gf = GoForward()

        assert isinstance(gf, GoForward)

    def test_implements_protocol(self) -> None:
        g = GoForward()

        assert isinstance(g, Performable)
        assert isinstance(g, Describable)

    def test_perform_go_forward(self, Tester) -> None:
        browser = get_mocked_browser(Tester)

        GoForward().perform_as(Tester)

        browser.forward.assert_called_once()

    def test_describe(self) -> None:
        assert GoForward().describe() == "Go forward."


class TestHoldDown:
    def test_can_be_instantiated(self) -> None:
        hd1 = HoldDown.left_mouse_button()
        hd2 = HoldDown.left_mouse_button().on_the(TARGET)
        hd3 = HoldDown(Keys.ALT)
        hd4 = HoldDown.command_or_control_key()

        assert isinstance(hd1, HoldDown)
        assert isinstance(hd2, HoldDown)
        assert isinstance(hd3, HoldDown)
        assert isinstance(hd4, HoldDown)

    def test_implements_protocol(self) -> None:
        h = HoldDown.left_mouse_button()

        assert isinstance(h, Describable)
        assert isinstance(h, Chainable)

    @pytest.mark.parametrize(
        "platform,expected_key", [["Windows", Keys.CONTROL], ["Darwin", Keys.COMMAND]]
    )
    def test_command_or_control_key(self, platform, expected_key) -> None:
        """HoldDown figures out which key to use based on platform"""
        system_path = "screenpy_selenium.actions.hold_down.platform.system"
        with mock.patch(system_path, return_value=platform, autospec=True):
            hd = HoldDown.command_or_control_key()

        assert hd.key == expected_key

    def test_description_is_correct(self) -> None:
        """description is set based on the button or key"""
        hd1 = HoldDown.left_mouse_button()
        hd2 = HoldDown(Keys.LEFT_ALT)
        hd3 = HoldDown(Keys.SHIFT)

        assert hd1.description == "LEFT MOUSE BUTTON"
        assert hd2.description == "ALT"
        assert hd3.description == "SHIFT"

    def test_chain_hold_down_key(self, Tester) -> None:
        chain = get_mocked_chain()
        key = Keys.PAGE_UP

        HoldDown(key).add_to_chain(Tester, chain)

        chain.key_down.assert_called_once_with(key)

    def test_chain_hold_down_mouse_button(self, Tester) -> None:
        chain = get_mocked_chain()

        HoldDown.left_mouse_button().add_to_chain(Tester, chain)

        chain.click_and_hold.assert_called_once_with(on_element=None)

    def test_chain_hold_down_mouse_button_on_target(self, Tester) -> None:
        chain = get_mocked_chain()
        target, element = get_mocked_target_and_element()

        HoldDown.left_mouse_button().on(target).add_to_chain(Tester, chain)

        target.found_by.assert_called_once_with(Tester)
        chain.click_and_hold.assert_called_once_with(on_element=element)

    def test_without_params_raises(self, Tester) -> None:
        chain = get_mocked_chain()
        hd = HoldDown(Keys.SPACE)
        hd.description = "blah"
        hd.key = None

        with pytest.raises(UnableToAct):
            hd.add_to_chain(Tester, chain)

    def test_describe(self) -> None:
        assert HoldDown.left_mouse_button().describe() == "Hold down LEFT MOUSE BUTTON."
        assert HoldDown(Keys.SPACE).describe() == "Hold down SPACE."


class TestMoveMouse:
    def test_can_be_instantiated(self) -> None:
        mm1 = MoveMouse.to_the(TARGET)
        mm2 = MoveMouse.on_the(TARGET)
        mm3 = MoveMouse.by_offset(1, 1)
        mm4 = MoveMouse.to_the(TARGET).with_offset(1, 1)

        assert isinstance(mm1, MoveMouse)
        assert isinstance(mm2, MoveMouse)
        assert isinstance(mm3, MoveMouse)
        assert isinstance(mm4, MoveMouse)

    def test_implements_protocol(self) -> None:
        m = MoveMouse()

        assert isinstance(m, Performable)
        assert isinstance(m, Describable)
        assert isinstance(m, Chainable)

    def test_description_is_set_by_method(self) -> None:
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

    @mock.patch("screenpy_selenium.actions.move_mouse.ActionChains", autospec=True)
    def test_perform_move_mouse_with_target(self, MockedActionChains, Tester) -> None:
        target, element = get_mocked_target_and_element()
        browser = get_mocked_browser(Tester)

        MoveMouse.to_the(target).perform_as(Tester)

        MockedActionChains(browser).move_to_element.assert_called_once_with(element)

    @mock.patch("screenpy_selenium.actions.move_mouse.ActionChains", autospec=True)
    def test_perform_move_mouse_by_offset(self, MockedActionChains, Tester) -> None:
        offset = (1, 2)
        browser = get_mocked_browser(Tester)

        MoveMouse.by_offset(*offset).perform_as(Tester)

        MockedActionChains(browser).move_by_offset.assert_called_once_with(*offset)

    @mock.patch("screenpy_selenium.actions.move_mouse.ActionChains", autospec=True)
    def test_calls_move_to_element_by_offset(self, MockedActionChains, Tester) -> None:
        target, element = get_mocked_target_and_element()
        offset = (1, 2)
        browser = get_mocked_browser(Tester)

        MoveMouse.to_the(target).with_offset(*offset).perform_as(Tester)

        MockedActionChains(browser).move_to_element_with_offset.assert_called_once_with(
            element, *offset
        )

    def test_can_be_chained(self, Tester) -> None:
        offset = (1, 2)
        chain = get_mocked_chain()

        MoveMouse.by_offset(*offset).add_to_chain(Tester, chain)

        chain.move_by_offset.assert_called_once_with(*offset)

    def test_without_params_raises(self, Tester) -> None:
        chain = get_mocked_chain()

        with pytest.raises(UnableToAct):
            MoveMouse().add_to_chain(Tester, chain)

    def test_describe(self) -> None:
        assert MoveMouse().describe() == "Move the mouse ."
        assert MoveMouse(description="over").describe() == "Move the mouse over."


class TestOpen:
    def test_can_be_instantiated(self) -> None:
        o1 = Open.browser_on(None)
        o2 = Open.their_browser_on(None)

        assert isinstance(o1, Open)
        assert isinstance(o2, Open)

    def test_implements_protocol(self) -> None:
        o = Open("")

        assert isinstance(o, Performable)
        assert isinstance(o, Describable)

    def test_perform_open(self, Tester) -> None:
        url = "https://localtest.test"
        browser = get_mocked_browser(Tester)

        Open.their_browser_on(url).perform_as(Tester)

        browser.get.assert_called_once_with(url)

    def test_describe(self) -> None:
        assert Open("place.com").describe() == "Visit place.com."


class TestPause:
    def test_can_be_instantiated(self) -> None:
        p1 = Pause(1)

        assert isinstance(p1, Pause)

    def test_implements_protocol(self) -> None:
        a = Pause(1)

        assert isinstance(a, Performable)
        assert isinstance(a, Describable)
        assert isinstance(a, Chainable)

    @mock.patch("screenpy.actions.pause.sleep", autospec=True)
    def test_perform_pause(self, MockedSleep, Tester) -> None:
        length = 20

        Pause.for_(length).seconds_because("Ah ha! Testing!").perform_as(Tester)

        MockedSleep.assert_called_once_with(length)

    def test_chain_pause(self, Tester) -> None:
        length = 20
        chain = get_mocked_chain()

        Pause.for_(length).seconds_because("... reasons").add_to_chain(Tester, chain)

        chain.pause.assert_called_once_with(length)

    def test_describe(self) -> None:
        assert (
            Pause(1).second_because("moo").describe()
            == "Pause for 1 second because moo."
        )


class TestRefreshPage:
    def test_can_be_instantiated(self) -> None:
        r = RefreshPage()

        assert isinstance(r, RefreshPage)

    def test_implements_protocol(self) -> None:
        r = RefreshPage()

        assert isinstance(r, Performable)
        assert isinstance(r, Describable)

    def test_perform_refresh(self, Tester) -> None:
        browser = get_mocked_browser(Tester)

        RefreshPage().perform_as(Tester)

        browser.refresh.assert_called_once()

    def test_describe(self) -> None:
        assert RefreshPage().describe() == "Refresh the page."


class TestRelease:
    def test_can_be_instantiated(self) -> None:
        r1 = Release.left_mouse_button()
        r2 = Release(Keys.ALT)
        r3 = Release.command_or_control_key()

        assert isinstance(r1, Release)
        assert isinstance(r2, Release)
        assert isinstance(r3, Release)

    def test_implements_protocol(self) -> None:
        r = Release.left_mouse_button()

        assert isinstance(r, Describable)
        assert isinstance(r, Chainable)

    @pytest.mark.parametrize(
        "platform,expected_key", [["Windows", Keys.CONTROL], ["Darwin", Keys.COMMAND]]
    )
    def test_command_or_control_key(self, platform, expected_key) -> None:
        """Release figures out which key to use based on platform"""
        system_path = "screenpy_selenium.actions.hold_down.platform.system"
        with mock.patch(system_path, return_value=platform, autospec=True):
            r = Release.command_or_control_key()

        assert r.key == expected_key

    def test_description_is_correct(self) -> None:
        """description is set based on the button or key"""
        r1 = Release.left_mouse_button()
        r2 = Release(Keys.LEFT_ALT)
        r3 = Release(Keys.SHIFT)

        assert r1.description == "LEFT MOUSE BUTTON"
        assert r2.description == "ALT"
        assert r3.description == "SHIFT"

    def test_calls_key_down(self, Tester) -> None:
        chain = get_mocked_chain()
        key = Keys.ALT

        Release(key).add_to_chain(Tester, chain)

        chain.key_up.assert_called_once_with(key)

    def test_calls_release(self, Tester) -> None:
        chain = get_mocked_chain()

        Release.left_mouse_button().add_to_chain(Tester, chain)

        chain.release.assert_called_once()

    def test_without_params_raises(self, Tester) -> None:
        chain = get_mocked_chain()
        r = Release.left_mouse_button()
        r.lmb = False
        with pytest.raises(UnableToAct):
            r.add_to_chain(Tester, chain)

    def test_describe(self) -> None:
        assert Release.left_mouse_button().describe() == "Release LEFT MOUSE BUTTON."
        assert Release(Keys.SPACE).describe() == "Release SPACE."


class TestRespondToThePrompt:
    def test_can_be_instantiated(self) -> None:
        rttp = RespondToThePrompt.with_("test")

        assert isinstance(rttp, RespondToThePrompt)

    def test_implements_protocol(self) -> None:
        r = RespondToThePrompt("")

        assert isinstance(r, Performable)
        assert isinstance(r, Describable)

    def test_perform_responed_to_the_prompt(self, Tester) -> None:
        text = "Hello. My name is Inigo Montoya. You killed my father. Prepare to die."
        mocked_alert = get_mocked_browser(Tester).switch_to.alert

        RespondToThePrompt.with_(text).perform_as(Tester)

        mocked_alert.send_keys.assert_called_once_with(text)
        mocked_alert.accept.assert_called_once()

    def test_describe(self) -> None:
        assert (
            RespondToThePrompt("baz").describe() == 'Respond to the prompt with "baz".'
        )


class TestRightClick:
    def test_can_be_instantiated(self) -> None:
        rc1 = RightClick()
        rc2 = RightClick.on_the(TARGET)

        assert isinstance(rc1, RightClick)
        assert isinstance(rc2, RightClick)

    def test_implements_protocol(self):
        rc = RightClick()

        assert isinstance(rc, Performable)
        assert isinstance(rc, Describable)
        assert isinstance(rc, Chainable)

    @mock.patch("screenpy_selenium.actions.right_click.ActionChains", autospec=True)
    def test_can_be_performed(self, MockedActionChains, Tester) -> None:
        Tester.attempts_to(RightClick())
        browser = get_mocked_browser(Tester)

        MockedActionChains(browser).context_click.assert_called_once_with(
            on_element=None
        )

    def test_add_right_click_to_chain(self, Tester) -> None:
        target, element = get_mocked_target_and_element()
        chain = get_mocked_chain()

        RightClick.on_the(target).add_to_chain(Tester, chain)

        chain.context_click.assert_called_once_with(on_element=element)

    def test_chain_right_click_without_target(self, Tester) -> None:
        chain = get_mocked_chain()

        RightClick().add_to_chain(Tester, chain)

        chain.context_click.assert_called_once_with(on_element=None)

    def test_describe(self) -> None:
        assert RightClick().describe() == "Right-click."
        assert RightClick(Target("foo")).describe() == "Right-click on the foo."


class TestSaveConsoleLog:
    def test_can_be_instantiated(self) -> None:
        scl1 = SaveConsoleLog("")
        scl2 = SaveConsoleLog.as_("")
        scl3 = SaveConsoleLog.as_("").and_attach_it()
        scl4 = SaveConsoleLog.as_("").and_attach_it(witch_weight="duck_weight")

        assert isinstance(scl1, SaveConsoleLog)
        assert isinstance(scl2, SaveConsoleLog)
        assert isinstance(scl3, SaveConsoleLog)
        assert isinstance(scl4, SaveConsoleLog)

    def test_implements_protocol(self) -> None:
        r = SaveConsoleLog("")

        assert isinstance(r, Performable)
        assert isinstance(r, Describable)

    def test_filepath_vs_filename(self) -> None:
        test_name = "cmcmanus.png"
        test_path = f"boondock/saints/{test_name}"

        scl = SaveConsoleLog.as_(test_path)

        assert scl.path == test_path
        assert scl.filename == test_name

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_perform_save_console_log_calls_open(self, mocked_open, Tester) -> None:
        test_path = "jhowlett/images/a_wolverine.py"
        browser = get_mocked_browser(Tester)
        browser.get_log.return_value = ["logan"]

        SaveConsoleLog(test_path).perform_as(Tester)

        mocked_open.assert_called_once_with(test_path, "w+", encoding="utf-8")

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_perform_save_console_log_writes_log(self, mocked_open, Tester) -> None:
        test_path = "ssummers/images/a_cyclops.py"
        test_log = ["shot a beam", "shot a second beam", "closed my eyes"]
        browser = get_mocked_browser(Tester)
        browser.get_log.return_value = test_log

        SaveConsoleLog(test_path).perform_as(Tester)

        file_descriptor = mocked_open()
        file_descriptor.write.assert_called_once_with("\n".join(test_log))

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    @mock.patch(
        "screenpy_selenium.actions.save_console_log.AttachTheFile", autospec=True
    )
    def test_sends_kwargs_to_attach(self, mocked_atf, mocked_open, Tester) -> None:
        test_path = "doppelganger.png"
        test_kwargs = {"name": "Mystique"}
        browser = get_mocked_browser(Tester)
        browser.get_log.return_value = [1, 2, 3]

        SaveConsoleLog(test_path).and_attach_it(**test_kwargs).perform_as(Tester)

        mocked_atf.assert_called_once_with(test_path, **test_kwargs)

    def test_describe(self) -> None:
        assert SaveConsoleLog("pth").describe() == "Save browser console log as pth"


class TestSaveScreenshot:
    def test_can_be_instantiated(self) -> None:
        ss1 = SaveScreenshot("")
        ss2 = SaveScreenshot.as_("")
        ss3 = SaveScreenshot.as_("").and_attach_it()
        ss4 = SaveScreenshot.as_("").and_attach_it(me="newt")

        assert isinstance(ss1, SaveScreenshot)
        assert isinstance(ss2, SaveScreenshot)
        assert isinstance(ss3, SaveScreenshot)
        assert isinstance(ss4, SaveScreenshot)

    def test_implements_protocol(self) -> None:
        r = SaveScreenshot("")

        assert isinstance(r, Performable)
        assert isinstance(r, Describable)

    def test_filepath_vs_filename(self) -> None:
        test_name = "mmcmanus.png"
        test_path = f"boondock/saints/{test_name}"

        ss = SaveScreenshot.as_(test_path)

        assert ss.path == test_path
        assert ss.filename == test_name

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_perform_calls_open_with_path(self, mocked_open, Tester) -> None:
        test_path = "bwayne/images/a_bat.py"

        SaveScreenshot(test_path).perform_as(Tester)

        mocked_open.assert_called_once_with(test_path, "wb+")

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    @mock.patch(
        "screenpy_selenium.actions.save_screenshot.AttachTheFile", autospec=True
    )
    def test_perform_sends_kwargs_to_attach(
        self, mocked_atf, mocked_open, Tester
    ) -> None:
        test_path = "souiiie.png"
        test_kwargs = {"color": "Red", "weather": "Tornado"}

        SaveScreenshot(test_path).and_attach_it(**test_kwargs).perform_as(Tester)

        mocked_atf.assert_called_once_with(test_path, **test_kwargs)

    def test_describe(self) -> None:
        assert SaveScreenshot("pth").describe() == "Save screenshot as pth"


class TestSelect:
    def test_specifics_can_be_instantiated(self) -> None:
        by_index1 = Select.the_option_at_index(0)
        by_index2 = Select.the_option_at_index(0).from_(TARGET)
        by_index3 = Select.the_option_at_index(0).from_the(TARGET)
        by_text1 = Select.the_option_named("Option")
        by_text2 = Select.the_option_named("Option").from_(TARGET)
        by_text3 = Select.the_option_named("Option").from_the(TARGET)
        by_value1 = Select.the_option_with_value(1)
        by_value2 = Select.the_option_with_value(1).from_(TARGET)
        by_value3 = Select.the_option_with_value(1).from_the(TARGET)

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
    def test_can_be_instantiated(self) -> None:
        sbi = SelectByIndex(1)

        assert isinstance(sbi, SelectByIndex)

    def test_implements_protocol(self) -> None:
        r = SelectByIndex(0)

        assert isinstance(r, Performable)
        assert isinstance(r, Describable)

    @mock.patch("screenpy_selenium.actions.select.SeleniumSelect", autospec=True)
    def test_perform_select_by_index(self, mocked_selselect, Tester) -> None:
        index = 1
        fake_target = Target.the("fake").located_by("//xpath")

        SelectByIndex(index).from_the(fake_target).perform_as(Tester)

        mocked_selselect(fake_target).select_by_index.assert_called_once_with(
            str(index)
        )

    def test_perform_complains_for_no_target(self, Tester) -> None:
        with pytest.raises(UnableToAct):
            SelectByIndex(1).perform_as(Tester)

    @mock.patch("screenpy_selenium.actions.select.SeleniumSelect", autospec=True)
    def test_exception(self, mocked_selselect, Tester) -> None:
        target, element = get_mocked_target_and_element()
        mocked_selselect(element).select_by_index.side_effect = WebDriverException()

        with pytest.raises(DeliveryError) as excinfo:
            SelectByIndex(1).from_(target).perform_as(Tester)

        assert str(target) in str(excinfo.value)

    def test_describe(self) -> None:
        assert (
            SelectByIndex(1, None).describe()
            == "Select the option at index 1 from the None."
        )


class TestSelectByText:
    def test_can_be_instantiated(self) -> None:
        sbt = SelectByText("")

        assert isinstance(sbt, SelectByText)

    def test_implements_protocol(self) -> None:
        r = SelectByText("")

        assert isinstance(r, Performable)
        assert isinstance(r, Describable)

    @mock.patch("screenpy_selenium.actions.select.SeleniumSelect", autospec=True)
    def test_perform_select_by_text(self, mocked_selselect, Tester) -> None:
        text = "test"
        fake_target = Target.the("fake").located_by("//xpath")

        SelectByText(text).from_the(fake_target).perform_as(Tester)

        mocked_selselect(fake_target).select_by_visible_text.assert_called_once_with(
            text
        )

    def test_perform_complains_for_no_target(self, Tester) -> None:
        with pytest.raises(UnableToAct):
            SelectByText("text").perform_as(Tester)

    @mock.patch("screenpy_selenium.actions.select.SeleniumSelect", autospec=True)
    def test_exception(self, mocked_selselect, Tester) -> None:
        target, element = get_mocked_target_and_element()
        mocked_selselect(
            element
        ).select_by_visible_text.side_effect = WebDriverException()

        with pytest.raises(DeliveryError) as excinfo:
            SelectByText("blah").from_(target).perform_as(Tester)

        assert str(target) in str(excinfo.value)

    def test_describe(self) -> None:
        assert (
            SelectByText("bar", None).describe()
            == 'Select the option "bar" from the None.'
        )


class TestSelectByValue:
    def test_can_be_instantiated(self) -> None:
        sbv = SelectByValue(0)

        assert isinstance(sbv, SelectByValue)

    def test_implements_protocol(self) -> None:
        r = SelectByValue(0)

        assert isinstance(r, Performable)
        assert isinstance(r, Describable)

    @mock.patch("screenpy_selenium.actions.select.SeleniumSelect", autospec=True)
    def test_perform_select_by_value(self, mocked_selselect, Tester) -> None:
        value = 1337
        fake_target = Target.the("fake").located_by("//xpath")
        element = mock.create_autospec(WebElement, instance=True)

        SelectByValue(value).from_the(fake_target).perform_as(Tester)

        mocked_selselect(element).select_by_value.assert_called_once_with(str(value))

    def test_perform_complains_for_no_target(self, Tester) -> None:
        with pytest.raises(UnableToAct):
            SelectByValue("value").perform_as(Tester)

    @mock.patch("screenpy_selenium.actions.select.SeleniumSelect", autospec=True)
    def test_exception(self, mocked_selselect, Tester) -> None:
        target, element = get_mocked_target_and_element()
        mocked_selselect(element).select_by_value.side_effect = WebDriverException()

        with pytest.raises(DeliveryError) as excinfo:
            SelectByValue("2").from_(target).perform_as(Tester)

        assert str(target) in str(excinfo.value)

    def test_describe(self) -> None:
        assert (
            SelectByValue("baz", None).describe()
            == 'Select the option with value "baz" from the None.'
        )


class TestSwitchTo:
    def test_can_be_instantiated(self) -> None:
        st1 = SwitchTo.the(TARGET)
        st2 = SwitchTo.default()

        assert isinstance(st1, SwitchTo)
        assert isinstance(st2, SwitchTo)

    def test_implements_protocol(self) -> None:
        r = SwitchTo(None, "")

        assert isinstance(r, Performable)
        assert isinstance(r, Describable)

    def test_perform_switch_to_frame(self, Tester) -> None:
        target, element = get_mocked_target_and_element()
        browser = get_mocked_browser(Tester)

        SwitchTo.the(target).perform_as(Tester)

        browser.switch_to.frame.assert_called_once_with(element)

    def test_perform_switch_to_default(self, Tester) -> None:
        browser = get_mocked_browser(Tester)

        SwitchTo.default().perform_as(Tester)

        browser.switch_to.default_content.assert_called_once()

    def test_describe(self) -> None:
        assert SwitchTo.default().describe() == "Switch to the default frame."


class TestSwitchToTab:
    def test_can_be_instantiated(self) -> None:
        stt = SwitchToTab(1)

        assert isinstance(stt, SwitchToTab)

    def test_implements_protocol(self) -> None:
        r = SwitchToTab(0)

        assert isinstance(r, Performable)
        assert isinstance(r, Describable)

    def test_perform_switch_to_tab(self, Tester) -> None:
        number = 3
        browser = get_mocked_browser(Tester)
        browser.window_handles = range(number + 1)

        SwitchToTab(number).perform_as(Tester)

        browser.switch_to.window.assert_called_once_with(number - 1)

    def test_describe(self) -> None:
        assert SwitchToTab(2).describe() == "Switch to tab #2."


class TestWait:
    def test_can_be_instantiated(self) -> None:
        def foo() -> None:
            pass

        target = mock.create_autospec(Target, instance=True)
        w1 = Wait.for_the(target)
        w2 = Wait(0).seconds_for_the(target)
        w3 = Wait().using(foo)
        w4 = Wait().using(foo).with_(target)

        assert isinstance(w1, Wait)
        assert isinstance(w2, Wait)
        assert isinstance(w3, Wait)
        assert isinstance(w4, Wait)

    def test_implements_protocol(self) -> None:
        r = Wait(1)

        assert isinstance(r, Performable)
        assert isinstance(r, Describable)

    def test_default_log_message(self) -> None:
        target_name = "spam"
        w = Wait.for_the(Target.the(target_name).located_by("//eggs"))

        assert "visibility_of_element_located" in w.log_message
        assert target_name in w.log_message

    def test_custom_log_message(self) -> None:
        args = [1, Target.the("baked").located_by("//beans"), "and spam"]
        w = Wait().using(mock.Mock(), "{0}, {1}, {2}").with_(*args)

        assert all([str(arg) in w.log_message for arg in args])

    def test_set_timeout(self) -> None:
        timeout = 1000

        w = Wait(timeout).seconds_for_the(TARGET)

        assert w.timeout == timeout

    @mock_settings(TIMEOUT=8)
    def test_adjusting_settings_timeout(self) -> None:
        w1 = Wait.for_the(mock.create_autospec(Target, instance=True))
        w2 = Wait()

        assert w1.timeout == 8
        assert w2.timeout == 8

    @mock.patch("screenpy_selenium.actions.wait.EC", autospec=True)
    @mock.patch("screenpy_selenium.actions.wait.WebDriverWait", autospec=True)
    def test_defaults(self, mocked_webdriverwait, mocked_ec, Tester) -> None:
        test_target = Target.the("foo").located_by("//bar")
        mocked_ec.visibility_of_element_located.__name__ = "foo"
        mocked_browser = get_mocked_browser(Tester)

        Wait.for_the(test_target).perform_as(Tester)

        mocked_webdriverwait.assert_called_once_with(mocked_browser, settings.TIMEOUT)
        mocked_ec.visibility_of_element_located.assert_called_once_with(test_target)
        mocked_webdriverwait(
            mocked_browser, settings.TIMEOUT
        ).until.assert_called_once_with(
            mocked_ec.visibility_of_element_located(test_target.locator)
        )

    @mock.patch("screenpy_selenium.actions.wait.WebDriverWait", autospec=True)
    def test_custom(self, mocked_webdriverwait, Tester) -> None:
        browser = get_mocked_browser(Tester)
        test_func = mock.Mock()
        test_func.__name__ = "foo"

        Wait().using(test_func).perform_as(Tester)

        mocked_webdriverwait(browser, settings.TIMEOUT).until.assert_called_once_with(
            test_func()
        )

    @mock.patch("screenpy_selenium.actions.wait.EC", autospec=True)
    @mock.patch("screenpy_selenium.actions.wait.WebDriverWait", autospec=True)
    def test_exception(self, mocked_webdriverwait, mocked_ec, Tester) -> None:
        browser = get_mocked_browser(Tester)
        test_target = Target.the("foo").located_by("//bar")
        mocked_ec.visibility_of_element_located.__name__ = "foo"
        mocked_webdriverwait(
            browser, settings.TIMEOUT
        ).until.side_effect = WebDriverException

        with pytest.raises(DeliveryError) as excinfo:
            Wait.for_the(test_target).perform_as(Tester)

        assert str(test_target) in str(excinfo.value)

    def test_helpful_methods(self) -> None:
        assert Wait(1).to_appear().condition == EC.visibility_of_element_located
        assert Wait(1).to_be_clickable().condition == EC.element_to_be_clickable
        assert Wait(1).to_disappear().condition == EC.invisibility_of_element_located
        assert Wait(1).to_contain_text("").condition == EC.text_to_be_present_in_element

    def test_describe(self) -> None:
        assert (
            Wait(2).describe()
            == "Wait 2 seconds using visibility_of_element_located with []."
        )
        assert (
            Wait(5).seconds_for_the(TARGET).to_contain_text("foo").describe()
            == f'Wait 5 seconds for "foo" to appear in the {TARGET}....'
        )
