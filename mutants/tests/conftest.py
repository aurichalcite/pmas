"""
Shared pytest fixtures and configuration for PMAS test suite.

This module provides core fixtures used across all test layers:
- pmas_config: Test-friendly configuration instances
- fake_driver: Fast fake WebDriver for unit/integration tests
- real_driver: Actual Selenium WebDriver for smoke tests
- artifacts_dir: Temporary directory for test artifacts
"""

import os
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest
from pmas.config.model import BrowserConfig, EnvironmentConfig, TestConfig
from selenium import webdriver

# ASSUMPTION: Import PMAS components - these imports reflect the actual PMAS API
from pmas import Config, DriverFactory

from .fakes.fake_webdriver import FakeWebDriver


@pytest.fixture(scope="function")
def pmas_config() -> Config:
    """
    Function-scoped fixture providing a test-friendly PMAS Config instance.

    Returns a Config with safe defaults suitable for testing:
    - Fast timeouts to speed up test execution
    - Headless browser configuration
    - Test-specific base URL
    - Disabled screenshot capture for unit tests

    Returns:
        Config: Test-optimized PMAS configuration
    """
    # ASSUMPTION: Config can be constructed with individual component configs
    return Config(
        browser=BrowserConfig(
            name="chrome",
            headless=True,
            window_width=1280,
            window_height=720,
            additional_options=["--no-sandbox", "--disable-dev-shm-usage"],
        ),
        environment=EnvironmentConfig(base_url="http://localhost:8080", name="test"),
        test=TestConfig(
            default_timeout=5.0,  # Fast timeouts for tests
            retry_attempts=1,  # Minimal retries in tests
            retry_delay=0.1,  # Fast retry delay
            take_screenshot_on_failure=False,  # Disable for unit tests
            capture_logs_on_failure=True,
            parallel_execution=False,
        ),
    )


@pytest.fixture(scope="session")
def fake_driver() -> Generator[FakeWebDriver, None, None]:
    """
    Session-scoped fixture providing a FakeWebDriver instance for fast testing.

    This fixture provides a mock WebDriver that implements the WebDriverProtocol
    interface without actually launching a browser. Perfect for unit and integration
    tests that need to verify WebDriver interactions without the overhead.

    Yields:
        FakeWebDriver: Mock WebDriver instance for testing
    """
    driver = FakeWebDriver()
    try:
        yield driver
    finally:
        # Cleanup any state in the fake driver
        driver.quit()


@pytest.fixture(scope="function")
def real_driver(pmas_config: Config) -> Generator[webdriver.Chrome, None, None]:
    """
    Function-scoped fixture providing actual Selenium WebDriver for smoke tests.

    This fixture creates a real Chrome WebDriver instance in headless mode.
    It automatically skips tests when the PMAS_RUN_REAL_BROWSER environment
    variable is not set, ensuring real browser tests are opt-in only.

    Args:
        pmas_config: PMAS configuration fixture

    Yields:
        webdriver.Chrome: Actual Chrome WebDriver instance

    Raises:
        pytest.skip: When PMAS_RUN_REAL_BROWSER environment variable is not set
    """
    # Skip real browser tests unless explicitly enabled
    if not os.getenv("PMAS_RUN_REAL_BROWSER"):
        pytest.skip(
            "Real browser tests disabled. Set PMAS_RUN_REAL_BROWSER=1 to enable."
        )

    # ASSUMPTION: DriverFactory.create_driver accepts browser config parameters
    try:
        driver = DriverFactory.create_driver(
            browser=pmas_config.browser.name,
            headless=True,  # Always headless for CI/automated testing
            window_size=(
                pmas_config.browser.window_width,
                pmas_config.browser.window_height,
            ),
            additional_options=pmas_config.browser.additional_options,
        )
        yield driver
    finally:
        if "driver" in locals():
            driver.quit()


@pytest.fixture(scope="function")
def artifacts_dir() -> Generator[Path, None, None]:
    """
    Function-scoped fixture providing a temporary directory for test artifacts.

    Creates a temporary directory that can be used for storing test artifacts
    like screenshots, logs, or temporary files. The directory is automatically
    cleaned up after the test completes.

    Yields:
        Path: Path to temporary directory for test artifacts
    """
    with tempfile.TemporaryDirectory(prefix="pmas_test_") as temp_dir:
        yield Path(temp_dir)


# Pytest hooks for test execution control


def pytest_configure(config):
    """Configure pytest with PMAS-specific settings."""
    # Add custom markers if not already defined
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add automatic markers based on test location."""
    import pytest

    for item in items:
        # Auto-mark tests based on their location
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "real_browser" in str(item.fspath):
            item.add_marker(pytest.mark.real_browser)


def pytest_runtest_setup(item):
    """Setup hook called before each test runs."""
    # Skip real_browser tests if environment variable not set
    if item.get_closest_marker("real_browser"):
        if not os.getenv("PMAS_RUN_REAL_BROWSER"):
            pytest.skip("Real browser tests require PMAS_RUN_REAL_BROWSER=1")


# Custom pytest markers for test categorization
pytestmark = [
    pytest.mark.filterwarnings("ignore:.*:DeprecationWarning"),
    pytest.mark.filterwarnings("ignore:.*:PendingDeprecationWarning"),
]
