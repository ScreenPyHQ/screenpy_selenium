from typing import Optional
from unittest import mock

import pytest
from screenpy.exceptions import UnableToAnswer
from screenpy.protocols import Answerable, ErrorKeeper, Describable

from screenpy_selenium import Target
from screenpy_selenium.abilities import BrowseTheWeb
from screenpy_selenium.exceptions import TargetingError
from screenpy_selenium.questions import (
    Attribute,
    BrowserTitle,
    BrowserURL,
    Cookies,
    Element,
    List,
    Number,
    Selected,
    Text,
    TextOfTheAlert,
)
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.alert import Alert as SeleniumAlert
from selenium.webdriver.remote.webelement import WebElement


class TestAttribute:
    def test_can_be_instantiated(self):
        a1 = Attribute("")
        a2 = Attribute("").of_the(None)

        assert isinstance(a1, Attribute)
        assert isinstance(a2, Attribute)

    def test_implements_protocol(self):
        a = Attribute("")
        assert isinstance(a, Answerable)
        assert isinstance(a, Describable)

    def test_raises_error_if_no_target(self, Tester):
        with pytest.raises(UnableToAnswer):
            Attribute("").answered_by(Tester)

    def test_of_all_sets_multi(self):
        assert Attribute("").of_all(None).multi

    def test_uses_get_attribute(self, Tester):
        fake_target = Target.the("fake").located_by("//html")
        attr = "foo"
        value = "bar"
        mocked_browser = Tester.ability_to(BrowseTheWeb).browser
        mocked_element = mock.create_autospec(WebElement, instance=True)
        mocked_element.get_attribute.return_value = value
        mocked_browser.find_element.return_value = mocked_element

        assert Attribute(attr).of_the(fake_target).answered_by(Tester) == value
        mocked_browser.find_element.assert_called_once_with(*fake_target)
        mocked_element.get_attribute.assert_called_once_with(attr)

    def test_describe(self):
        assert Attribute("foo").describe() == f'The "foo" attribute of the None.'

class TestBrowserTitle:
    def test_can_be_instantiated(self):
        b = BrowserTitle()

        assert isinstance(b, BrowserTitle)

    def test_implements_protocol(self):
        b = BrowserTitle()
        assert isinstance(b, Answerable)
        assert isinstance(b, Describable)

    def test_ask_for_browser_title(self, Tester):
        expected_title = "Welcome to the WORLD of TOMORROW!"
        mocked_browser = Tester.ability_to(BrowseTheWeb).browser
        mocked_browser.title = expected_title

        assert BrowserTitle().answered_by(Tester) == expected_title

    def test_describe(self):
        assert BrowserTitle().describe() == f"The current page's title."

class TestBrowserURL:
    def test_can_be_instantiated(self):
        b = BrowserURL()

        assert isinstance(b, BrowserURL)

    def test_implements_protocol(self):
        b = BrowserURL()
        assert isinstance(b, Answerable)
        assert isinstance(b, Describable)

    def test_ask_for_browser_url(self, Tester):
        expected_url = "https://screenpy-docs.readthedocs.io/en/latest/"
        mocked_browser = Tester.ability_to(BrowseTheWeb).browser
        mocked_browser.current_url = expected_url

        assert BrowserURL().answered_by(Tester) == expected_url

    def test_describe(self):
        assert BrowserURL().describe() == f"The browser URL."

class TestCookies:
    def test_can_be_instantiated(self):
        c = Cookies()

        assert isinstance(c, Cookies)

    def test_implements_protocol(self):
        c = Cookies()
        assert isinstance(c, Answerable)
        assert isinstance(c, Describable)

    def test_ask_for_cookies(self, Tester):
        test_name = "cookie_type"
        test_value = "madeleine"
        expected_cookie = {test_name: test_value}
        mocked_browser = Tester.ability_to(BrowseTheWeb).browser
        mocked_browser.get_cookies.return_value = [
            {"name": test_name, "value": test_value}
        ]

        assert Cookies().answered_by(Tester) == expected_cookie

    def test_describe(self):
        assert Cookies().describe() == f"The browser's cookies."

