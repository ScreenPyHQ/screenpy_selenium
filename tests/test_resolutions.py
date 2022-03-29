from unittest import mock

from screenpy_selenium.resolutions import IsClickable, IsVisible, IsInvisible, IsPresent
from selenium.webdriver.remote.webelement import WebElement

class TestIsClickable:
    def test_can_be_instantiated(self):
        ic = IsClickable()

        assert isinstance(ic, IsClickable)

    def test_matches_a_clickable_element(self):
        element = mock.Mock()
        element.is_enabled.return_value = True
        element.is_displayed.return_value = True
        ic = IsClickable()

        assert ic._matches(element)


    @mock.patch("selenium.webdriver.remote.webelement.WebElement", spec=WebElement)
    @mock.patch("selenium.webdriver.remote.webelement.WebElement", spec=WebElement)
    def test_does_not_match_unclickable_element(self, invisible_element, inactive_element):
        invisible_element.is_displayed.return_value = False
        invisible_element.is_enabled.return_value = True
        inactive_element.is_displayed.return_value = True
        inactive_element.is_enabled.return_value = False
        ic = IsClickable()

        assert not ic._matches(None)  # element was not found by Element()
        assert not ic._matches(invisible_element)
        assert not ic._matches(inactive_element)


class TestIsVisible:
    def test_can_be_instantiated(self):
        iv = IsVisible()

        assert isinstance(iv, IsVisible)

    def test_matches_a_visible_element(self):
        element = mock.Mock()
        element.is_displayed.return_value = True
        iv = IsVisible()

        assert iv._matches(element)

    def test_does_not_match_invisible_element(self):
        invisible_element = mock.Mock()
        invisible_element.is_displayed.return_value = False
        iv = IsVisible()

        assert not iv._matches(None)  # element was not found by Element()
        assert not iv._matches(invisible_element)


class TestIsInVisible:
    def test_can_be_instantiated(self):
        ii = IsInvisible()

        assert isinstance(ii, IsInvisible)

    @mock.patch("selenium.webdriver.remote.webelement.WebElement", spec=WebElement)
    def test_matches_a_visible_element(self, element):
        element.is_displayed.return_value = False
        ii = IsInvisible()

        assert ii._matches(element)

    @mock.patch("selenium.webdriver.remote.webelement.WebElement", spec=WebElement)
    def test_does_not_match_invisible_element(self, visible_element):
        visible_element.is_displayed.return_value = True
        ii = IsInvisible()

        assert not ii._matches(None)  # element was not found by Element()
        assert not ii._matches(visible_element)


class TestIsPresent:
    def test_can_be_instantiated(self):
        ip = IsPresent()

        assert isinstance(ip, IsPresent)

    @mock.patch("selenium.webdriver.remote.webelement.WebElement", spec=WebElement)
    def test_matches_a_present_element(self, mock_element):
        ic = IsPresent()

        mock_element.is_enabled.return_value = False
        mock_element.is_displayed.return_value = False
        assert ic._matches(mock_element)

        mock_element.is_enabled.return_value = True
        mock_element.is_displayed.return_value = True
        assert ic._matches(mock_element)

        mock_element.is_enabled.return_value = True
        mock_element.is_displayed.return_value = False
        assert ic._matches(mock_element)

        mock_element.is_enabled.return_value = False
        mock_element.is_displayed.return_value = True
        assert ic._matches(mock_element)

    def test_does_not_match_missing_element(self):
        ic = IsPresent()
        assert not ic._matches(None)
