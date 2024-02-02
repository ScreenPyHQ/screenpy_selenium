from typing import Optional
from unittest import mock

import pytest
from screenpy import Answerable, Describable, ErrorKeeper, UnableToAnswer, Actor
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.alert import Alert as SeleniumAlert
from selenium.webdriver.remote.webelement import WebElement

from screenpy_selenium import (
    Attribute,
    BrowserTitle,
    BrowserURL,
    Cookies,
    Element,
    List,
    Number,
    Selected,
    Target,
    TargetingError,
    Text,
    TextOfTheAlert,
)
from useful_mocks import get_mock_target_class, get_mocked_browser, get_mocked_element

FakeTarget = get_mock_target_class()
TARGET = FakeTarget()


class TestAttribute:
    def test_can_be_instantiated(self) -> None:
        a1 = Attribute("")
        a2 = Attribute("").of_the(TARGET)

        assert isinstance(a1, Attribute)
        assert isinstance(a2, Attribute)

    def test_implements_protocol(self) -> None:
        a = Attribute("")

        assert isinstance(a, Answerable)
        assert isinstance(a, Describable)

    def test_raises_error_if_no_target(self, Tester: Actor) -> None:
        with pytest.raises(UnableToAnswer):
            Attribute("").answered_by(Tester)

    def test_of_all_sets_multi(self) -> None:
        assert Attribute("").of_all(TARGET).multi

    def test_ask_for_attribute(self, Tester: Actor) -> None:
        fake_target = Target.the("fake").located_by("//html")
        attr = "foo"
        value = "bar"
        mocked_browser = get_mocked_browser(Tester)
        element = get_mocked_element()
        element.get_attribute.return_value = value
        mocked_browser.find_element.return_value = element

        assert Attribute(attr).of_the(fake_target).answered_by(Tester) == value
        mocked_browser.find_element.assert_called_once_with(*fake_target)
        element.get_attribute.assert_called_once_with(attr)

    def test_ask_for_attribute_multi(self, Tester: Actor) -> None:
        fake_target = Target.the("fake").located_by("//html")
        attr = "foo"
        value = "bar"
        mocked_browser = get_mocked_browser(Tester)
        element = get_mocked_element()
        element.get_attribute.return_value = value
        mocked_browser.find_elements.return_value = [element]

        assert Attribute(attr).of_all(fake_target).answered_by(Tester) == [value]
        mocked_browser.find_elements.assert_called_once_with(*fake_target)
        element.get_attribute.assert_called_once_with(attr)

    def test_describe(self) -> None:
        assert Attribute("foo").describe() == 'The "foo" attribute of the None.'


class TestBrowserTitle:
    def test_can_be_instantiated(self) -> None:
        b = BrowserTitle()

        assert isinstance(b, BrowserTitle)

    def test_implements_protocol(self) -> None:
        b = BrowserTitle()

        assert isinstance(b, Answerable)
        assert isinstance(b, Describable)

    def test_ask_for_browser_title(self, Tester: Actor) -> None:
        expected_title = "Welcome to the WORLD of TOMORROW!"
        mocked_browser = get_mocked_browser(Tester)
        mocked_browser.title = expected_title

        assert BrowserTitle().answered_by(Tester) == expected_title

    def test_describe(self) -> None:
        assert BrowserTitle().describe() == "The current page's title."


class TestBrowserURL:
    def test_can_be_instantiated(self) -> None:
        b = BrowserURL()

        assert isinstance(b, BrowserURL)

    def test_implements_protocol(self) -> None:
        b = BrowserURL()

        assert isinstance(b, Answerable)
        assert isinstance(b, Describable)

    def test_ask_for_browser_url(self, Tester: Actor) -> None:
        expected_url = "https://screenpy-docs.readthedocs.io/en/latest/"
        mocked_browser = get_mocked_browser(Tester)
        mocked_browser.current_url = expected_url

        assert BrowserURL().answered_by(Tester) == expected_url

    def test_describe(self) -> None:
        assert BrowserURL().describe() == "The browser URL."


