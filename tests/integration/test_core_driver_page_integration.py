"""
Integration tests for PMAS core driver and page object interactions.

This module tests the interaction between DriverFactory, BasePage, and element
components using FakeWebDriver. Tests cover:
- Driver creation and page object initialization
- Element finding and interaction workflows
- Page navigation and state management
- Error handling across component boundaries
- Configuration integration with core components

Uses FakeWebDriver to simulate browser interactions without real browser overhead.
No network calls or external dependencies.
"""

from unittest.mock import patch

import pytest
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from pmas import Config, DriverFactory
from pmas.core.errors import ConfigurationError, ElementNotFoundError
from pmas.core.locators import by_id
from pmas.core.page import BasePage

from ..fakes.fake_webdriver import FakeWebDriver, FakeWebElement


class IntegrationTestPage(BasePage):
    """Concrete test page implementation for integration testing."""

    def __init__(self, driver, base_url="http://test.example.com", timeout=5.0):
        super().__init__(driver, base_url, timeout)
        self.url_path = "/test-page"

    def verify_page_loaded(self) -> bool:
        """Verify the test page is loaded."""
        return self.is_element_present(by_id("test-page-marker"))


@pytest.mark.integration
class TestCoreDriverPageIntegration:
    """Integration tests for driver and page object interactions."""

    @pytest.fixture
    def fake_driver(self) -> FakeWebDriver:
        """Provide a configured fake driver for integration tests."""
        driver = FakeWebDriver()

        # Set up test page elements
        driver.add_element(
            "id:test-page-marker",
            FakeWebElement("div", attributes={"id": "test-page-marker"}),
        )
        driver.add_element(
            "id:submit-button",
            FakeWebElement("button", text="Submit", attributes={"id": "submit-button"}),
        )
        driver.add_element(
            "id:username-input",
            FakeWebElement(
                "input", attributes={"type": "text", "id": "username-input"}
            ),
        )
        driver.add_element(
            "css:.error-message",
            FakeWebElement(
                "div", text="Error occurred", attributes={"class": "error-message"}
            ),
        )

        return driver

    @pytest.fixture
    def test_config(self) -> Config:
        """Provide test configuration for integration tests."""
        config = Config()
        config.environment.base_url = "http://test.example.com"
        config.environment.name = "integration_test"
        config.test.default_timeout = 5.0
        config.browser.name = "chrome"
        config.browser.headless = True
        return config

    def test_driver_factory_page_initialization_integration(
        self, fake_driver: FakeWebDriver, test_config: Config
    ):
        """Test integration between DriverFactory and page object initialization."""
        # Mock DriverFactory to return our fake driver
        with patch.object(DriverFactory, "create_driver", return_value=fake_driver):
            # Create driver through factory
            driver = DriverFactory.create_driver(
                browser=test_config.browser.name, headless=test_config.browser.headless
            )

            # Initialize page object with factory-created driver
            page = IntegrationTestPage(
                driver,
                test_config.environment.base_url,
                test_config.test.default_timeout,
            )

            # Verify integration
            assert page.driver is driver
            assert page.base_url == test_config.environment.base_url
            assert page.timeout == test_config.test.default_timeout
            assert page.url == "http://test.example.com/test-page"

    def test_page_navigation_and_element_interaction_workflow(
        self, fake_driver: FakeWebDriver
    ):
        """Test complete workflow of page navigation and element interactions."""
        page = IntegrationTestPage(fake_driver)

        # Test navigation
        page.navigate_to()

        # Verify navigation occurred
        assert fake_driver.current_url == page.url

        # Test element interactions
        submit_button = page.get_button(by_id("submit-button"))
        username_input = page.get_text_input(by_id("username-input"))

        # Perform interactions
        username_input.type_text("test_user")
        submit_button.click()

        # Verify interactions were logged
        operations = [op["operation"] for op in fake_driver.operation_log]
        assert "get" in operations  # Navigation
        assert "find_element" in operations  # Element finding

        # Verify element states
        username_element = fake_driver._elements_registry["id:username-input"]
        submit_element = fake_driver._elements_registry["id:submit-button"]
        assert username_element._text_input == "test_user"
        assert submit_element._click_count == 1

    def test_page_verification_and_error_handling_integration(
        self, fake_driver: FakeWebDriver
    ):
        """Test page verification and error handling across components."""
        page = IntegrationTestPage(fake_driver)

        # Test successful page verification
        page.navigate_to()
        assert page.verify_page_loaded() is True

        # Test error handling when element not found
        fake_driver.remove_element("id:test-page-marker")
        assert page.verify_page_loaded() is False

        # Test element not found error propagation
        with pytest.raises(ElementNotFoundError):
            button = page.get_button(by_id("nonexistent-button"))
            button.click()  # This should trigger the error

    def test_configuration_integration_across_components(
        self, fake_driver: FakeWebDriver, test_config: Config
    ):
        """
        Test configuration integration across driver, page, and element
        components.
        """
        page = IntegrationTestPage(
            fake_driver,
            test_config.environment.base_url,
            test_config.test.default_timeout,
        )

        # Test timeout configuration propagation
        button = page.get_button(by_id("submit-button"))
        assert button.timeout == test_config.test.default_timeout

        # Test base URL configuration
        assert page.base_url == test_config.environment.base_url
        assert test_config.environment.base_url in page.url

    def test_element_state_management_across_interactions(
        self, fake_driver: FakeWebDriver
    ):
        """Test element state management across multiple interactions."""
        page = IntegrationTestPage(fake_driver)
        page.navigate_to()

        # Get same element multiple times
        button1 = page.get_button(by_id("submit-button"))
        button2 = page.get_button(by_id("submit-button"))

        # Interact with both references
        button1.click()
        button2.click()

        # Verify state is consistent
        element = fake_driver._elements_registry["id:submit-button"]
        assert element._click_count == 2

    def test_error_propagation_across_component_boundaries(
        self, fake_driver: FakeWebDriver
    ):
        """Test error propagation from driver through page to elements."""
        page = IntegrationTestPage(fake_driver)

        # Configure driver to fail on element finding
        fake_driver.configure_failure_mode(
            "find_element", should_fail=True, exception=NoSuchElementException
        )

        # Test error propagation through page to element
        with pytest.raises(ElementNotFoundError):
            button = page.get_button(by_id("submit-button"))
            button.click()  # This should trigger the error

        # Test timeout error propagation
        fake_driver.configure_failure_mode(
            "find_element", should_fail=True, exception=TimeoutException
        )

        with pytest.raises(ElementNotFoundError):
            text_input = page.get_text_input(by_id("username-input"))
            # This should trigger the error
            text_input.type_text("test")

    def test_multiple_page_objects_sharing_driver(self, fake_driver: FakeWebDriver):
        """Test multiple page objects sharing the same driver instance."""
        page1 = IntegrationTestPage(fake_driver, base_url="http://test1.example.com")
        page2 = IntegrationTestPage(fake_driver, base_url="http://test2.example.com")

        # Both pages should share the same driver
        assert page1.driver is page2.driver
        assert page1.driver is fake_driver

        # Navigation should update shared driver state
        page1.navigate_to()
        assert fake_driver.current_url == page1.url

        page2.navigate_to()
        assert fake_driver.current_url == page2.url

        # Verify operation log contains both navigations
        get_operations = [
            op for op in fake_driver.operation_log if op["operation"] == "get"
        ]
        assert len(get_operations) >= 2

    def test_driver_configuration_error_handling(self, fake_driver: FakeWebDriver):
        """Test driver configuration error handling in integration context."""
        # Test invalid configuration handling
        with pytest.raises(ConfigurationError):
            DriverFactory.create_driver(browser="invalid_browser")

        # Test page initialization with edge case parameters (should work)
        page = IntegrationTestPage(fake_driver, base_url="", timeout=-1)
        assert page.base_url == ""
        assert page.timeout == -1

    def test_concurrent_element_operations(self, fake_driver: FakeWebDriver):
        """Test concurrent element operations on the same page."""
        page = IntegrationTestPage(fake_driver)
        page.navigate_to()

        # Get multiple elements
        button = page.get_button(by_id("submit-button"))
        text_input = page.get_text_input(by_id("username-input"))

        # Perform concurrent operations
        text_input.type_text("user1")
        button.click()
        text_input.clear()
        text_input.type_text("user2")
        button.click()

        # Verify final states
        username_element = fake_driver._elements_registry["id:username-input"]
        submit_element = fake_driver._elements_registry["id:submit-button"]

        assert username_element._text_input == "user2"
        assert submit_element._click_count == 2
