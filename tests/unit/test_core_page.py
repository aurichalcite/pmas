"""
Comprehensive unit tests for BasePage class.

This module tests the BasePage class with extensive mocking to ensure:
- Page initialization and URL handling
- Element location and interaction methods
- Navigation and page load verification
- Wait mechanisms and timeout handling
- Error scenarios and edge cases
"""

from unittest.mock import Mock, patch

import pytest
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from pmas.core.errors import PageLoadError
from pmas.core.locators import Locator
from pmas.core.page import BasePage


class ConcretePage(BasePage):
    """Concrete test implementation of BasePage."""

    url_path = "test-page"
    expected_titles = ["Test Page", "Test Page - Loading"]

    def verify_page_loaded(self) -> bool:
        """Test implementation of abstract method."""
        return "Test Page" in self.driver.title


class TestBasePageInitialization:
    """Test BasePage initialization and basic properties."""

    def test_init_when_all_parameters_provided_expects_correct_setup(self):
        """Test BasePage initialization with all parameters."""
        mock_driver = Mock()
        base_url = "https://example.com"
        timeout = 15.0

        page = ConcretePage(mock_driver, base_url, timeout)

        assert page.driver == mock_driver
        assert page.base_url == "https://example.com"
        assert page.timeout == 15.0
        assert page._elements_cache == {}

    def test_init_when_base_url_has_trailing_slash_expects_stripped(self):
        """Test that trailing slash is removed from base_url."""
        mock_driver = Mock()

        page = ConcretePage(mock_driver, "https://example.com/", 10.0)

        assert page.base_url == "https://example.com"

    def test_init_when_minimal_parameters_expects_defaults(self):
        """Test BasePage initialization with minimal parameters."""
        mock_driver = Mock()

        page = ConcretePage(mock_driver)

        assert page.driver == mock_driver
        assert page.base_url == ""
        assert page.timeout == 10.0

    def test_url_property_when_url_path_set_expects_combined_url(self):
        """Test URL property combines base_url and url_path."""
        mock_driver = Mock()
        page = ConcretePage(mock_driver, "https://example.com", 10.0)

        assert page.url == "https://example.com/test-page"

    def test_url_property_when_no_url_path_expects_base_url(self):
        """Test URL property returns base_url when no url_path."""
        mock_driver = Mock()

        class NoPathPage(BasePage):
            url_path = ""

            def verify_page_loaded(self) -> bool:
                return True

        page = NoPathPage(mock_driver, "https://example.com", 10.0)
        assert page.url == "https://example.com"

    def test_current_url_property_expects_driver_current_url(self):
        """Test current_url property delegates to driver."""
        mock_driver = Mock()
        mock_driver.current_url = "https://example.com/current"

        page = ConcretePage(mock_driver, "https://example.com", 10.0)

        assert page.current_url == "https://example.com/current"

    def test_title_property_expects_driver_title(self):
        """Test title property delegates to driver."""
        mock_driver = Mock()
        mock_driver.title = "Test Page Title"

        page = ConcretePage(mock_driver, "https://example.com", 10.0)

        assert page.title == "Test Page Title"


class TestBasePageNavigation:
    """Test navigation methods."""

    def test_navigate_to_when_called_expects_driver_get(self):
        """Test navigate_to calls driver.get with page URL."""
        mock_driver = Mock()
        page = ConcretePage(mock_driver, "https://example.com", 10.0)

        page.navigate_to()

        mock_driver.get.assert_called_once_with("https://example.com/test-page")

    @patch("pmas.core.page.WebDriverWait")
    def test_wait_for_page_load_when_title_matches_expects_success(self, mock_wait):
        """Test wait_for_page_load succeeds when title matches."""
        mock_driver = Mock()
        mock_driver.title = "Test Page"
        mock_wait_instance = Mock()
        mock_wait.return_value = mock_wait_instance
        mock_wait_instance.until.return_value = True

        page = ConcretePage(mock_driver, "https://example.com", 10.0)

        result = page.wait_for_page_load()

        assert result == page  # wait_for_page_load returns self, not True
        # WebDriverWait is called twice: once for title check, once for document ready
        assert mock_wait.call_count == 2

    @patch("pmas.core.page.WebDriverWait")
    def test_wait_for_page_load_when_timeout_expects_page_load_error(self, mock_wait):
        """Test wait_for_page_load raises PageLoadError on timeout."""
        mock_driver = Mock()
        mock_driver.title = "Wrong Title"
        mock_driver.current_url = "https://example.com/test-page"
        mock_wait_instance = Mock()
        mock_wait.return_value = mock_wait_instance
        mock_wait_instance.until.side_effect = TimeoutException("Timeout")

        page = ConcretePage(mock_driver, "https://example.com", 10.0)

        with pytest.raises(PageLoadError) as exc_info:
            page.wait_for_page_load()

        assert "Test Page" in str(exc_info.value)
        assert "Wrong Title" in str(exc_info.value)

    @patch("pmas.core.page.WebDriverWait")
    def test_refresh_when_called_expects_driver_refresh(self, mock_wait):
        """Test refresh calls driver.refresh."""
        mock_driver = Mock()
        mock_driver.title = "Test Page"
        mock_wait_instance = Mock()
        mock_wait.return_value = mock_wait_instance
        mock_wait_instance.until.return_value = True

        page = ConcretePage(mock_driver, "https://example.com", 10.0)

        result = page.refresh()

        mock_driver.refresh.assert_called_once()
        assert result == page