class TestCookies:
    def test_can_be_instantiated(self) -> None:
        c = Cookies()

        assert isinstance(c, Cookies)

    def test_implements_protocol(self) -> None:
        c = Cookies()

        assert isinstance(c, Answerable)
        assert isinstance(c, Describable)

    def test_ask_for_cookies(self, Tester: Actor) -> None:
        test_name = "cookie_type"
        test_value = "madeleine"
        expected_cookie = {test_name: test_value}
        mocked_browser = get_mocked_browser(Tester)
        mocked_browser.get_cookies.return_value = [
            {"name": test_name, "value": test_value}
        ]

        assert Cookies().answered_by(Tester) == expected_cookie

    def test_describe(self) -> None:
        assert Cookies().describe() == "The browser's cookies."


class TestElement:
    def test_can_be_instantiated(self) -> None:
        e = Element(TARGET)

        assert isinstance(e, Element)

    def test_implements_protocol(self) -> None:
        e = Element(TARGET)

        assert isinstance(e, Answerable)
        assert isinstance(e, ErrorKeeper)
        assert isinstance(e, Describable)

    def test_caught_exception_annotation(self) -> None:
        e = Element(TARGET)

        annotation = e.__annotations__["caught_exception"]
        assert annotation == Optional[TargetingError]

    def test_question_returns_none_if_no_element_found(self, Tester: Actor) -> None:
        test_target = Target.the("foo").located_by("//bar")
        mocked_browser = get_mocked_browser(Tester)
        mocked_browser.find_element.side_effect = WebDriverException()

        assert Element(test_target).answered_by(Tester) is None

    def test_question_captures_exception(self, Tester: Actor) -> None:
        test_target = Target.the("foo").located_by("//bar")
        mocked_browser = get_mocked_browser(Tester)
        mocked_browser.find_element.side_effect = WebDriverException("Specific Msg")

        elem = Element(test_target)
        elem.answered_by(Tester)

        assert isinstance(elem.caught_exception, TargetingError)
        assert (
            elem.caught_exception.args[0]
            == "Message: Specific Msg\n raised while trying to find foo."
        )

    def test_ask_for_element(self, Tester: Actor) -> None:
        fake_target = Target.the("fake").located_by("//html")
        mocked_browser = get_mocked_browser(Tester)
        element = get_mocked_element()
        mocked_browser.find_element.return_value = element

        assert Element(fake_target).answered_by(Tester) is element
        mocked_browser.find_element.assert_called_once_with(*fake_target)

    def test_describe(self) -> None:
        assert Element(TARGET).describe() == f"The {TARGET}."


class TestList:
    def test_can_be_instantiated(self) -> None:
        l1 = List.of(TARGET)
        l2 = List.of_all(TARGET)

        assert isinstance(l1, List)
        assert isinstance(l2, List)

    def test_implements_protocol(self) -> None:
        e = List(TARGET)

        assert isinstance(e, Answerable)
        assert isinstance(e, Describable)

    def test_ask_for_list(self, Tester: Actor) -> None:
        fake_target = Target.the("fake").located_by("//xpath")
        return_value = ["a", "b", "c"]
        mocked_browser = get_mocked_browser(Tester)
        mocked_browser.find_elements.return_value = return_value

        assert List.of(fake_target).answered_by(Tester) == return_value
        mocked_browser.find_elements.assert_called_once_with(*fake_target)

    def test_describe(self) -> None:
        assert List(TARGET).describe() == f"The list of {TARGET}."


class TestNumber:
    def test_can_be_instantiated(self) -> None:
        n1 = Number.of(TARGET)

        assert isinstance(n1, Number)

    def test_implements_protocol(self) -> None:
        n = Number(TARGET)

        assert isinstance(n, Answerable)
        assert isinstance(n, Describable)

    def test_ask_for_number(self, Tester: Actor) -> None:
        fake_target = Target.the("fake").located_by("//xpath")
        return_value = [1, 2, 3]
        mocked_browser = get_mocked_browser(Tester)
        mocked_browser.find_elements.return_value = return_value

        assert Number.of(fake_target).answered_by(Tester) == len(return_value)
        mocked_browser.find_elements.assert_called_once_with(*fake_target)

    def test_describe(self) -> None:
        assert Number(TARGET).describe() == f"The number of {TARGET}."


