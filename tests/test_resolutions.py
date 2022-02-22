from unittest import mock

from screenpy_selenium.resolutions import IsClickable, IsVisible


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

    def test_does_not_match_unclickable_element(self):
        invisible_element = mock.Mock()
        invisible_element.is_displayed.return_value = False
        invisible_element.is_enabled.return_value = True
        inactive_element = mock.Mock()
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
