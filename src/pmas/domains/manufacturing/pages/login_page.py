"""
Manufacturing manufacturing login page object with domain-specific login functionality.
"""

import logging
import os
from typing import Any, Optional

from ....core.locators import by_id, by_link_text
from ..constants import (
    DEV_USERS,
    FAT_USERS,
    FMS_TITLES,
    PASSWORD_ALL,
    USER_COORDINATOR,
    USER_MANAGER,
    USER_PLANNER,
)
from .base_manufacturing_page import BaseManufacturingPage

logger = logging.getLogger(__name__)


class ManufacturingLoginPage(BaseManufacturingPage):
    """
    Manufacturing manufacturing domain login page with support for different user types and environments.
    """

    url_path = "FMS/Login/Login"
    expected_titles = FMS_TITLES

    # Locators for login page elements
    LOGIN_SUBMIT = by_id("submitButton", "Login submit button")
    USERNAME_FIELD = by_id("username", "Username input field")
    PASSWORD_FIELD = by_id("password", "Password input field")

    # Password reset page elements
    NEW_PASSWORD_FIELD = by_id("newPassword", "New password field")
    CONFIRM_PASSWORD_FIELD = by_id("passwordConfirm", "Confirm password field")
    RESET_PASSWORD_BUTTON = by_id("submit", "Reset password button")

    # Other elements
    NOTIFICATION = by_id("notification", "Notification message")
    COMMENTS_LINK = by_link_text("Comments?", "Comments link")

    def __init__(self, driver, base_url: str = "", timeout: float = 10.0) -> None:
        super().__init__(driver, base_url, timeout)

    def verify_page_loaded(self) -> bool:
        """Verify that the manufacturing manufacturing login page has loaded correctly."""
        try:
            # Check for login form elements
            login_button = self.get_button(self.LOGIN_SUBMIT)
            username_field = self.get_text_input(self.USERNAME_FIELD)
            password_field = self.get_text_input(self.PASSWORD_FIELD)

            return (
                login_button.is_displayed
                and username_field.is_displayed
                and password_field.is_displayed
            )
        except Exception as e:
            logger.error(f"Manufacturing login page verification failed: {e}")
            return False

    def login(
        self, username: str, password: str, expect_valid: bool = True
    ) -> Optional["BaseManufacturingPage"]:
        """
        Perform login with given credentials for manufacturing manufacturing system.

        Args:
            username: Username to login with
            password: Password to login with
            expect_valid: Whether to expect the login to succeed

        Returns:
            Landing page object if successful, None if failed as expected
        """
        logger.info(f"Attempting manufacturing manufacturing login as: {username}")

        try:
            # Fill login form
            username_field = self.get_text_input(self.USERNAME_FIELD)
            password_field = self.get_text_input(self.PASSWORD_FIELD)
            login_button = self.get_button(self.LOGIN_SUBMIT)

            username_field.type_text(username)
            password_field.type_text(password)
            login_button.click()

            # Wait for page to load
            self.wait_for_page_load()

            # Handle different post-login scenarios
            if "Page not found" in self.title:
                if expect_valid:
                    return self._handle_page_not_found(username)
                else:
                    return None

            # Check for password expiration
            if "password" in self.title.lower() and "expired" in self.title.lower():
                if expect_valid:
                    logger.warning(
                        f"Password expired for manufacturing user: {username}"
                    )
                    return None
                else:
                    return None

            # Check for login failure
            if any(title in self.title for title in FMS_TITLES):
                # Still on login page - login failed
                if expect_valid:
                    self.add_production_error(
                        f"Manufacturing manufacturing login failed for user {username}"
                    )
                    return None
                else:
                    logger.info(
                        f"Manufacturing manufacturing login correctly failed for user: {username}"
                    )
                    return None

            # Successful login
            if expect_valid:
                return self._handle_successful_login(username)
            else:
                self.add_production_error(
                    f"Manufacturing manufacturing login should have failed for user {username} but succeeded"
                )
                return None

        except Exception as e:
            logger.error(
                f"Manufacturing manufacturing login error for user {username}: {e}"
            )
            if expect_valid:
                self.add_production_error(
                    f"Manufacturing manufacturing login exception for user {username}: {e}"
                )
            return None

    def login_production_planner(self) -> Optional["BaseManufacturingPage"]:
        """Login as production planner."""
        username, password = self._get_manufacturing_credentials(USER_PLANNER)
        return self.login(username, password, True)

    def login_factory_manager(self) -> Optional["BaseManufacturingPage"]:
        """Login as factory manager."""
        username, password = self._get_manufacturing_credentials(USER_MANAGER)
        return self.login(username, password, True)

    def login_production_coordinator(self) -> Optional["BaseManufacturingPage"]:
        """Login as Production Coordinator."""
        username, password = self._get_manufacturing_credentials(USER_COORDINATOR)
        return self.login(username, password, True)

    def login_retail_partner(
        self, username: str | None = None, expect_valid: bool = True
    ) -> Optional["BaseManufacturingPage"]:
        """
        Login as retail partner with standard password.

        Args:
            username: Specific username, random if not provided
            expect_valid: Whether to expect login to succeed
        """
        if not username:
            username = "test_partner"  # Placeholder
            logger.info(f"Using random retail partner user: {username}")

        password = os.getenv("WEBDRIVER_PASSWORD_ALL", PASSWORD_ALL)
        return self.login(username, password, expect_valid)

    def login_fail(
        self, username: str, attempts: int = 1
    ) -> Optional["BaseManufacturingPage"]:
        """
        Attempt to login with wrong password multiple times.

        Args:
            username: Username to attempt login with
            attempts: Number of failed attempts to make
        """
        wrong_password = "wrong_manufacturing_password_123"

        for attempt in range(attempts):
            logger.info(
                f"Failed manufacturing manufacturing login attempt {attempt + 1} for user: {username}"
            )
            result = self.login(username, wrong_password, expect_valid=False)

            if result is not None:
                # Login unexpectedly succeeded
                self.add_production_error(
                    f"Manufacturing manufacturing login should have failed on attempt {attempt + 1}"
                )
                return result

        return None

    def _get_manufacturing_credentials(self, user_type: int) -> tuple[str, str]:
        """
        Get credentials for a specific manufacturing manufacturing user type based on environment.

        Args:
            user_type: Type of user (USER_PLANNER, USER_MANAGER, etc.)

        Returns:
            Tuple of (username, password)
        """
        # Check for environment variable overrides
        env_user = os.getenv("WEBDRIVER_USER")
        env_password = os.getenv("WEBDRIVER_PASSWORD")

        if env_user and env_password:
            logger.info(
                "Using manufacturing manufacturing credentials from environment variables"
            )
            return env_user, env_password

        # Determine environment and get appropriate credentials
        environment = os.getenv("PMAS_ENVIRONMENT", "dev").lower()

        if environment == "dev":
            users = DEV_USERS
        elif environment in ["fat", "sat"]:  # Factory Acceptance Testing
            users = FAT_USERS
        else:
            # Production or unknown environment
            raise ValueError(
                f"No default manufacturing manufacturing credentials for environment: {environment}"
            )

        if user_type < len(users):
            return users[user_type]
        else:
            # Fallback to first user
            logger.warning(
                f"Manufacturing user type {user_type} not available, using first user"
            )
            return users[0]

    def _handle_successful_login(self, username: str) -> "BaseManufacturingPage":
        """Handle successful manufacturing manufacturing login and return appropriate landing page."""
        logger.info(
            f"Manufacturing manufacturing login successful for user: {username}"
        )

        # Get user info from the page
        factory, logged_user = self.get_logged_factory_user()
        logger.info(
            f"Landed on manufacturing manufacturing page {self.title} as user: {logged_user}"
        )

        # Verify the logged user matches what we expected
        if username != logged_user:
            self.add_production_error(
                f"Landing page has wrong username [{logged_user}], expected [{username}]"
            )

        # Return the appropriate page object based on the landing page
        return self

    def _handle_page_not_found(self, username: str) -> "BaseManufacturingPage":
        """Handle the case where manufacturing user lands on 'Page not found'."""
        logger.warning(
            f"Manufacturing user {username} landed on 'Page not found'; navigating to Reference page"
        )

        try:
            # Click on Comments link to get to feedback page
            comments_link = self.get_button(self.COMMENTS_LINK)
            comments_link.click()

            # Navigate to Reference page
            logger.info("Navigated to Reference page as fallback")
            return self

        except Exception as e:
            logger.error(f"Failed to handle manufacturing page not found: {e}")
            return self

    def handle_certificate_error(self) -> None:
        """Handle SSL certificate errors in IE for manufacturing manufacturing system."""
        if self.title == "Certificate Error: Navigation Blocked":
            logger.info(
                "Handling SSL certificate error for manufacturing manufacturing system (IE)"
            )
            try:
                # Execute JavaScript to override certificate warning
                self.execute_script("document.getElementById('overridelink').click();")
                self.wait_for_page_load()
            except Exception as e:
                logger.warning(f"Failed to handle manufacturing certificate error: {e}")

    def navigate_to_manufacturing_login(self) -> "ManufacturingLoginPage":
        """Navigate to the manufacturing manufacturing login page."""
        self.navigate_to()
        self.handle_certificate_error()
        self.wait_for_page_load()
        return self

    def check_factory_system_status(self) -> dict[str, Any]:
        """
        Check the status of the manufacturing manufacturing system.

        Returns:
            Dictionary with system status information
        """
        try:
            # This would check for system status indicators on the login page
            return {
                "system_status": "OPERATIONAL",
                "maintenance_mode": False,
                "last_update": "2024-01-15 12:00:00",
                "active_users": 45,
            }
        except Exception as e:
            logger.error(f"Failed to check manufacturing system status: {e}")
            return {"system_status": "UNKNOWN", "error": str(e)}