class TestElement:
    def test_can_be_instantiated(self):
        e = Element(None)

        assert isinstance(e, Element)

    def test_implements_protocol(self):
        e = Element(None)
        assert isinstance(e, Answerable)
        assert isinstance(e, ErrorKeeper)
        assert isinstance(e, Describable)

    def test_caught_exception_annotation(self):
        e = Element(None)
        stuff = e.__annotations__['caught_exception']
        assert stuff == Optional[TargetingError]

    def test_question_returns_none_if_no_element_found(self, Tester):
        test_target = Target.the("foo").located_by("//bar")
        mocked_browser = Tester.ability_to(BrowseTheWeb).browser
        mocked_browser.find_element.side_effect = WebDriverException()

        assert Element(test_target).answered_by(Tester) is None

    def test_question_captures_exception(self, Tester):
        test_target = Target.the("foo").located_by("//bar")
        mocked_browser = Tester.ability_to(BrowseTheWeb).browser
        mocked_browser.find_element.side_effect = WebDriverException('Specific Msg')

        elem = Element(test_target)
        elem.answered_by(Tester)

        assert isinstance(elem.caught_exception, TargetingError)
        assert elem.caught_exception.args[0] == "Message: Specific Msg\n raised while trying to find foo."

    def test_ask_for_element(self, Tester):
        fake_target = Target.the("fake").located_by("//html")
        mocked_browser = Tester.ability_to(BrowseTheWeb).browser
        mocked_element = mock.create_autospec(WebElement, instance=True)
        mocked_browser.find_element.return_value = mocked_element

        assert Element(fake_target).answered_by(Tester) is mocked_element
        mocked_browser.find_element.assert_called_once_with(*fake_target)

    def test_describe(self):
        assert Element(None).describe() == f"The None."

class TestList:
    def test_can_be_instantiated(self):
        l1 = List.of(None)
        l2 = List.of_all(None)

        assert isinstance(l1, List)
        assert isinstance(l2, List)

    def test_implements_protocol(self):
        e = List(None)
        assert isinstance(e, Answerable)
        assert isinstance(e, Describable)

    def test_ask_for_list(self, Tester):
        fake_target = Target.the("fake").located_by("//xpath")
        return_value = ["a", "b", "c"]
        mocked_browser = Tester.ability_to(BrowseTheWeb).browser
        mocked_browser.find_elements.return_value = return_value

        assert List.of(fake_target).answered_by(Tester) == return_value
        mocked_browser.find_elements.assert_called_once_with(*fake_target)

    def test_describe(self):
        assert List(None).describe() == f"The list of None."

class TestNumber:
    def test_can_be_instantiated(self):
        n1 = Number.of(None)

        assert isinstance(n1, Number)

    def test_implements_protocol(self):
        n = Number(None)
        assert isinstance(n, Answerable)
        assert isinstance(n, Describable)

    def test_ask_for_number(self, Tester):
        fake_target = Target.the("fake").located_by("//xpath")
        return_value = [1, 2, 3]
        mocked_browser = Tester.ability_to(BrowseTheWeb).browser
        mocked_browser.find_elements.return_value = return_value

        assert Number.of(fake_target).answered_by(Tester) == len(return_value)
        mocked_browser.find_elements.assert_called_once_with(*fake_target)

    def test_describe(self):
        assert Number(None).describe() == f"The number of None."

