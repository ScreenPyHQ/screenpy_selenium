from unittest import mock

import pytest

from screenpy.exceptions import UnableToAnswer
from selenium.common.exceptions import WebDriverException

from screenpy_selenium import Target
from screenpy_selenium.abilities import BrowseTheWeb
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


class TestAttribute:
    def test_can_be_instantiated(self):
        a1 = Attribute("")
        a2 = Attribute("").of_the(None)

        assert isinstance(a1, Attribute)
        assert isinstance(a2, Attribute)

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
        mocked_element = mock.Mock()
        mocked_element.get_attribute.return_value = value
        mocked_browser.find_element.return_value = mocked_element

        assert Attribute(attr).of_the(fake_target).answered_by(Tester) == value
        mocked_browser.find_element.assert_called_once_with(*fake_target)
        mocked_element.get_attribute.assert_called_once_with(attr)


class TestBrowserTitle:
    def test_can_be_instantiated(self):
        b = BrowserTitle()

        assert isinstance(b, BrowserTitle)

    def test_ask_for_browser_title(self, Tester):
        expected_title = "Welcome to the WORLD of TOMORROW!"
        mocked_browser = Tester.ability_to(BrowseTheWeb).browser
        mocked_browser.title = expected_title

        assert BrowserTitle().answered_by(Tester) == expected_title


class TestBrowserURL:
    def test_can_be_instantiated(self):
        b = BrowserURL()

        assert isinstance(b, BrowserURL)

    def test_ask_for_browser_url(self, Tester):
        expected_url = "https://screenpy-docs.readthedocs.io/en/latest/"
        mocked_browser = Tester.ability_to(BrowseTheWeb).browser
        mocked_browser.current_url = expected_url

        assert BrowserURL().answered_by(Tester) == expected_url


class TestCookies:
    def test_can_be_instantiated(self):
        c = Cookies()

        assert isinstance(c, Cookies)

    def test_ask_for_cookies(self, Tester):
        test_name = "cookie_type"
        test_value = "madeleine"
        expected_cookie = {test_name: test_value}
        mocked_browser = Tester.ability_to(BrowseTheWeb).browser
        mocked_browser.get_cookies.return_value = [
            {"name": test_name, "value": test_value}
        ]

        assert Cookies().answered_by(Tester) == expected_cookie


class TestElement:
    def test_can_be_instantiated(self):
        e = Element(None)

        assert isinstance(e, Element)

    def test_question_returns_none_if_no_element_found(self, Tester):
        test_target = Target.the("foo").located_by("//bar")
        mocked_browser = Tester.ability_to(BrowseTheWeb).browser
        mocked_browser.find_element.side_effect = WebDriverException

        assert Element(test_target).answered_by(Tester) is None

    def test_ask_for_element(self, Tester):
        fake_target = Target.the("fake").located_by("//html")
        mocked_browser = Tester.ability_to(BrowseTheWeb).browser
        mocked_element = mock.Mock()
        mocked_browser.find_element.return_value = mocked_element

        assert Element(fake_target).answered_by(Tester) is mocked_element
        mocked_browser.find_element.assert_called_once_with(*fake_target)


class TestList:
    def test_can_be_instantiated(self):
        l1 = List.of(None)
        l2 = List.of_all(None)

        assert isinstance(l1, List)
        assert isinstance(l2, List)

    def test_ask_for_list(self, Tester):
        fake_target = Target.the("fake").located_by("//xpath")
        return_value = ["a", "b", "c"]
        mocked_browser = Tester.ability_to(BrowseTheWeb).browser
        mocked_browser.find_elements.return_value = return_value

        assert List.of(fake_target).answered_by(Tester) == return_value
        mocked_browser.find_elements.assert_called_once_with(*fake_target)


class TestNumber:
    def test_can_be_instantiated(self):
        n1 = Number.of(None)

        assert isinstance(n1, Number)

    def test_ask_for_number(self, Tester):
        fake_target = Target.the("fake").located_by("//xpath")
        return_value = [1, 2, 3]
        mocked_browser = Tester.ability_to(BrowseTheWeb).browser
        mocked_browser.find_elements.return_value = return_value

        assert Number.of(fake_target).answered_by(Tester) == len(return_value)
        mocked_browser.find_elements.assert_called_once_with(*fake_target)


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

    def test_options_from_sets_multi(self):
        assert Selected.options_from(None).multi

    @mock.patch("screenpy_selenium.questions.selected.SeleniumSelect")
    def test_ask_for_selected_option(self, mocked_selenium_select, Tester):
        fake_target = Target.the("fake").located_by("//xpath")
        return_value = "test"
        mocked_selenium_select.return_value.first_selected_option.text = return_value
        mocked_browser = Tester.ability_to(BrowseTheWeb).browser

        assert Selected.option_from(fake_target).answered_by(Tester) == return_value
        mocked_browser.find_element.assert_called_once_with(*fake_target)

    @mock.patch("screenpy_selenium.questions.selected.SeleniumSelect")
    def test_ask_for_selected_options_plural(self, mocked_selenium_select, Tester):
        fake_target = Target.the("fake").located_by("//xpath")
        expected_value = ["test", "the", "options"]
        return_value = [mock.Mock(text=text) for text in expected_value]
        mocked_selenium_select.return_value.all_selected_options = return_value
        mocked_browser = Tester.ability_to(BrowseTheWeb).browser

        assert Selected.options_from(fake_target).answered_by(Tester) == expected_value
        mocked_browser.find_element.assert_called_once_with(*fake_target)


class TestText:
    def test_can_be_instantiated(self):
        t1 = Text.of(None)
        t2 = Text.of_all(None)

        assert isinstance(t1, Text)
        assert isinstance(t2, Text)

    def test_of_all_sets_multi(self):
        assert Text.of_all(None).multi

    def test_ask_for_text(self, Tester):
        fake_target = Target.the("fake").located_by("//xpath")
        mocked_browser = Tester.ability_to(BrowseTheWeb).browser
        expected_text = "spam and eggs"
        mocked_element = mock.Mock(text=expected_text)
        mocked_browser.find_element.return_value = mocked_element

        assert Text.of_the(fake_target).answered_by(Tester) == expected_text
        mocked_browser.find_element.assert_called_once_with(*fake_target)

    def test_ask_for_all_text(self, Tester):
        fake_target = Target.the("fakes").located_by("//xpath")
        mocked_browser = Tester.ability_to(BrowseTheWeb).browser
        expected_texts = ["spam", "eggs", "baked beans"]
        mocked_elements = [mock.Mock(text=text) for text in expected_texts]
        mocked_browser.find_elements.return_value = mocked_elements

        assert Text.of_all(fake_target).answered_by(Tester) == expected_texts
        mocked_browser.find_elements.assert_called_once_with(*fake_target)


class TestTextOfTheAlert:
    def test_can_be_instantiated(self):
        tota1 = TextOfTheAlert()

        assert isinstance(tota1, TextOfTheAlert)

    def test_ask_for_text_of_the_alert(self, Tester):
        expected_text = "It's got what plants crave."
        mocked_browser = Tester.ability_to(BrowseTheWeb).browser
        mocked_browser.switch_to.alert = mock.Mock(text=expected_text)

        assert TextOfTheAlert().answered_by(Tester) == expected_text
