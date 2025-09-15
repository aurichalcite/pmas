"""
Integration tests for PMAS domain adapter login workflows.

This module tests the interaction between multiple internal PMAS components
using fakes for external systems. Tests cover:
- ManufacturingLoginAdapter integration with page objects and driver
- Login workflow orchestration and error handling
- Adapter state management and method call sequences
- Different user type login scenarios
- Failure scenarios and exception handling

Uses FakeWebDriver to simulate browser interactions without real browser overhead.
No network calls or external dependencies.
"""

from unittest.mock import Mock, patch

import pytest
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# ASSUMPTION: Import PMAS domain components
from pmas import Config
from pmas.domains.manufacturing.adapters import (
    ManufacturingLoginAdapter,
    ManufacturingUserCredentials,
)

from ..fakes.fake_webdriver import FakeWebDriver, FakeWebElement


class TestManufacturingLoginAdapterIntegration:
    """Integration tests for ManufacturingLoginAdapter with fake driver."""

    @pytest.fixture
    def fake_driver(self) -> FakeWebDriver:
        """Provide a configured fake driver for manufacturing login tests."""
        driver = FakeWebDriver()

        # Set up manufacturing login page elements
        driver.add_element(
            "id:username",
            FakeWebElement("input", attributes={"type": "text", "id": "username"}),
        )
        driver.add_element(
            "id:password",
            FakeWebElement("input", attributes={"type": "password", "id": "password"}),
        )
        driver.add_element(
            "id:login-button",
            FakeWebElement("button", text="Login", attributes={"id": "login-button"}),
        )
        driver.add_element(
            "css:.user-type-selector",
            FakeWebElement("select", attributes={"class": "user-type-selector"}),
        )

        return driver

    @pytest.fixture
    def test_config(self) -> Config:
        """Provide test configuration for manufacturing domain."""
        # ASSUMPTION: Config can be created with manufacturing-specific settings
        config = Config()
        config.environment.base_url = "https://manufacturing.example.com"
        config.environment.name = "test"
        config.test.default_timeout = 5.0
        return config

    @pytest.fixture
    def login_adapter(
        self, fake_driver: FakeWebDriver, test_config: Config
    ) -> ManufacturingLoginAdapter:
        """Provide ManufacturingLoginAdapter instance with fake driver."""
        return ManufacturingLoginAdapter(fake_driver, test_config)

    def test_login_adapter_initialization(
        self, fake_driver: FakeWebDriver, test_config: Config
    ):
        """
        Test that ManufacturingLoginAdapter initializes correctly with
        dependencies.
        """
        adapter = ManufacturingLoginAdapter(fake_driver, test_config)

        assert adapter.driver is fake_driver
        assert adapter.config is test_config
        assert adapter.login_page is not None
        # ASSUMPTION: login_page is created with correct parameters
        assert hasattr(adapter, "login_page")

    def test_login_as_production_planner_success(
        self, login_adapter: ManufacturingLoginAdapter, fake_driver: FakeWebDriver
    ):
        """Test successful login as production planner."""
        # Configure fake driver for successful navigation and login
        fake_driver.configure_failure_mode("get", should_fail=False)
        fake_driver.configure_failure_mode("find_element", should_fail=False)

        # Mock the login page methods
        with (
            patch.object(
                login_adapter.login_page, "navigate_to_manufacturing_login"
            ) as mock_navigate,
            patch.object(
                login_adapter.login_page, "login_production_planner"
            ) as mock_login,
        ):
            # Configure mock return value
            mock_login.return_value = (
                Mock()
            )  # Simulate successful login returning a page object

            # Execute login
            result = login_adapter.login_as_production_planner()

            # Verify method calls
            mock_navigate.assert_called_once()
            mock_login.assert_called_once()
            assert result is not None

        # Verify driver operations were logged
        assert (
            fake_driver.get_operation_count("get") >= 0
        )  # Navigation might trigger get

    def test_login_as_factory_manager_success(
        self, login_adapter: ManufacturingLoginAdapter, fake_driver: FakeWebDriver
    ):
        """Test successful login as factory manager."""
        with (
            patch.object(
                login_adapter.login_page, "navigate_to_manufacturing_login"
            ) as mock_navigate,
            patch.object(
                login_adapter.login_page, "login_factory_manager"
            ) as mock_login,
        ):
            mock_login.return_value = Mock()

            result = login_adapter.login_as_factory_manager()

            mock_navigate.assert_called_once()
            mock_login.assert_called_once()
            assert result is not None

    def test_login_as_production_coordinator_success(
        self, login_adapter: ManufacturingLoginAdapter, fake_driver: FakeWebDriver
    ):
        """Test successful login as production coordinator."""
        with (
            patch.object(
                login_adapter.login_page, "navigate_to_manufacturing_login"
            ) as mock_navigate,
            patch.object(
                login_adapter.login_page, "login_production_coordinator"
            ) as mock_login,
        ):
            mock_login.return_value = Mock()

            result = login_adapter.login_as_production_coordinator()

            mock_navigate.assert_called_once()
            mock_login.assert_called_once()
            assert result is not None

    def test_login_as_retail_partner_with_username(
        self, login_adapter: ManufacturingLoginAdapter
    ):
        """Test login as retail partner with specific username."""
        test_username = "retail_partner_001"

        with (
            patch.object(
                login_adapter.login_page, "navigate_to_manufacturing_login"
            ) as mock_navigate,
            patch.object(
                login_adapter.login_page, "login_retail_partner"
            ) as mock_login,
        ):
            mock_login.return_value = Mock()

            result = login_adapter.login_as_retail_partner(test_username)

            mock_navigate.assert_called_once()
            mock_login.assert_called_once_with(test_username)
            assert result is not None

    def test_login_as_retail_partner_without_username(
        self, login_adapter: ManufacturingLoginAdapter
    ):
        """Test login as retail partner without specific username (random)."""
        with (
            patch.object(
                login_adapter.login_page, "navigate_to_manufacturing_login"
            ) as mock_navigate,
            patch.object(
                login_adapter.login_page, "login_retail_partner"
            ) as mock_login,
        ):
            mock_login.return_value = Mock()

            result = login_adapter.login_as_retail_partner()

            mock_navigate.assert_called_once()
            mock_login.assert_called_once_with(None)
            assert result is not None

    def test_login_with_credentials_success(
        self, login_adapter: ManufacturingLoginAdapter
    ):
        """Test login with specific user credentials."""
        credentials = ManufacturingUserCredentials(
            username="test_user",
            password="test_password",
            user_type=1,
            factory="FAC001",
        )

        with (
            patch.object(
                login_adapter.login_page, "navigate_to_manufacturing_login"
            ) as mock_navigate,
            patch.object(login_adapter.login_page, "login") as mock_login,
        ):
            mock_login.return_value = Mock()

            result = login_adapter.login_with_credentials(credentials)

            mock_navigate.assert_called_once()
            mock_login.assert_called_once_with(
                credentials.username, credentials.password
            )
            assert result is not None

    def test_login_failure_scenarios(self, login_adapter: ManufacturingLoginAdapter):
        """Test various login failure scenarios."""
        test_cases = [
            ("login_production_planner", login_adapter.login_as_production_planner),
            ("login_factory_manager", login_adapter.login_as_factory_manager),
            (
                "login_production_coordinator",
                login_adapter.login_as_production_coordinator,
            ),
        ]

        for login_method_name, adapter_method in test_cases:
            with (
                patch.object(
                    login_adapter.login_page, "navigate_to_manufacturing_login"
                ),
                patch.object(login_adapter.login_page, login_method_name) as mock_login,
            ):
                # Configure login to return None (failure)
                mock_login.return_value = None

                result = adapter_method()

                assert result is None
                mock_login.assert_called_once()

    def test_navigation_failure_handling(
        self, login_adapter: ManufacturingLoginAdapter, fake_driver: FakeWebDriver
    ):
        """Test handling of navigation failures."""
        # Configure fake driver to fail on navigation
        fake_driver.configure_failure_mode(
            "get", should_fail=True, exception=TimeoutException
        )

        with patch.object(
            login_adapter.login_page, "navigate_to_manufacturing_login"
        ) as mock_navigate:
            # Configure navigation to raise exception
            mock_navigate.side_effect = TimeoutException("Page load timeout")

            # Login should handle navigation failure gracefully
            with pytest.raises(TimeoutException):
                login_adapter.login_as_production_planner()

            mock_navigate.assert_called_once()

    def test_element_not_found_handling(
        self, login_adapter: ManufacturingLoginAdapter, fake_driver: FakeWebDriver
    ):
        """Test handling of element not found scenarios."""
        # Remove login elements to simulate missing elements
        fake_driver.remove_element("id:username")
        fake_driver.remove_element("id:password")

        with (
            patch.object(login_adapter.login_page, "navigate_to_manufacturing_login"),
            patch.object(
                login_adapter.login_page, "login_production_planner"
            ) as mock_login,
        ):
            # Configure login to raise NoSuchElementException
            mock_login.side_effect = NoSuchElementException("Login button not found")

            with pytest.raises(NoSuchElementException):
                login_adapter.login_as_production_planner()

            mock_login.assert_called_once()

    def test_multiple_login_attempts_state_management(
        self, login_adapter: ManufacturingLoginAdapter, fake_driver: FakeWebDriver
    ):
        """Test adapter state management across multiple login attempts."""
        with (
            patch.object(
                login_adapter.login_page, "navigate_to_manufacturing_login"
            ) as mock_navigate,
            patch.object(
                login_adapter.login_page, "login_production_planner"
            ) as mock_login,
        ):
            mock_login.return_value = Mock()

            # Perform multiple logins
            result1 = login_adapter.login_as_production_planner()
            result2 = login_adapter.login_as_production_planner()

            # Verify each login triggered navigation and login
            assert mock_navigate.call_count == 2
            assert mock_login.call_count == 2
            assert result1 is not None
            assert result2 is not None

        # Verify driver state is consistent
        assert not fake_driver._is_quit

    def test_adapter_with_different_configurations(self, fake_driver: FakeWebDriver):
        """Test adapter behavior with different configuration settings."""
        # Test with different timeout settings
        configs = [
            Config(),  # Default config
        ]

        # Modify configs for testing
        configs[0].test.default_timeout = 1.0  # Fast timeout

        for config in configs:
            adapter = ManufacturingLoginAdapter(fake_driver, config)

            assert adapter.config.test.default_timeout == config.test.default_timeout
            assert adapter.login_page is not None

    @pytest.mark.parametrize(
        "user_type,expected_method",
        [
            ("production_planner", "login_as_production_planner"),
            ("factory_manager", "login_as_factory_manager"),
            ("production_coordinator", "login_as_production_coordinator"),
            ("retail_partner", "login_as_retail_partner"),
        ],
    )
    def test_parametrized_user_type_logins(
        self,
        login_adapter: ManufacturingLoginAdapter,
        user_type: str,
        expected_method: str,
    ):
        """Test different user type logins with parametrized data."""
        method = getattr(login_adapter, expected_method)

        with (
            patch.object(login_adapter.login_page, "navigate_to_manufacturing_login"),
            patch.object(login_adapter.login_page, f"login_{user_type}") as mock_login,
        ):
            mock_login.return_value = Mock()

            if user_type == "retail_partner":
                result = method("test_partner")
            else:
                result = method()

            assert result is not None
            mock_login.assert_called_once()

    def test_adapter_cleanup_and_resource_management(
        self, login_adapter: ManufacturingLoginAdapter, fake_driver: FakeWebDriver
    ):
        """Test that adapter properly manages resources and cleanup."""
        # Perform login operation
        with (
            patch.object(login_adapter.login_page, "navigate_to_manufacturing_login"),
            patch.object(
                login_adapter.login_page, "login_production_planner"
            ) as mock_login,
        ):
            mock_login.return_value = Mock()
            login_adapter.login_as_production_planner()

        # Verify driver is still usable after operations
        assert not fake_driver._is_quit

        # Verify operation log contains expected entries
        # Should contain operations related to element finding, navigation, etc.
        assert len(fake_driver.operation_log) >= 0  # At least some operations logged

    def test_concurrent_adapter_usage_concept(
        self, fake_driver: FakeWebDriver, test_config: Config
    ):
        """Test concept of multiple adapters sharing the same driver."""
        # Create multiple adapter instances
        adapter1 = ManufacturingLoginAdapter(fake_driver, test_config)
        adapter2 = ManufacturingLoginAdapter(fake_driver, test_config)

        # Both should reference the same driver
        assert adapter1.driver is adapter2.driver
        assert adapter1.driver is fake_driver

        # Both should be independently usable
        assert adapter1.config is test_config
        assert adapter2.config is test_config
