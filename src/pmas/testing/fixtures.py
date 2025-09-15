"""
Core pytest fixtures for the PMAS testing framework.
"""

import logging
from collections.abc import Generator
from pathlib import Path

import pytest

from ..config.loader import load_config
from ..config.model import Config
from ..core.driver import DriverFactory, WebDriverProtocol
from ..core.errors import DriverError
from .reporting import capture_failure_artifacts

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def config() -> Config:
    """
    Session-scoped configuration fixture.
    Loads configuration from all sources with proper precedence.
    """
    try:
        # Load configuration from environment, CLI args, and config files
        config = load_config()
        logger.info(f"Configuration loaded for environment: {config.environment.name}")
        return config
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        raise


@pytest.fixture(scope="function")
def driver(
    config: Config, request: pytest.FixtureRequest
) -> Generator[WebDriverProtocol, None, None]:
    """
    Function-scoped WebDriver fixture.
    Creates a new driver instance for each test and handles cleanup.
    """
    driver_instance = None

    try:
        # Create driver with configuration
        driver_instance = DriverFactory.create_driver(
            browser=config.browser.name,
            headless=config.browser.headless,
            remote_url=config.webdriver.remote_url,
            window_size=config.window_size,
            download_dir=config.browser.download_dir,
            additional_options=config.browser.additional_options,
        )

        # Configure timeouts
        driver_instance.set_page_load_timeout(config.webdriver.page_load_timeout)
        driver_instance.set_script_timeout(config.webdriver.script_timeout)

        logger.info(
            f"Created WebDriver: {config.browser.name} "
            f"({'headless' if config.browser.headless else 'headed'})"
        )

        yield driver_instance

    except Exception as e:
        logger.error(f"Failed to create WebDriver: {e}")
        raise DriverError(f"WebDriver creation failed: {e}") from e

    finally:
        # Cleanup: capture artifacts on failure and quit driver
        if driver_instance:
            try:
                # Check if test failed and capture artifacts
                if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
                    capture_failure_artifacts(driver_instance, config, request)

                driver_instance.quit()
                logger.debug("WebDriver quit successfully")

            except Exception as e:
                logger.warning(f"Error during WebDriver cleanup: {e}")


@pytest.fixture(scope="function")
def base_url(config: Config) -> str:
    """Fixture providing the base URL for the application."""
    if not config.environment.base_url:
        pytest.skip("No base URL configured for current environment")
    return config.environment.base_url


@pytest.fixture(scope="function")
def api_base_url(config: Config) -> str:
    """Fixture providing the API base URL."""
    if not config.environment.api_base_url:
        pytest.skip("No API base URL configured for current environment")
    return config.environment.api_base_url


@pytest.fixture(scope="function")
def credentials(config: Config) -> dict:
    """Fixture providing test credentials."""
    creds = {
        "username": config.credentials.username,
        "password": config.credentials.password,
        "api_key": config.credentials.api_key,
        "token": config.credentials.token,
    }

    # Filter out None values
    return {k: v for k, v in creds.items() if v is not None}


@pytest.fixture(scope="function")
def test_data_dir(config: Config) -> Path:
    """Fixture providing the test data directory."""
    data_dir = Path.cwd() / "test_data"
    data_dir.mkdir(exist_ok=True)
    return data_dir


@pytest.fixture(scope="function")
def temp_dir(config: Config) -> Generator[Path, None, None]:
    """Fixture providing a temporary directory for test artifacts."""
    import shutil
    import tempfile

    temp_path = Path(tempfile.mkdtemp(prefix="pmas_test_"))
    try:
        yield temp_path
    finally:
        if temp_path.exists():
            shutil.rmtree(temp_path)


@pytest.fixture(scope="function")
def screenshot_dir(config: Config) -> Path:
    """Fixture providing the screenshot directory."""
    config.reporting.screenshot_dir.mkdir(parents=True, exist_ok=True)
    return config.reporting.screenshot_dir


@pytest.fixture(scope="session")
def test_environment(config: Config) -> str:
    """Fixture providing the current test environment name."""
    return config.environment.name


@pytest.fixture(scope="function")
def retry_config(config: Config) -> dict:
    """Fixture providing retry configuration for flaky tests."""
    return {"attempts": config.test.retry_attempts, "delay": config.test.retry_delay}


# Conditional fixtures based on environment
@pytest.fixture(scope="function")
def skip_in_production(config: Config):
    """Fixture that skips tests in production environment."""
    if config.environment.name == "prod":
        pytest.skip("Test skipped in production environment")


@pytest.fixture(scope="function")
def require_api_access(config: Config):
    """Fixture that skips tests if API access is not configured."""
    if not config.environment.api_base_url:
        pytest.skip("API access not configured")


@pytest.fixture(scope="function")
def require_credentials(config: Config):
    """Fixture that skips tests if credentials are not configured."""
    if not config.credentials.username or not config.credentials.password:
        pytest.skip("Test credentials not configured")


# Performance tracking fixtures
@pytest.fixture(scope="function")
def performance_tracker():
    """Fixture providing a performance tracker for timing operations."""
    from ..core.utils.timing import PerformanceTracker

    tracker = PerformanceTracker()
    yield tracker

    # Log performance summary if there are measurements
    if tracker.measurements:
        logger.info(f"Performance summary:\n{tracker.summary()}")


# Browser-specific fixtures
@pytest.fixture(scope="function")
def chrome_driver(config: Config) -> Generator[WebDriverProtocol, None, None]:
    """Chrome-specific driver fixture."""
    if config.browser.name != "chrome":
        pytest.skip("Test requires Chrome browser")

    # Use the main driver fixture but ensure it's Chrome
    original_browser = config.browser.name
    config.browser.name = "chrome"

    try:
        driver_instance = DriverFactory.create_driver(
            browser="chrome",
            headless=config.browser.headless,
            remote_url=config.webdriver.remote_url,
            window_size=config.window_size,
            download_dir=config.browser.download_dir,
            additional_options=config.browser.additional_options,
        )
        yield driver_instance
    finally:
        config.browser.name = original_browser
        if driver_instance:
            driver_instance.quit()


@pytest.fixture(scope="function")
def firefox_driver(config: Config) -> Generator[WebDriverProtocol, None, None]:
    """Firefox-specific driver fixture."""
    if config.browser.name != "firefox":
        pytest.skip("Test requires Firefox browser")

    original_browser = config.browser.name
    config.browser.name = "firefox"

    try:
        driver_instance = DriverFactory.create_driver(
            browser="firefox",
            headless=config.browser.headless,
            remote_url=config.webdriver.remote_url,
            window_size=config.window_size,
            download_dir=config.browser.download_dir,
            additional_options=config.browser.additional_options,
        )
        yield driver_instance
    finally:
        config.browser.name = original_browser
        if driver_instance:
            driver_instance.quit()


# Parametrized fixtures for cross-browser testing
@pytest.fixture(scope="function", params=["chrome", "firefox", "edge"])
def cross_browser_driver(
    request, config: Config
) -> Generator[WebDriverProtocol, None, None]:
    """Parametrized fixture for cross-browser testing."""
    browser = request.param

    try:
        driver_instance = DriverFactory.create_driver(
            browser=browser,
            headless=config.browser.headless,
            remote_url=config.webdriver.remote_url,
            window_size=config.window_size,
            download_dir=config.browser.download_dir,
            additional_options=config.browser.additional_options,
        )
        yield driver_instance
    finally:
        if driver_instance:
            driver_instance.quit()


# Hooks for test result tracking
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results for failure handling."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