class TestSelected:
    def test_can_be_instantiated(self) -> None:
        s1 = Selected.option_from(TARGET)
        s2 = Selected.option_from_the(TARGET)
        s3 = Selected.options_from(TARGET)
        s4 = Selected.options_from_the(TARGET)

        assert isinstance(s1, Selected)
        assert isinstance(s2, Selected)
        assert isinstance(s3, Selected)
        assert isinstance(s4, Selected)

    def test_implements_protocol(self) -> None:
        s = Selected(TARGET)

        assert isinstance(s, Answerable)
        assert isinstance(s, Describable)

    def test_options_from_sets_multi(self) -> None:
        assert Selected.options_from(TARGET).multi

    @mock.patch("screenpy_selenium.questions.selected.SeleniumSelect", autospec=True)
    def test_ask_for_selected_option(
        self, mocked_selenium_select: mock.Mock, Tester: Actor
    ) -> None:
        fake_target = Target.the("fake").located_by("//xpath")
        return_value = "test"
        mocked_selenium_select.return_value.first_selected_option.text = return_value
        mocked_browser = get_mocked_browser(Tester)

        assert Selected.option_from(fake_target).answered_by(Tester) == return_value
        mocked_browser.find_element.assert_called_once_with(*fake_target)

    @mock.patch("screenpy_selenium.questions.selected.SeleniumSelect", autospec=True)
    def test_ask_for_selected_options_plural(
        self, mocked_selenium_select: mock.Mock, Tester: Actor
    ) -> None:
        fake_target = Target.the("fake").located_by("//xpath")
        expected_value = ["test", "the", "options"]
        return_value = [mock.Mock(text=text) for text in expected_value]
        mocked_selenium_select.return_value.all_selected_options = return_value
        mocked_browser = get_mocked_browser(Tester)

        assert Selected.options_from(fake_target).answered_by(Tester) == expected_value
        mocked_browser.find_element.assert_called_once_with(*fake_target)

    def test_describe(self) -> None:
        assert (
            Selected(TARGET).describe() == f"The selected option(s) from the {TARGET}."
        )


class TestText:
    def test_can_be_instantiated(self) -> None:
        t1 = Text.of(TARGET)
        t2 = Text.of_all(TARGET)

        assert isinstance(t1, Text)
        assert isinstance(t2, Text)

    def test_implements_protocol(self) -> None:
        t = Text(TARGET)

        assert isinstance(t, Answerable)
        assert isinstance(t, Describable)

    def test_of_all_sets_multi(self) -> None:
        assert Text.of_all(TARGET).multi

    def test_ask_for_text(self, Tester: Actor) -> None:
        fake_target = Target.the("fake").located_by("//xpath")
        mocked_browser = get_mocked_browser(Tester)
        expected_text = "spam and eggs"
        mocked_element = mock.create_autospec(
            WebElement, text=expected_text, instance=True
        )
        mocked_browser.find_element.return_value = mocked_element

        assert Text.of_the(fake_target).answered_by(Tester) == expected_text
        mocked_browser.find_element.assert_called_once_with(*fake_target)

    def test_ask_for_all_text(self, Tester: Actor) -> None:
        fake_target = Target.the("fakes").located_by("//xpath")
        mocked_browser = get_mocked_browser(Tester)
        expected_texts = ["spam", "eggs", "baked beans"]
        mocked_elements = [
            mock.create_autospec(WebElement, text=text, instance=True)
            for text in expected_texts
        ]
        mocked_browser.find_elements.return_value = mocked_elements

        assert Text.of_all(fake_target).answered_by(Tester) == expected_texts
        mocked_browser.find_elements.assert_called_once_with(*fake_target)

    def test_describe(self) -> None:
        assert Text(TARGET).describe() == f"The text from the {TARGET}."


class TestTextOfTheAlert:
    def test_can_be_instantiated(self) -> None:
        tota1 = TextOfTheAlert()

        assert isinstance(tota1, TextOfTheAlert)

    def test_implements_protocol(self) -> None:
        t = TextOfTheAlert()

        assert isinstance(t, Answerable)
        assert isinstance(t, Describable)

    def test_ask_for_text_of_the_alert(self, Tester: Actor) -> None:
        expected_text = "It's got what plants crave."
        mocked_browser = get_mocked_browser(Tester)
        mocked_browser.switch_to.alert = mock.create_autospec(
            SeleniumAlert, text=expected_text, instance=True
        )

        assert TextOfTheAlert().answered_by(Tester) == expected_text

    def test_describe(self) -> None:
        assert TextOfTheAlert().describe() == "The text of the alert."
