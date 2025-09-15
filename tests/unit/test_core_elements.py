"""
Comprehensive unit tests for element wrapper classes.

This module tests the element wrapper classes with extensive mocking to ensure:
- BaseElement functionality and error handling
- Clickable element interactions (Button, Link)
- Input element operations (TextInput)
- Selection element behavior (Dropdown, Checkbox, RadioButton)
- Wait mechanisms and timeout handling
- Error scenarios and edge cases
"""

from unittest.mock import Mock, PropertyMock, patch

import pytest
from selenium.common.exceptions import (
    ElementNotInteractableException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By

from pmas.core.elements import (
    BaseElement,
    Button,
    Checkbox,
    Link,
    RadioButton,
    TextInput,
)
from pmas.core.errors import ElementNotFoundError, ElementNotInteractableError
from pmas.core.locators import Locator


class TestBaseElement:
    """Test BaseElement abstract base class."""

    def test_init_when_all_parameters_provided_expects_correct_setup(self):
        """Test BaseElement initialization with all parameters."""
        mock_driver = Mock()
        mock_locator = Mock(spec=Locator)
        timeout = 15.0

        # Create a concrete subclass for testing
        class ConcreteElement(BaseElement):
            pass

        element = ConcreteElement(mock_driver, mock_locator, timeout)

        assert element.driver == mock_driver
        assert element.locator == mock_locator
        assert element.timeout == 15.0
        assert element._element is None

    @patch("pmas.core.elements.WebDriverWait")
    def test_element_property_when_first_access_expects_element_found(self, mock_wait):
        """Test element property finds element on first access."""
        mock_driver = Mock()
        mock_locator = Mock(spec=Locator)
        mock_locator.selenium_locator = ("id", "test-element")
        mock_web_element = Mock()

        mock_wait_instance = Mock()
        mock_wait.return_value = mock_wait_instance
        mock_wait_instance.until.return_value = mock_web_element

        class ConcreteElement(BaseElement):
            pass

        element = ConcreteElement(mock_driver, mock_locator, 10.0)

        result = element.element

        assert result == mock_web_element
        assert element._element == mock_web_element
        mock_wait.assert_called_once_with(mock_driver, 10.0)

    @patch("pmas.core.elements.WebDriverWait")
    def test_element_property_when_timeout_expects_element_not_found_error(
        self, mock_wait
    ):
        """Test element property raises ElementNotFoundError on timeout."""
        mock_driver = Mock()
        mock_locator = Mock(spec=Locator)
        mock_locator.selenium_locator = ("id", "missing-element")

        mock_wait_instance = Mock()
        mock_wait.return_value = mock_wait_instance
        mock_wait_instance.until.side_effect = TimeoutException("Timeout")

        class ConcreteElement(BaseElement):
            pass

        element = ConcreteElement(mock_driver, mock_locator, 5.0)

        with pytest.raises(ElementNotFoundError) as exc_info:
            _ = element.element

        assert "Element not found" in str(exc_info.value)
        assert "5.0 seconds" in str(exc_info.value)

    @patch("pmas.core.elements.WebDriverWait")
    def test_element_property_when_stale_element_expects_refind(self, mock_wait):
        """Test element property refines element when stale."""
        mock_driver = Mock()
        mock_locator = Mock(spec=Locator)
        mock_locator.selenium_locator = ("id", "test-element")

        # Create stale element
        stale_element = Mock()
        type(stale_element).tag_name = PropertyMock(
            side_effect=StaleElementReferenceException("Stale")
        )

        # Create fresh element
        fresh_element = Mock()
        fresh_element.is_displayed.return_value = True

        # Mock WebDriverWait to return fresh element
        mock_wait_instance = Mock()
        mock_wait.return_value = mock_wait_instance
        mock_wait_instance.until.return_value = fresh_element

        class ConcreteElement(BaseElement):
            pass

        element = ConcreteElement(mock_driver, mock_locator, 10.0)
        element._element = stale_element

        result = element.element

        assert result == fresh_element

    def test_is_displayed_property_expects_element_is_displayed(self):
        """Test is_displayed property delegates to element."""
        mock_driver = Mock()
        mock_locator = Mock(spec=Locator)
        mock_web_element = Mock()
        mock_web_element.is_displayed.return_value = True

        class ConcreteElement(BaseElement):
            def _find_element(self):
                return mock_web_element

        element = ConcreteElement(mock_driver, mock_locator, 10.0)

        assert element.is_displayed is True
        mock_web_element.is_displayed.assert_called_once()

    def test_text_property_expects_element_text(self):
        """Test text property returns element text."""
        mock_driver = Mock()
        mock_locator = Mock(spec=Locator)
        mock_web_element = Mock()
        mock_web_element.text = "Element Text Content"

        class ConcreteElement(BaseElement):
            def _find_element(self):
                return mock_web_element

        element = ConcreteElement(mock_driver, mock_locator, 10.0)

        assert element.text == "Element Text Content"

    def test_get_attribute_when_attribute_exists_expects_value(self):
        """Test get_attribute returns attribute value."""
        mock_driver = Mock()
        mock_locator = Mock(spec=Locator)
        mock_web_element = Mock()
        mock_web_element.get_attribute.return_value = "attribute-value"

        class ConcreteElement(BaseElement):
            def _find_element(self):
                return mock_web_element

        element = ConcreteElement(mock_driver, mock_locator, 10.0)

        result = element.get_attribute("data-test")

        assert result == "attribute-value"
        mock_web_element.get_attribute.assert_called_once_with("data-test")


class TestClickableElements:
    """Test Clickable base class and Button/Link implementations."""

    def test_click_when_normal_click_expects_element_clicked(self):
        """Test normal click operation."""
        mock_driver = Mock()
        mock_locator = Mock(spec=Locator)
        mock_web_element = Mock()

        button = Button(mock_driver, mock_locator, 10.0)
        button._element = mock_web_element

        with (
            patch.object(button, "scroll_into_view"),
            patch.object(button, "wait_for_clickable"),
        ):
            result = button.click()

            mock_web_element.click.assert_called_once()
            assert result == button  # Should return self for chaining

    def test_click_when_force_click_expects_javascript_click(self):
        """Test force click uses JavaScript."""
        mock_driver = Mock()
        mock_locator = Mock(spec=Locator)
        mock_web_element = Mock()

        button = Button(mock_driver, mock_locator, 10.0)
        button._element = mock_web_element

        result = button.click(force=True)

        mock_driver.execute_script.assert_called_once_with(
            "arguments[0].click();", mock_web_element
        )
        assert result == button

    def test_click_when_element_not_interactable_expects_error(self):
        """
        Test click raises ElementNotInteractableError when element not
        interactable.
        """
        mock_driver = Mock()
        mock_locator = Mock(spec=Locator)
        mock_web_element = Mock()
        mock_web_element.click.side_effect = ElementNotInteractableException(
            "Not interactable"
        )

        button = Button(mock_driver, mock_locator, 10.0)
        button._element = mock_web_element

        with (
            patch.object(button, "scroll_into_view"),
            patch.object(button, "wait_for_clickable"),
        ):
            with pytest.raises(ElementNotInteractableError):
                button.click()

    @patch("pmas.core.elements.ActionChains")
    def test_double_click_when_called_expects_action_chains_double_click(
        self, mock_action_chains
    ):
        """Test double click uses ActionChains."""
        mock_driver = Mock()
        mock_locator = Mock(spec=Locator)
        mock_web_element = Mock()
        mock_chains = Mock()
        mock_action_chains.return_value = mock_chains
        mock_chains.double_click.return_value = mock_chains

        button = Button(mock_driver, mock_locator, 10.0)
        button._element = mock_web_element

        with (
            patch.object(button, "scroll_into_view"),
            patch.object(button, "wait_for_clickable"),
        ):
            result = button.double_click()

            mock_action_chains.assert_called_once_with(mock_driver)
            mock_chains.double_click.assert_called_once_with(mock_web_element)
            mock_chains.perform.assert_called_once()
            assert result == button

    @patch("pmas.core.elements.ActionChains")
    def test_right_click_when_called_expects_action_chains_context_click(
        self, mock_action_chains
    ):
        """Test right click uses ActionChains context_click."""
        mock_driver = Mock()
        mock_locator = Mock(spec=Locator)
        mock_web_element = Mock()
        mock_chains = Mock()
        mock_action_chains.return_value = mock_chains
        mock_chains.context_click.return_value = mock_chains

        button = Button(mock_driver, mock_locator, 10.0)
        button._element = mock_web_element

        with (
            patch.object(button, "scroll_into_view"),
            patch.object(button, "wait_for_clickable"),
        ):
            result = button.right_click()

            mock_action_chains.assert_called_once_with(mock_driver)
            mock_chains.context_click.assert_called_once_with(mock_web_element)
            mock_chains.perform.assert_called_once()
            assert result == button


class TestLinkElement:
    """Test Link element specific functionality."""

    def test_href_property_when_href_exists_expects_url(self):
        """Test href property returns href attribute."""
        mock_driver = Mock()
        mock_locator = Mock(spec=Locator)
        mock_web_element = Mock()
        mock_web_element.get_attribute.return_value = "https://example.com"

        link = Link(mock_driver, mock_locator, 10.0)
        link._element = mock_web_element

        result = link.href

        assert result == "https://example.com"
        mock_web_element.get_attribute.assert_called_once_with("href")


class TestTextInputElement:
    """Test TextInput element functionality."""

    def test_type_text_when_text_provided_expects_text_sent(self):
        """Test type_text sends text to element."""
        mock_driver = Mock()
        mock_locator = Mock(spec=Locator)
        mock_locator.selenium_locator = ("id", "test-input")
        mock_web_element = Mock()

        text_input = TextInput(mock_driver, mock_locator, 10.0)
        text_input._element = mock_web_element

        with (
            patch.object(text_input, "scroll_into_view"),
            patch.object(text_input, "wait_for_clickable"),
            patch.object(text_input, "wait_for_visible"),
        ):
            result = text_input.type_text("Hello World")

            mock_web_element.send_keys.assert_called_once_with("Hello World")
            assert result == text_input

    def test_clear_when_called_expects_element_cleared(self):
        """Test clear method clears element."""
        mock_driver = Mock()
        mock_locator = Mock(spec=Locator)
        mock_locator.selenium_locator = ("id", "test-input")
        mock_web_element = Mock()

        text_input = TextInput(mock_driver, mock_locator, 10.0)
        text_input._element = mock_web_element

        with patch.object(text_input, "wait_for_visible"):
            result = text_input.clear()

            mock_web_element.clear.assert_called_once()
            assert result == text_input

    def test_value_property_expects_value_attribute(self):
        """Test value property returns value attribute."""
        mock_driver = Mock()
        mock_locator = Mock(spec=Locator)
        mock_web_element = Mock()
        mock_web_element.get_attribute.return_value = "input value"

        text_input = TextInput(mock_driver, mock_locator, 10.0)
        text_input._element = mock_web_element

        result = text_input.value

        assert result == "input value"
        mock_web_element.get_attribute.assert_called_once_with("value")


class TestCheckboxElement:
    """Test Checkbox element functionality."""

    def test_check_when_not_checked_expects_clicked(self):
        """Test check method clicks when checkbox not checked."""
        mock_driver = Mock()
        mock_locator = Mock(spec=Locator)
        mock_web_element = Mock()
        mock_web_element.is_selected.return_value = False

        checkbox = Checkbox(mock_driver, mock_locator, 10.0)
        checkbox._element = mock_web_element

        with (
            patch.object(checkbox, "scroll_into_view"),
            patch.object(checkbox, "wait_for_clickable"),
        ):
            result = checkbox.check()

            mock_web_element.click.assert_called_once()
            assert result == checkbox

    def test_check_when_already_checked_expects_no_click(self):
        """Test check method does not click when already checked."""
        mock_driver = Mock()
        mock_locator = Mock(spec=Locator)
        mock_web_element = Mock()
        mock_web_element.is_selected.return_value = True

        checkbox = Checkbox(mock_driver, mock_locator, 10.0)
        checkbox._element = mock_web_element

        result = checkbox.check()

        mock_web_element.click.assert_not_called()
        assert result == checkbox

    def test_uncheck_when_checked_expects_clicked(self):
        """Test uncheck method clicks when checkbox is checked."""
        mock_driver = Mock()
        mock_locator = Mock(spec=Locator)
        mock_web_element = Mock()
        mock_web_element.is_selected.return_value = True

        checkbox = Checkbox(mock_driver, mock_locator, 10.0)
        checkbox._element = mock_web_element

        with (
            patch.object(checkbox, "scroll_into_view"),
            patch.object(checkbox, "wait_for_clickable"),
        ):
            result = checkbox.uncheck()

            mock_web_element.click.assert_called_once()
            assert result == checkbox

    def test_toggle_when_called_expects_clicked(self):
        """Test toggle method always clicks."""
        mock_driver = Mock()
        mock_locator = Mock(spec=Locator)
        mock_web_element = Mock()

        checkbox = Checkbox(mock_driver, mock_locator, 10.0)
        checkbox._element = mock_web_element

        with (
            patch.object(checkbox, "scroll_into_view"),
            patch.object(checkbox, "wait_for_clickable"),
        ):
            result = checkbox.toggle()

            mock_web_element.click.assert_called_once()
            assert result == checkbox

    def test_is_checked_property_expects_is_selected(self):
        """Test is_checked property returns is_selected."""
        mock_driver = Mock()
        mock_locator = Mock(spec=Locator)
        mock_web_element = Mock()
        mock_web_element.is_selected.return_value = True

        checkbox = Checkbox(mock_driver, mock_locator, 10.0)
        checkbox._element = mock_web_element

        assert checkbox.is_checked is True
        mock_web_element.is_selected.assert_called_once()


class TestRadioButtonElement:
    """Test RadioButton element functionality."""

    def test_select_when_not_selected_expects_clicked(self):
        """Test select method clicks when radio button not selected."""
        mock_driver = Mock()
        mock_locator = Mock(spec=Locator)
        mock_web_element = Mock()
        mock_web_element.is_selected.return_value = False

        radio = RadioButton(mock_driver, mock_locator, 10.0)
        radio._element = mock_web_element

        with (
            patch.object(radio, "scroll_into_view"),
            patch.object(radio, "wait_for_clickable"),
        ):
            result = radio.select()

            mock_web_element.click.assert_called_once()
            assert result == radio

    def test_is_selected_property_expects_is_selected(self):
        """Test is_selected property returns element is_selected."""
        mock_driver = Mock()
        mock_locator = Mock(spec=Locator)
        mock_web_element = Mock()
        mock_web_element.is_selected.return_value = True

        radio = RadioButton(mock_driver, mock_locator, 10.0)
        radio._element = mock_web_element

        assert radio.is_selected is True
        mock_web_element.is_selected.assert_called_once()


class TestElementsBranchCoverage:
    """Test specific conditional branches to improve branch coverage."""

    def test_base_element_is_stale_when_element_none_expects_false(self):
        """Test _is_stale returns False when element is None."""
        mock_driver = Mock()
        mock_locator = Mock()
        mock_locator.selenium_locator = (By.ID, "test-element")

        element = BaseElement(mock_driver, mock_locator)
        element._element = None

        result = element._is_stale()

        assert result is False

    def test_base_element_is_stale_when_element_not_stale_expects_false(self):
        """Test _is_stale returns False when element is not stale."""
        mock_driver = Mock()
        mock_locator = Mock()
        mock_locator.selenium_locator = (By.ID, "test-element")
        mock_element = Mock()
        mock_element.tag_name = "div"  # No exception raised

        element = BaseElement(mock_driver, mock_locator)
        element._element = mock_element

        result = element._is_stale()

        assert result is False

    def test_base_element_is_stale_when_stale_element_expects_true(self):
        """Test _is_stale returns True when element is stale."""
        from selenium.common.exceptions import StaleElementReferenceException

        mock_driver = Mock()
        mock_locator = Mock()
        mock_locator.selenium_locator = (By.ID, "test-element")
        mock_element = Mock()

        # Configure the tag_name property to raise StaleElementReferenceException
        type(mock_element).tag_name = PropertyMock(
            side_effect=StaleElementReferenceException()
        )

        element = BaseElement(mock_driver, mock_locator)
        element._element = mock_element

        result = element._is_stale()

        assert result is True

    def test_wait_for_clickable_when_timeout_provided_expects_custom_timeout(self):
        """Test wait_for_clickable uses provided timeout instead of default."""
        with patch("pmas.core.elements.WebDriverWait") as mock_wait:
            mock_driver = Mock()
            mock_locator = Mock()
            mock_locator.selenium_locator = (By.ID, "test-element")
            mock_wait_instance = Mock()
            mock_wait.return_value = mock_wait_instance

            element = BaseElement(mock_driver, mock_locator, timeout=10.0)

            result = element.wait_for_clickable(timeout=5.0)

            # Should use provided timeout (5.0), not default (10.0)
            mock_wait.assert_called_once_with(mock_driver, 5.0)
            assert result == element

    def test_wait_for_clickable_when_no_timeout_expects_default_timeout(self):
        """Test wait_for_clickable uses default timeout when none provided."""
        with patch("pmas.core.elements.WebDriverWait") as mock_wait:
            mock_driver = Mock()
            mock_locator = Mock()
            mock_locator.selenium_locator = (By.ID, "test-element")
            mock_wait_instance = Mock()
            mock_wait.return_value = mock_wait_instance

            element = BaseElement(mock_driver, mock_locator, timeout=15.0)

            result = element.wait_for_clickable()

            # Should use default timeout (15.0)
            mock_wait.assert_called_once_with(mock_driver, 15.0)
            assert result == element
