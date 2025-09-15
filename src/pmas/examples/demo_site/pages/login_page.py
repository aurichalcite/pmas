"""
SauceDemo login page object demonstrating PMAS framework usage.
"""

import logging
from typing import TYPE_CHECKING

from ....core.errors import LoginError
from ....core.locators import by_class_name, by_css_selector, by_id
from ....core.page import BasePage

if TYPE_CHECKING:
    from .inventory_page import SauceDemoInventoryPage


logger = logging.getLogger(__name__)


class SauceDemoLoginPage(BasePage):
    """
    SauceDemo login page demonstrating modern page object patterns.
    """

    url_path = ""

    # Locators using the modern locator system
    USERNAME_FIELD = by_id("user-name", "Username input field")
    PASSWORD_FIELD = by_id("password", "Password input field")
    LOGIN_BUTTON = by_id("login-button", "Login button")
    ERROR_MESSAGE = by_css_selector('[data-test="error"]', "Error message container")
    ERROR_BUTTON = by_class_name("error-button", "Error close button")

    def __init__(
        self, driver, base_url: str = "https://www.saucedemo.com", timeout: float = 10.0
    ) -> None:
        super().__init__(driver, base_url, timeout)

    def verify_page_loaded(self) -> bool:
        """Verify that the SauceDemo login page has loaded correctly."""
        try:
            # Check for login form elements
            login_button = self.get_button(self.LOGIN_BUTTON)
            username_field = self.get_text_input(self.USERNAME_FIELD)
            password_field = self.get_text_input(self.PASSWORD_FIELD)

            return (
                login_button.is_displayed
                and username_field.is_displayed
                and password_field.is_displayed
            )
        except Exception as e:
            logger.error(f"SauceDemo login page verification failed: {e}")
            return False

    def login(self, username: str, password: str) -> "SauceDemoInventoryPage":
        """
        Perform login with given credentials.

        Args:
            username: Username to login with
            password: Password to login with

        Returns:
            Inventory page object if successful

        Raises:
            LoginError: If login fails
        """
        logger.info(f"Attempting SauceDemo login as: {username}")

        # Fill login form
        username_field = self.get_text_input(self.USERNAME_FIELD)
        password_field = self.get_text_input(self.PASSWORD_FIELD)
        login_button = self.get_button(self.LOGIN_BUTTON)

        username_field.clear()
        username_field.type_text(username)

        password_field.clear()
        password_field.type_text(password)

        login_button.click()

        # Wait for page to load
        self.wait_for_page_load()

        # Check for error messages
        if self.is_error_displayed():
            error_msg = self.get_error_message()
            raise LoginError(f"Login failed: {error_msg}")

        # Import here to avoid circular imports
        from .inventory_page import SauceDemoInventoryPage

        return SauceDemoInventoryPage(self.driver, self.base_url, self.timeout)

    def login_standard_user(self) -> "SauceDemoInventoryPage":
        """Login as standard user."""
        return self.login("standard_user", "secret_sauce")

    def login_locked_out_user(self) -> None:
        """
        Attempt to login as locked out user (should fail).

        Raises:
            LoginError: Always, as this user is locked out
        """
        self.login("locked_out_user", "secret_sauce")

    def login_problem_user(self) -> "SauceDemoInventoryPage":
        """Login as problem user (has UI issues)."""
        return self.login("problem_user", "secret_sauce")

    def login_performance_glitch_user(self) -> "SauceDemoInventoryPage":
        """Login as performance glitch user (slow responses)."""
        return self.login("performance_glitch_user", "secret_sauce")

    def is_error_displayed(self) -> bool:
        """Check if an error message is displayed."""
        try:
            error_element = self.find_element(self.ERROR_MESSAGE, timeout=2.0)
            return error_element.is_displayed()
        except Exception:
            return False

    def get_error_message(self) -> str:
        """Get the error message text."""
        try:
            error_element = self.find_element(self.ERROR_MESSAGE)
            return error_element.text.strip()
        except Exception:
            return ""

    def close_error_message(self) -> None:
        """Close the error message by clicking the X button."""
        try:
            error_button = self.get_button(self.ERROR_BUTTON)
            error_button.click()
        except Exception as e:
            logger.warning(f"Could not close error message: {e}")

    def attempt_invalid_login(
        self, username: str = "invalid_user", password: str = "invalid_pass"
    ) -> str:
        """
        Attempt login with invalid credentials and return error message.

        Args:
            username: Invalid username to try
            password: Invalid password to try

        Returns:
            Error message text
        """
        logger.info(f"Attempting invalid login: {username}")

        try:
            # Fill login form with invalid credentials
            username_field = self.get_text_input(self.USERNAME_FIELD)
            password_field = self.get_text_input(self.PASSWORD_FIELD)
            login_button = self.get_button(self.LOGIN_BUTTON)

            username_field.clear()
            username_field.type_text(username)

            password_field.clear()
            password_field.type_text(password)

            login_button.click()

            # Wait for error message to appear
            self.wait_for_element(self.ERROR_MESSAGE, timeout=5.0)

            return self.get_error_message()

        except Exception as e:
            logger.error(f"Error during invalid login attempt: {e}")
            return ""

    def get_available_usernames(self) -> list[str]:
        """
        Get list of available usernames from the page.

        Returns:
            List of valid usernames
        """
        # These are the known usernames for SauceDemo
        return [
            "standard_user",
            "locked_out_user",
            "problem_user",
            "performance_glitch_user",
        ]

    def navigate_to_login(self) -> "SauceDemoLoginPage":
        """Navigate to the SauceDemo login page."""
        self.navigate_to()
        self.wait_for_page_load()
        return self