class TestBasePageElementLocation:
    """Test element location and interaction methods."""

    def test_is_element_present_when_element_found_expects_true(self):
        """Test is_element_present returns True when element exists."""
        mock_driver = Mock()
        mock_locator = Mock(spec=Locator)
        mock_locator.selenium_locator = ("id", "test-element")
        mock_driver.find_element.return_value = Mock()

        page = ConcretePage(mock_driver, "https://example.com", 10.0)

        result = page.is_element_present(mock_locator)

        assert result is True
        mock_driver.find_element.assert_called_once_with("id", "test-element")

    def test_is_element_present_when_element_not_found_expects_false(self):
        """Test is_element_present returns False when element not found."""
        mock_driver = Mock()
        mock_locator = Mock(spec=Locator)
        mock_locator.selenium_locator = ("id", "missing-element")
        mock_driver.find_element.side_effect = NoSuchElementException("Not found")

        page = ConcretePage(mock_driver, "https://example.com", 10.0)

        result = page.is_element_present(mock_locator)

        assert result is False

    @patch("pmas.core.page.BaseElement")
    def test_is_element_visible_when_element_displayed_expects_true(
        self, mock_element_class
    ):
        """Test is_element_visible returns True when element is displayed."""
        mock_driver = Mock()
        mock_locator = Mock(spec=Locator)
        mock_element = Mock()
        mock_element.is_displayed = True
        mock_element_class.return_value = mock_element

        page = ConcretePage(mock_driver, "https://example.com", 10.0)

        result = page.is_element_visible(mock_locator)

        assert result is True
        mock_element_class.assert_called_once_with(mock_driver, mock_locator, 1.0)

    @patch("pmas.core.page.BaseElement")
    def test_is_element_visible_when_element_not_displayed_expects_false(
        self, mock_element_class
    ):
        """Test is_element_visible returns False when element not displayed."""
        mock_driver = Mock()
        mock_locator = Mock(spec=Locator)
        mock_element_class.side_effect = Exception("Element not found")

        page = ConcretePage(mock_driver, "https://example.com", 10.0)

        result = page.is_element_visible(mock_locator)

        assert result is False


class TestBasePageElementGetters:
    """Test element getter methods."""

    @patch("pmas.core.page.Button")
    def test_get_button_when_called_expects_button_instance(self, mock_button_class):
        """Test get_button returns Button instance."""
        mock_driver = Mock()
        mock_locator = Mock(spec=Locator)
        mock_button = Mock()
        mock_button_class.return_value = mock_button

        page = ConcretePage(mock_driver, "https://example.com", 10.0)

        result = page.get_button(mock_locator)

        assert result == mock_button
        mock_button_class.assert_called_once_with(mock_driver, mock_locator, 10.0)

    @patch("pmas.core.page.TextInput")
    def test_get_text_input_when_called_expects_text_input_instance(
        self, mock_text_input_class
    ):
        """Test get_text_input returns TextInput instance."""
        mock_driver = Mock()
        mock_locator = Mock(spec=Locator)
        mock_text_input = Mock()
        mock_text_input_class.return_value = mock_text_input

        page = ConcretePage(mock_driver, "https://example.com", 10.0)

        result = page.get_text_input(mock_locator)

        assert result == mock_text_input
        mock_text_input_class.assert_called_once_with(mock_driver, mock_locator, 10.0)

    @patch("pmas.core.page.Dropdown")
    def test_get_dropdown_when_called_expects_dropdown_instance(
        self, mock_dropdown_class
    ):
        """Test get_dropdown returns Dropdown instance."""
        mock_driver = Mock()
        mock_locator = Mock(spec=Locator)
        mock_dropdown = Mock()
        mock_dropdown_class.return_value = mock_dropdown

        page = ConcretePage(mock_driver, "https://example.com", 10.0)

        result = page.get_dropdown(mock_locator)

        assert result == mock_dropdown
        mock_dropdown_class.assert_called_once_with(mock_driver, mock_locator, 10.0)

    @patch("pmas.core.page.Checkbox")
    def test_get_checkbox_when_called_expects_checkbox_instance(
        self, mock_checkbox_class
    ):
        """Test get_checkbox returns Checkbox instance."""
        mock_driver = Mock()
        mock_locator = Mock(spec=Locator)
        mock_checkbox = Mock()
        mock_checkbox_class.return_value = mock_checkbox

        page = ConcretePage(mock_driver, "https://example.com", 10.0)

        result = page.get_checkbox(mock_locator)

        assert result == mock_checkbox
        mock_checkbox_class.assert_called_once_with(mock_driver, mock_locator, 10.0)

    @patch("pmas.core.page.RadioButton")
    def test_get_radio_button_when_called_expects_radio_button_instance(
        self, mock_radio_class
    ):
        """Test get_radio_button returns RadioButton instance."""
        mock_driver = Mock()
        mock_locator = Mock(spec=Locator)
        mock_radio = Mock()
        mock_radio_class.return_value = mock_radio

        page = ConcretePage(mock_driver, "https://example.com", 10.0)

        result = page.get_radio_button(mock_locator)

        assert result == mock_radio
        mock_radio_class.assert_called_once_with(mock_driver, mock_locator, 10.0)


