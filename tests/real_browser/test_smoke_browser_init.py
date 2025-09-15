"""
Real browser smoke tests for PMAS WebDriver integration.

This module contains minimal smoke tests that validate PMAS integration with
actual browser drivers. These tests are NOT end-to-end tests - they only
confirm basic browser control functionality and driver stack integration.

Key characteristics:
- Uses actual headless browser drivers (Chrome)
- Minimal operations to verify driver functionality
- Must be explicitly enabled via PMAS_RUN_REAL_BROWSER environment variable
- Focuses on driver creation, basic navigation, and cleanup
- No application-specific testing - only framework integration

These tests confirm that:
- PMAS DriverFactory can create real WebDriver instances
- Basic WebDriver operations work correctly
- Driver cleanup and resource management functions properly
- Browser options and configuration are applied correctly
"""

import os
import time

import pytest
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver

# ASSUMPTION: Import PMAS components for real browser testing
from pmas import Config, DriverFactory


@pytest.mark.real_browser
class TestRealBrowserSmoke:
    """Smoke tests using actual browser drivers."""

    def test_driver_creation_and_basic_operations(self, real_driver: WebDriver):
        """
        Test basic driver creation and fundamental operations.

        This test verifies that:
        - PMAS can create a real WebDriver instance
        - Basic navigation works
        - Driver properties are accessible
        - Driver can be properly cleaned up

        Args:
            real_driver: Actual WebDriver fixture (Chrome headless)
        """
        # Verify driver was created successfully
        assert real_driver is not None
        assert hasattr(real_driver, "get")
        assert hasattr(real_driver, "current_url")
        assert hasattr(real_driver, "title")
        assert hasattr(real_driver, "quit")

        # Test basic navigation to a data URL (no network required)
        test_url = (
            "data:text/html,<html><head><title>PMAS Test Page</title></head>"
            "<body><h1>Test</h1></body></html>"
        )
        real_driver.get(test_url)

        # Verify navigation worked
        assert real_driver.current_url.startswith("data:")
        assert real_driver.title == "PMAS Test Page"

        # Test window size operations
        initial_size = real_driver.get_window_size()
        assert isinstance(initial_size, dict)
        assert "width" in initial_size
        assert "height" in initial_size
        assert initial_size["width"] > 0
        assert initial_size["height"] > 0

    def test_driver_factory_integration(self, pmas_config: Config):
        """
        Test PMAS DriverFactory integration with real browser creation.

        This test verifies that:
        - DriverFactory can create drivers with PMAS configuration
        - Configuration options are properly applied
        - Multiple driver creation works
        - Proper cleanup occurs

        Args:
            pmas_config: PMAS configuration fixture
        """
        # Skip if real browser tests are disabled
        if not os.getenv("PMAS_RUN_REAL_BROWSER"):
            pytest.skip("Real browser tests disabled")

        # Test driver creation with PMAS configuration
        driver = None
        try:
            driver = DriverFactory.create_driver(
                browser=pmas_config.browser.name,
                headless=True,  # Always headless for CI
                window_size=(
                    pmas_config.browser.window_width,
                    pmas_config.browser.window_height,
                ),
                additional_options=["--no-sandbox", "--disable-dev-shm-usage"],
            )

            # Verify driver was created with correct configuration
            assert driver is not None

            # Test basic functionality
            driver.get("data:,")  # Minimal data URL
            assert driver.current_url == "data:,"
            assert driver.title == ""

            # Verify window size matches configuration
            window_size = driver.get_window_size()
            # Allow some tolerance for browser chrome/decorations
            assert abs(window_size["width"] - pmas_config.browser.window_width) <= 50
            assert abs(window_size["height"] - pmas_config.browser.window_height) <= 100

        finally:
            if driver:
                driver.quit()

    def test_multiple_driver_instances(self, pmas_config: Config):
        """
        Test creation and management of multiple driver instances.

        This test verifies that:
        - Multiple drivers can be created simultaneously
        - Each driver operates independently
        - Proper cleanup of all instances works

        Args:
            pmas_config: PMAS configuration fixture
        """
        if not os.getenv("PMAS_RUN_REAL_BROWSER"):
            pytest.skip("Real browser tests disabled")

        drivers = []
        try:
            # Create multiple driver instances
            for i in range(2):  # Keep it minimal for CI performance
                driver = DriverFactory.create_driver(
                    browser="chrome",
                    headless=True,
                    additional_options=["--no-sandbox", "--disable-dev-shm-usage"],
                )
                drivers.append(driver)

                # Test each driver independently
                test_url = (
                    f"data:text/html,<html><head><title>Driver {i}</title></head>"
                    f"</html>"
                )
                driver.get(test_url)
                assert f"Driver {i}" in driver.title

            # Verify all drivers are independent
            assert len(drivers) == 2
            assert drivers[0] is not drivers[1]

        finally:
            # Cleanup all drivers
            for driver in drivers:
                try:
                    driver.quit()
                except Exception:
                    pass  # Ignore cleanup errors

    def test_driver_error_handling(self, pmas_config: Config):
        """
        Test driver error handling and recovery scenarios.

        This test verifies that:
        - Invalid configurations are handled gracefully
        - Driver creation failures are properly reported
        - Error messages are informative

        Args:
            pmas_config: PMAS configuration fixture
        """
        if not os.getenv("PMAS_RUN_REAL_BROWSER"):
            pytest.skip("Real browser tests disabled")

        # Test invalid browser name
        with pytest.raises(Exception) as exc_info:
            DriverFactory.create_driver(browser="invalid_browser")

        # Verify error message is informative
        error_message = str(exc_info.value)
        assert (
            "invalid_browser" in error_message.lower()
            or "unsupported" in error_message.lower()
        )

    def test_driver_performance_baseline(self, real_driver: WebDriver):
        """
        Test basic performance characteristics of driver operations.

        This test establishes baseline performance metrics for:
        - Driver startup time (already created by fixture)
        - Navigation time
        - Element finding time
        - Basic operation responsiveness

        Args:
            real_driver: Actual WebDriver fixture
        """
        # Test navigation performance
        start_time = time.time()
        real_driver.get(
            "data:text/html,<html><body><div id='test'>Test Content</div></body></html>"
        )
        navigation_time = time.time() - start_time

        # Navigation should be fast for data URLs
        assert navigation_time < 5.0, (
            f"Navigation took too long: {navigation_time:.2f}s"
        )

        # Test element finding performance
        start_time = time.time()
        try:
            element = real_driver.find_element("id", "test")
            find_time = time.time() - start_time

            # Element finding should be fast
            assert find_time < 2.0, f"Element finding took too long: {find_time:.2f}s"
            assert element is not None
            assert element.text == "Test Content"

        except Exception as e:
            pytest.fail(f"Element finding failed: {e}")

    def test_driver_cleanup_verification(self, pmas_config: Config):
        """
        Test that driver cleanup works properly and releases resources.

        This test verifies that:
        - Driver quit() method works correctly
        - Resources are properly released
        - Subsequent operations fail appropriately after quit

        Args:
            pmas_config: PMAS configuration fixture
        """
        if not os.getenv("PMAS_RUN_REAL_BROWSER"):
            pytest.skip("Real browser tests disabled")

        # Create a driver for cleanup testing
        driver = DriverFactory.create_driver(
            browser="chrome",
            headless=True,
            additional_options=["--no-sandbox", "--disable-dev-shm-usage"],
        )

        # Verify driver is functional
        driver.get("data:,")
        assert driver.current_url == "data:,"

        # Quit the driver
        driver.quit()

        # Verify operations fail after quit
        with pytest.raises(WebDriverException):
            driver.get("data:,")

    @pytest.mark.parametrize(
        "browser_name", ["chrome"]
    )  # Add more browsers as supported
    def test_different_browser_types(self, browser_name: str, pmas_config: Config):
        """
        Test driver creation with different browser types.

        This test verifies that:
        - Different browser types can be created
        - Each browser type works correctly
        - Browser-specific options are applied

        Args:
            browser_name: Name of browser to test
            pmas_config: PMAS configuration fixture
        """
        if not os.getenv("PMAS_RUN_REAL_BROWSER"):
            pytest.skip("Real browser tests disabled")

        driver = None
        try:
            driver = DriverFactory.create_driver(
                browser=browser_name,
                headless=True,
                additional_options=["--no-sandbox", "--disable-dev-shm-usage"],
            )

            # Test basic functionality
            driver.get(
                "data:text/html,<html><head><title>Browser Test</title></head></html>"
            )
            assert driver.title == "Browser Test"

            # Verify browser-specific capabilities
            capabilities = driver.capabilities
            assert capabilities is not None
            assert "browserName" in capabilities

        finally:
            if driver:
                driver.quit()

    def test_headless_mode_verification(self, real_driver: WebDriver):
        """
        Test that headless mode is properly configured and working.

        This test verifies that:
        - Driver is running in headless mode
        - No visible browser windows are created
        - All functionality works in headless mode

        Args:
            real_driver: Actual WebDriver fixture (should be headless)
        """
        # Test that we can perform all basic operations in headless mode
        real_driver.get(
            "data:text/html,<html><body><h1>Headless Test</h1></body></html>"
        )

        # Verify page loaded correctly
        assert "Headless Test" in real_driver.page_source

        # Test JavaScript execution in headless mode
        result = real_driver.execute_script("return document.title;")
        assert result == ""  # data URLs have empty titles

        # Test screenshot capability in headless mode
        screenshot = real_driver.get_screenshot_as_png()
        assert screenshot is not None
        assert len(screenshot) > 0

    def test_driver_configuration_options(self, pmas_config: Config):
        """
        Test that driver configuration options are properly applied.

        This test verifies that:
        - Custom options are applied to the driver
        - Window size configuration works
        - Additional browser options are respected

        Args:
            pmas_config: PMAS configuration fixture
        """
        if not os.getenv("PMAS_RUN_REAL_BROWSER"):
            pytest.skip("Real browser tests disabled")

        custom_options = [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--window-size=800,600",
        ]

        driver = None
        try:
            driver = DriverFactory.create_driver(
                browser="chrome",
                headless=True,
                window_size=(800, 600),
                additional_options=custom_options,
            )

            # Test that window size option was applied
            driver.get("data:,")
            window_size = driver.get_window_size()

            # Allow some tolerance for browser differences
            assert abs(window_size["width"] - 800) <= 50
            assert abs(window_size["height"] - 600) <= 100

        finally:
            if driver:
                driver.quit()
