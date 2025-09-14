"""
Example tests for SauceDemo login functionality demonstrating PMAS framework usage.
"""

import pytest

from ....testing.assertions import SoftAssertions
from ..pages.login_page import SauceDemoLoginPage


class TestSauceDemoLogin:
    """Test class demonstrating login functionality testing with PMAS framework."""

    def test_successful_login_standard_user(self, driver, config):
        """Test successful login with standard user."""
        # Arrange
        login_page = SauceDemoLoginPage(driver, config.environment.base_url)
        login_page.navigate_to_login()

        # Act
        inventory_page = login_page.login_standard_user()

        # Assert
        assert inventory_page.verify_page_loaded()
        assert "inventory.html" in inventory_page.current_url

    def test_successful_login_problem_user(self, driver, config):
        """Test successful login with problem user."""
        # Arrange
        login_page = SauceDemoLoginPage(driver, config.environment.base_url)
        login_page.navigate_to_login()

        # Act
        inventory_page = login_page.login_problem_user()

        # Assert
        assert inventory_page.verify_page_loaded()
        assert "inventory.html" in inventory_page.current_url

    def test_successful_login_performance_glitch_user(self, driver, config):
        """Test successful login with performance glitch user."""
        # Arrange
        login_page = SauceDemoLoginPage(driver, config.environment.base_url)
        login_page.navigate_to_login()

        # Act
        inventory_page = login_page.login_performance_glitch_user()

        # Assert
        assert inventory_page.verify_page_loaded()
        assert "inventory.html" in inventory_page.current_url

    def test_locked_out_user_login_fails(self, driver, config):
        """Test that locked out user cannot login."""
        # Arrange
        login_page = SauceDemoLoginPage(driver, config.environment.base_url)
        login_page.navigate_to_login()

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            login_page.login_locked_out_user()

        assert "locked out" in str(exc_info.value).lower()

    def test_invalid_credentials_login_fails(self, driver, config):
        """Test that invalid credentials produce appropriate error message."""
        # Arrange
        login_page = SauceDemoLoginPage(driver, config.environment.base_url)
        login_page.navigate_to_login()

        # Act
        error_message = login_page.attempt_invalid_login("invalid_user", "invalid_pass")

        # Assert
        assert error_message
        assert "do not match" in error_message.lower()

    def test_empty_username_validation(self, driver, config):
        """Test validation when username is empty."""
        # Arrange
        login_page = SauceDemoLoginPage(driver, config.environment.base_url)
        login_page.navigate_to_login()

        # Act
        error_message = login_page.attempt_invalid_login("", "secret_sauce")

        # Assert
        assert error_message
        assert "username is required" in error_message.lower()

    def test_empty_password_validation(self, driver, config):
        """Test validation when password is empty."""
        # Arrange
        login_page = SauceDemoLoginPage(driver, config.environment.base_url)
        login_page.navigate_to_login()

        # Act
        error_message = login_page.attempt_invalid_login("standard_user", "")

        # Assert
        assert error_message
        assert "password is required" in error_message.lower()

    def test_login_page_elements_present(self, driver, config):
        """Test that all expected login page elements are present."""
        # Arrange
        login_page = SauceDemoLoginPage(driver, config.environment.base_url)
        login_page.navigate_to_login()

        # Act & Assert using soft assertions
        with SoftAssertions() as soft:
            soft.assert_true(
                login_page.verify_page_loaded(), "Login page should be loaded"
            )

            # Check individual elements
            username_field = login_page.get_text_input(login_page.USERNAME_FIELD)
            password_field = login_page.get_text_input(login_page.PASSWORD_FIELD)
            login_button = login_page.get_button(login_page.LOGIN_BUTTON)

            soft.assert_true(
                username_field.is_displayed, "Username field should be visible"
            )
            soft.assert_true(
                password_field.is_displayed, "Password field should be visible"
            )
            soft.assert_true(
                login_button.is_displayed, "Login button should be visible"
            )

            # Check placeholders/attributes
            soft.assert_equal(
                username_field.get_attribute("placeholder"),
                "Username",
                "Username placeholder should be correct",
            )
            soft.assert_equal(
                password_field.get_attribute("placeholder"),
                "Password",
                "Password placeholder should be correct",
            )

    def test_error_message_dismissal(self, driver, config):
        """Test that error messages can be dismissed."""
        # Arrange
        login_page = SauceDemoLoginPage(driver, config.environment.base_url)
        login_page.navigate_to_login()

        # Act
        # Generate an error first
        login_page.attempt_invalid_login("invalid", "invalid")
        assert login_page.is_error_displayed()

        # Dismiss the error
        login_page.close_error_message()

        # Assert
        assert not login_page.is_error_displayed()

    @pytest.mark.parametrize(
        "username,password,should_succeed",
        [
            ("standard_user", "secret_sauce", True),
            ("problem_user", "secret_sauce", True),
            ("performance_glitch_user", "secret_sauce", True),
            ("locked_out_user", "secret_sauce", False),
            ("invalid_user", "secret_sauce", False),
            ("standard_user", "wrong_password", False),
            ("", "secret_sauce", False),
            ("standard_user", "", False),
        ],
    )
    def test_login_scenarios(self, driver, config, username, password, should_succeed):
        """Parameterized test for various login scenarios."""
        # Arrange
        login_page = SauceDemoLoginPage(driver, config.environment.base_url)
        login_page.navigate_to_login()

        # Act & Assert
        if should_succeed:
            if username == "locked_out_user":
                # Special case for locked out user
                with pytest.raises(Exception):
                    login_page.login(username, password)
            else:
                inventory_page = login_page.login(username, password)
                assert inventory_page.verify_page_loaded()
                assert "inventory.html" in inventory_page.current_url
        else:
            if username == "locked_out_user":
                with pytest.raises(Exception):
                    login_page.login(username, password)
            else:
                error_message = login_page.attempt_invalid_login(username, password)
                assert error_message  # Should have an error message

    def test_available_usernames_list(self, driver, config):
        """Test that we can get the list of available usernames."""
        # Arrange
        login_page = SauceDemoLoginPage(driver, config.environment.base_url)
        login_page.navigate_to_login()

        # Act
        usernames = login_page.get_available_usernames()

        # Assert
        expected_usernames = [
            "standard_user",
            "locked_out_user",
            "problem_user",
            "performance_glitch_user",
        ]

        assert len(usernames) == len(expected_usernames)
        for username in expected_usernames:
            assert username in usernames