class TestBasePageUtilityMethods:
    """Test utility methods."""

    def test_str_representation_expects_class_name_and_details(self):
        """Test string representation includes class name, URL, and title."""
        mock_driver = Mock()
        mock_driver.title = "Test Page Title"

        page = ConcretePage(mock_driver, "https://example.com", 10.0)

        result = str(page)

        assert "ConcretePage" in result
        assert "https://example.com/test-page" in result
        assert "Test Page Title" in result


class TestBasePageAbstractMethods:
    """Test abstract method requirements."""

    def test_verify_page_loaded_when_implemented_expects_callable(self):
        """Test that verify_page_loaded is properly implemented."""
        mock_driver = Mock()
        mock_driver.title = "Test Page"

        page = ConcretePage(mock_driver, "https://example.com", 10.0)

        result = page.verify_page_loaded()

        assert isinstance(result, bool)
        assert result is True

    def test_base_page_when_not_implementing_abstract_method_expects_error(self):
        """Test that BasePage cannot be instantiated without implementing abstract methods."""
        mock_driver = Mock()

        with pytest.raises(TypeError):
            BasePage(mock_driver, "https://example.com", 10.0)


class TestBasePageBranchCoverage:
    """Test specific conditional branches to improve branch coverage."""

    def test_url_property_when_url_path_empty_expects_base_url_only(self):
        """Test url property returns base_url when url_path is empty."""
        mock_driver = Mock()

        # Create a page with empty url_path
        class EmptyPathPage(BasePage):
            url_path = ""  # Empty path

            def verify_page_loaded(self) -> bool:
                return True

        page = EmptyPathPage(mock_driver, "https://example.com", 10.0)

        result = page.url

        assert result == "https://example.com"

    def test_url_property_when_url_path_has_leading_slash_expects_stripped(self):
        """Test url property strips leading slash from url_path."""
        mock_driver = Mock()

        class LeadingSlashPage(BasePage):
            url_path = "/test-page"  # Leading slash

            def verify_page_loaded(self) -> bool:
                return True

        page = LeadingSlashPage(mock_driver, "https://example.com", 10.0)

        result = page.url

        assert result == "https://example.com/test-page"

    def test_wait_for_page_load_when_no_expected_titles_expects_document_ready_only(
        self,
    ):
        """Test wait_for_page_load skips title check when no expected_titles."""
        mock_driver = Mock()
        mock_driver.execute_script.return_value = "complete"

        class NoTitlesPage(BasePage):
            url_path = "test"
            expected_titles = []  # No expected titles

            def verify_page_loaded(self) -> bool:
                return True

        page = NoTitlesPage(mock_driver, "https://example.com", 10.0)

        with patch("pmas.core.page.WebDriverWait") as mock_wait:
            mock_wait_instance = Mock()
            mock_wait.return_value = mock_wait_instance

            result = page.wait_for_page_load()

            # Should only create one WebDriverWait for document ready, not for title
            assert mock_wait.call_count == 1
            assert result == page

    def test_wait_for_page_load_when_timeout_provided_expects_custom_timeout(self):
        """Test wait_for_page_load uses provided timeout instead of default."""
        mock_driver = Mock()
        mock_driver.title = "Expected Title"
        mock_driver.execute_script.return_value = "complete"

        page = ConcretePage(mock_driver, "https://example.com", 10.0)

        with patch("pmas.core.page.WebDriverWait") as mock_wait:
            mock_wait_instance = Mock()
            mock_wait.return_value = mock_wait_instance

            result = page.wait_for_page_load(timeout=5.0)

            # Should use provided timeout (5.0), not default (10.0)
            # Called twice: once for title check, once for document ready
            assert mock_wait.call_count == 2
            mock_wait.assert_any_call(mock_driver, 5.0)
            assert result == page

    def test_wait_for_page_load_when_document_ready_timeout_expects_warning_logged(
        self,
    ):
        """Test wait_for_page_load logs warning when document ready times out."""
        from selenium.common.exceptions import TimeoutException

        mock_driver = Mock()
        mock_driver.title = "Expected Title"

        page = ConcretePage(mock_driver, "https://example.com", 10.0)

        with (
            patch("pmas.core.page.WebDriverWait") as mock_wait,
            patch("pmas.core.page.logger") as mock_logger,
        ):
            mock_wait_instance = Mock()
            mock_wait.return_value = mock_wait_instance

            # First call (title check) succeeds, second call (document ready) times out
            mock_wait_instance.until.side_effect = [None, TimeoutException()]

            result = page.wait_for_page_load()

            # Should log warning about document ready timeout
            mock_logger.warning.assert_called_once_with(
                "Page did not reach complete ready state within timeout"
            )
            assert result == page
