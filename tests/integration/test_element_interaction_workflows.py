"""
Integration tests for PMAS element interaction workflows.

This module tests complex element interaction scenarios that span multiple
components and simulate real-world usage patterns. Tests cover:
- Form filling and submission workflows
- Element state management across interactions
- Wait conditions and timing integration
- Error recovery and retry mechanisms
- Cross-element dependencies and validation

Uses FakeWebDriver to simulate realistic element behaviors and timing.
No external dependencies or network calls.
"""

import pytest
from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
    WebDriverException,
)

from pmas.core.locators import by_id
from pmas.core.page import BasePage

from ..fakes.fake_webdriver import FakeWebDriver, FakeWebElement


class FormPage(BasePage):
    """Test page with form elements for integration testing."""

    def __init__(self, driver, base_url="http://test.example.com", timeout=5.0):
        super().__init__(driver, base_url, timeout)
        self.url_path = "/form"

    def verify_page_loaded(self) -> bool:
        """Verify the form page is loaded."""
        return self.is_element_present(by_id("form-container"))

    def fill_login_form(self, username: str, password: str, remember_me: bool = False):
        """Fill the login form with provided data."""
        username_input = self.get_text_input(by_id("username"))
        password_input = self.get_text_input(by_id("password"))
        remember_checkbox = self.get_checkbox(by_id("remember-me"))

        username_input.clear()
        username_input.type_text(username)

        password_input.clear()
        password_input.type_text(password)

        if remember_me:
            remember_checkbox.check()
        else:
            remember_checkbox.uncheck()

    def submit_form(self):
        """Submit the form."""
        submit_button = self.get_button(by_id("submit-btn"))
        submit_button.click()

    def get_error_message(self) -> str:
        """Get error message if present."""
        try:
            error_element = self.driver.find_element("css", ".error-message")
            return error_element.text
        except NoSuchElementException:
            return ""