class TestSelected:
    def test_can_be_instantiated(self):
        s1 = Selected.option_from(None)
        s2 = Selected.option_from_the(None)
        s3 = Selected.options_from(None)
        s4 = Selected.options_from_the(None)

        assert isinstance(s1, Selected)
        assert isinstance(s2, Selected)
        assert isinstance(s3, Selected)
        assert isinstance(s4, Selected)

    def test_implements_protocol(self):
        s = Selected(None)
        assert isinstance(s, Answerable)
        assert isinstance(s, Describable)

    def test_options_from_sets_multi(self):
        assert Selected.options_from(None).multi

    @mock.patch("screenpy_selenium.questions.selected.SeleniumSelect", autospec=True)
    def test_ask_for_selected_option(self, mocked_selenium_select, Tester):
        fake_target = Target.the("fake").located_by("//xpath")
        return_value = "test"
        mocked_selenium_select.return_value.first_selected_option.text = return_value
        mocked_browser = Tester.ability_to(BrowseTheWeb).browser

        assert Selected.option_from(fake_target).answered_by(Tester) == return_value
        mocked_browser.find_element.assert_called_once_with(*fake_target)

    @mock.patch("screenpy_selenium.questions.selected.SeleniumSelect", autospec=True)
    def test_ask_for_selected_options_plural(self, mocked_selenium_select, Tester):
        fake_target = Target.the("fake").located_by("//xpath")
        expected_value = ["test", "the", "options"]
        return_value = [mock.Mock(text=text) for text in expected_value]
        mocked_selenium_select.return_value.all_selected_options = return_value
        mocked_browser = Tester.ability_to(BrowseTheWeb).browser

        assert Selected.options_from(fake_target).answered_by(Tester) == expected_value
        mocked_browser.find_element.assert_called_once_with(*fake_target)

    def test_describe(self):
        assert Selected(None).describe() == f"The selected option(s) from the None."

class TestText:
    def test_can_be_instantiated(self):
        t1 = Text.of(None)
        t2 = Text.of_all(None)

        assert isinstance(t1, Text)
        assert isinstance(t2, Text)

    def test_implements_protocol(self):
        t = Text(None)
        assert isinstance(t, Answerable)
        assert isinstance(t, Describable)

    def test_of_all_sets_multi(self):
        assert Text.of_all(None).multi

    def test_ask_for_text(self, Tester):
        fake_target = Target.the("fake").located_by("//xpath")
        mocked_browser = Tester.ability_to(BrowseTheWeb).browser
        expected_text = "spam and eggs"
        mocked_element = mock.create_autospec(WebElement, text=expected_text, instance=True)
        mocked_browser.find_element.return_value = mocked_element

        assert Text.of_the(fake_target).answered_by(Tester) == expected_text
        mocked_browser.find_element.assert_called_once_with(*fake_target)

    def test_ask_for_all_text(self, Tester):
        fake_target = Target.the("fakes").located_by("//xpath")
        mocked_browser = Tester.ability_to(BrowseTheWeb).browser
        expected_texts = ["spam", "eggs", "baked beans"]
        mocked_elements = [mock.create_autospec(WebElement, text=text, instance=True) for text in expected_texts]
        mocked_browser.find_elements.return_value = mocked_elements

        assert Text.of_all(fake_target).answered_by(Tester) == expected_texts
        mocked_browser.find_elements.assert_called_once_with(*fake_target)

    def test_describe(self):
        assert Text(None).describe() == f"The text from the None."

class TestTextOfTheAlert:
    def test_can_be_instantiated(self):
        tota1 = TextOfTheAlert()

        assert isinstance(tota1, TextOfTheAlert)

    def test_implements_protocol(self):
        t = TextOfTheAlert()
        assert isinstance(t, Answerable)
        assert isinstance(t, Describable)

    def test_ask_for_text_of_the_alert(self, Tester):
        expected_text = "It's got what plants crave."
        mocked_browser = Tester.ability_to(BrowseTheWeb).browser
        mocked_browser.switch_to.alert = mock.create_autospec(SeleniumAlert, text=expected_text, instance=True)

        assert TextOfTheAlert().answered_by(Tester) == expected_text

    def test_describe(self):
        assert TextOfTheAlert().describe() == f"The text of the alert."