@pytest.mark.integration
class TestElementInteractionWorkflows:
    """Integration tests for element interaction workflows."""

    @pytest.fixture
    def fake_driver(self) -> FakeWebDriver:
        """Provide a configured fake driver with form elements."""
        driver = FakeWebDriver()

        # Set up form page elements
        driver.add_element(
            "id:form-container",
            FakeWebElement("div", attributes={"id": "form-container"}),
        )
        driver.add_element(
            "id:username",
            FakeWebElement("input", attributes={"type": "text", "id": "username"}),
        )
        driver.add_element(
            "id:password",
            FakeWebElement("input", attributes={"type": "password", "id": "password"}),
        )
        driver.add_element(
            "id:remember-me",
            FakeWebElement(
                "input", attributes={"type": "checkbox", "id": "remember-me"}
            ),
        )
        driver.add_element(
            "id:submit-btn",
            FakeWebElement("button", text="Submit", attributes={"id": "submit-btn"}),
        )
        driver.add_element(
            "css:.error-message",
            FakeWebElement("div", text="", attributes={"class": "error-message"}),
        )

        return driver

    def test_complete_form_filling_workflow(self, fake_driver: FakeWebDriver):
        """Test complete form filling and submission workflow."""
        page = FormPage(fake_driver)
        page.navigate_to()

        # Verify page loaded
        assert page.verify_page_loaded() is True

        # Fill form with test data
        test_username = "test_user"
        test_password = "secure_password"

        page.fill_login_form(test_username, test_password, remember_me=True)

        # Verify form was filled correctly
        username_element = fake_driver._elements_registry["id:username"]
        password_element = fake_driver._elements_registry["id:password"]
        checkbox_element = fake_driver._elements_registry["id:remember-me"]

        assert username_element._text_input == test_username
        assert password_element._text_input == test_password
        assert checkbox_element._is_selected is True

        # Submit form
        page.submit_form()

        # Verify submission
        submit_element = fake_driver._elements_registry["id:submit-btn"]
        assert submit_element._click_count == 1

    def test_form_validation_and_error_handling_workflow(
        self, fake_driver: FakeWebDriver
    ):
        """Test form validation and error handling workflow."""
        page = FormPage(fake_driver)
        page.navigate_to()

        # Test empty form submission
        page.submit_form()

        # Simulate validation error
        error_element = fake_driver._elements_registry["css:.error-message"]
        error_element.text = "Username and password are required"

        error_message = page.get_error_message()
        assert "required" in error_message

        # Fill form with invalid data
        page.fill_login_form("", "short", remember_me=False)
        page.submit_form()

        # Verify form state after error
        username_element = fake_driver._elements_registry["id:username"]
        password_element = fake_driver._elements_registry["id:password"]

        assert username_element._text_input == ""
        assert password_element._text_input == "short"

    def test_element_state_persistence_across_interactions(
        self, fake_driver: FakeWebDriver
    ):
        """Test element state persistence across multiple interactions."""
        page = FormPage(fake_driver)
        page.navigate_to()

        # Get element references
        username_input = page.get_text_input(by_id("username"))
        password_input = page.get_text_input(by_id("password"))

        # Perform multiple interactions
        username_input.type_text("user")
        username_input.append_text("123")  # Append

        password_input.type_text("pass")
        password_input.clear()
        password_input.type_text("newpass")

        # Verify final state
        username_element = fake_driver._elements_registry["id:username"]
        password_element = fake_driver._elements_registry["id:password"]

        assert username_element._text_input == "user123"
        assert password_element._text_input == "newpass"

    def test_checkbox_state_management_workflow(self, fake_driver: FakeWebDriver):
        """Test checkbox state management across interactions."""
        page = FormPage(fake_driver)
        page.navigate_to()

        checkbox = page.get_checkbox(by_id("remember-me"))

        # Test initial state
        assert checkbox.is_checked is False

        # Test check operation
        checkbox.check()
        assert checkbox.is_checked is True

        # Test check when already checked (should remain checked)
        checkbox.check()
        assert checkbox.is_checked is True

        # Test uncheck operation
        checkbox.uncheck()
        assert checkbox.is_checked is False

        # Test toggle operations
        checkbox.toggle()
        assert checkbox.is_checked is True

        checkbox.toggle()
        assert checkbox.is_checked is False

    def test_element_interaction_error_recovery(self, fake_driver: FakeWebDriver):
        """Test error recovery in element interactions."""
        page = FormPage(fake_driver)
        page.navigate_to()

        # Configure element to be disabled
        username_element = fake_driver._elements_registry["id:username"]
        username_element._is_enabled = False

        username_input = page.get_text_input(by_id("username"))

        # Test interaction with disabled element
        with pytest.raises((ElementNotInteractableException, WebDriverException)):
            username_input.type_text("test")

        # Re-enable element and retry
        username_element._is_enabled = True
        username_input.type_text("test")  # Should work now

        assert username_element._text_input == "test"

    def test_stale_element_recovery_workflow(self, fake_driver: FakeWebDriver):
        """Test stale element recovery workflow."""
        page = FormPage(fake_driver)
        page.navigate_to()

        # Get element reference
        submit_button = page.get_button(by_id("submit-btn"))

        # Simulate page refresh (elements become stale)
        fake_driver.refresh()

        # Re-add elements after refresh
        fake_driver.add_element(
            "id:submit-btn",
            FakeWebElement("button", text="Submit", attributes={"id": "submit-btn"}),
        )

        # Element should be re-found automatically
        submit_button.click()

        # Verify interaction worked
        new_submit_element = fake_driver._elements_registry["id:submit-btn"]
        assert new_submit_element._click_count == 1

    def test_multiple_element_coordination_workflow(self, fake_driver: FakeWebDriver):
        """Test coordination between multiple elements."""
        page = FormPage(fake_driver)
        page.navigate_to()

        # Get multiple element references
        username_input = page.get_text_input(by_id("username"))
        password_input = page.get_text_input(by_id("password"))
        submit_button = page.get_button(by_id("submit-btn"))

        # Coordinate interactions
        username_input.type_text("admin")
        password_input.type_text("password")

        # Verify both fields are filled before submission
        assert username_input.value == "admin"
        assert password_input.value == "password"

        # Submit form
        submit_button.click()

        # Verify all interactions were recorded
        operations = fake_driver.operation_log
        find_operations = [op for op in operations if op["operation"] == "find_element"]
        assert len(find_operations) >= 3  # At least one for each element

    def test_element_timing_and_wait_integration(self, fake_driver: FakeWebDriver):
        """Test element timing and wait condition integration."""
        page = FormPage(fake_driver)
        page.navigate_to()

        # Configure delays for realistic timing
        fake_driver.configure_response_delay("find_element", 0.1)

        # Test element finding with timing
        start_time = (
            fake_driver.operation_log[-1]["timestamp"]
            if fake_driver.operation_log
            else 0
        )

        username_input = page.get_text_input(by_id("username"))
        username_input.type_text("test")

        # Verify timing was applied
        find_operations = [
            op for op in fake_driver.operation_log if op["operation"] == "find_element"
        ]
        if find_operations:
            last_find = find_operations[-1]
            assert last_find["timestamp"] > start_time

    def test_form_reset_and_state_cleanup_workflow(self, fake_driver: FakeWebDriver):
        """Test form reset and state cleanup workflow."""
        page = FormPage(fake_driver)
        page.navigate_to()

        # Fill form completely
        page.fill_login_form("testuser", "testpass", remember_me=True)

        # Verify form is filled
        username_element = fake_driver._elements_registry["id:username"]
        password_element = fake_driver._elements_registry["id:password"]
        checkbox_element = fake_driver._elements_registry["id:remember-me"]

        assert username_element._text_input == "testuser"
        assert password_element._text_input == "testpass"
        assert checkbox_element._is_selected is True

        # Reset form by clearing all fields
        username_input = page.get_text_input(by_id("username"))
        password_input = page.get_text_input(by_id("password"))
        checkbox = page.get_checkbox(by_id("remember-me"))

        username_input.clear()
        password_input.clear()
        checkbox.uncheck()

        # Verify form is reset
        assert username_element._text_input == ""
        assert password_element._text_input == ""
        assert checkbox_element._is_selected is False

    def test_concurrent_element_access_workflow(self, fake_driver: FakeWebDriver):
        """Test concurrent access to the same elements."""
        page = FormPage(fake_driver)
        page.navigate_to()

        # Get multiple references to the same element
        username_input1 = page.get_text_input(by_id("username"))
        username_input2 = page.get_text_input(by_id("username"))

        # Interact through different references
        username_input1.type_text("user")
        username_input2.append_text("name")

        # Verify state is consistent
        username_element = fake_driver._elements_registry["id:username"]
        assert username_element._text_input == "username"

        # Both references should reflect the same state
        assert username_input1.value == username_input2.value

    def test_element_interaction_logging_and_verification(
        self, fake_driver: FakeWebDriver
    ):
        """Test element interaction logging and verification."""
        page = FormPage(fake_driver)
        page.navigate_to()

        # Perform various interactions
        page.fill_login_form("testuser", "testpass", remember_me=True)
        page.submit_form()

        # Verify operation log contains expected interactions
        operations = [op["operation"] for op in fake_driver.operation_log]

        # Should contain navigation, element finding, and interactions
        assert "get" in operations  # Navigation
        assert "find_element" in operations  # Element finding

        # Verify specific element interactions
        username_element = fake_driver._elements_registry["id:username"]
        password_element = fake_driver._elements_registry["id:password"]
        submit_element = fake_driver._elements_registry["id:submit-btn"]
        checkbox_element = fake_driver._elements_registry["id:remember-me"]

        assert username_element._text_input == "testuser"
        assert password_element._text_input == "testpass"
        assert submit_element._click_count == 1
        assert checkbox_element._is_selected is True
