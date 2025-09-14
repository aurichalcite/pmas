"""
WebDriver factory and protocol abstraction to decouple from Selenium specifics.
"""

import logging
from pathlib import Path
from typing import Any, Protocol

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.remote.webdriver import WebDriver

from .errors import ConfigurationError, DriverError

logger = logging.getLogger(__name__)


class WebDriverProtocol(Protocol):
    """
    Protocol defining the interface for WebDriver operations.
    This abstracts away Selenium-specific details from the rest of the framework.
    """

    def get(self, url: str) -> None:
        """Navigate to the specified URL."""
        ...

    def find_element(self, by: str, value: str):
        """Find a single element."""
        ...

    def find_elements(self, by: str, value: str):
        """Find multiple elements."""
        ...

    @property
    def title(self) -> str:
        """Get the page title."""
        ...

    @property
    def current_url(self) -> str:
        """Get the current URL."""
        ...

    def quit(self) -> None:
        """Quit the driver and close all windows."""
        ...

    def close(self) -> None:
        """Close the current window."""
        ...

    def maximize_window(self) -> None:
        """Maximize the browser window."""
        ...

    def set_window_size(self, width: int, height: int) -> None:
        """Set the window size."""
        ...

    def get_screenshot_as_file(self, filename: str) -> bool:
        """Save a screenshot to file."""
        ...

    def execute_script(self, script: str, *args) -> Any:
        """Execute JavaScript in the browser."""
        ...


class DriverFactory:
    """Factory for creating WebDriver instances with proper configuration."""

    SUPPORTED_BROWSERS = {"chrome", "firefox", "edge"}

    @classmethod
    def create_driver(
        cls,
        browser: str = "chrome",
        headless: bool = False,
        remote_url: str | None = None,
        window_size: tuple[int, int] | None = None,
        download_dir: Path | None = None,
        additional_options: list[str] | None = None,
        **kwargs: Any,
    ) -> WebDriver:
        """
        Create a WebDriver instance with the specified configuration.

        Args:
            browser: Browser type ('chrome', 'firefox', 'edge')
            headless: Run browser in headless mode
            remote_url: URL for remote WebDriver (Selenium Grid)
            window_size: Tuple of (width, height) for window size
            download_dir: Directory for downloads
            additional_options: List of additional browser options
            **kwargs: Additional arguments passed to WebDriver

        Returns:
            Configured WebDriver instance

        Raises:
            DriverError: If driver creation fails
            ConfigurationError: If invalid configuration provided
        """
        browser = browser.lower()
        if browser not in cls.SUPPORTED_BROWSERS:
            raise ConfigurationError(
                f"Unsupported browser: {browser}. "
                f"Supported browsers: {', '.join(cls.SUPPORTED_BROWSERS)}"
            )

        try:
            if remote_url:
                return cls._create_remote_driver(
                    browser,
                    remote_url,
                    headless,
                    window_size,
                    download_dir,
                    additional_options,
                    **kwargs,
                )
            else:
                return cls._create_local_driver(
                    browser,
                    headless,
                    window_size,
                    download_dir,
                    additional_options,
                    **kwargs,
                )
        except Exception as e:
            raise DriverError(f"Failed to create {browser} driver: {str(e)}") from e

    @classmethod
    def _create_local_driver(
        cls,
        browser: str,
        headless: bool,
        window_size: tuple[int, int] | None,
        download_dir: Path | None,
        additional_options: list[str] | None,
        **kwargs: Any,
    ) -> WebDriver:
        """Create a local WebDriver instance."""
        if browser == "chrome":
            options = cls._get_chrome_options(
                headless, window_size, download_dir, additional_options
            )
            service = ChromeService()
            driver = webdriver.Chrome(service=service, options=options, **kwargs)
        elif browser == "firefox":
            options = cls._get_firefox_options(
                headless, window_size, download_dir, additional_options
            )
            service = FirefoxService()
            driver = webdriver.Firefox(service=service, options=options, **kwargs)
        elif browser == "edge":
            options = cls._get_edge_options(
                headless, window_size, download_dir, additional_options
            )
            service = EdgeService()
            driver = webdriver.Edge(service=service, options=options, **kwargs)

        cls._configure_driver(driver, window_size)
        return driver

    @classmethod
    def _create_remote_driver(
        cls,
        browser: str,
        remote_url: str,
        headless: bool,
        window_size: tuple[int, int] | None,
        download_dir: Path | None,
        additional_options: list[str] | None,
        **kwargs: Any,
    ) -> WebDriver:
        """Create a remote WebDriver instance."""
        if browser == "chrome":
            options = cls._get_chrome_options(
                headless, window_size, download_dir, additional_options
            )
            capabilities = options.to_capabilities()
        elif browser == "firefox":
            options = cls._get_firefox_options(
                headless, window_size, download_dir, additional_options
            )
            capabilities = options.to_capabilities()
        elif browser == "edge":
            options = cls._get_edge_options(
                headless, window_size, download_dir, additional_options
            )
            capabilities = options.to_capabilities()

        driver = webdriver.Remote(
            command_executor=remote_url, desired_capabilities=capabilities, **kwargs
        )
        cls._configure_driver(driver, window_size)
        return driver

    @classmethod
    def _get_chrome_options(
        cls,
        headless: bool,
        window_size: tuple[int, int] | None,
        download_dir: Path | None,
        additional_options: list[str] | None,
    ) -> ChromeOptions:
        """Get Chrome options with common settings."""
        options = ChromeOptions()

        if headless:
            options.add_argument("--headless")

        # Common Chrome options for stability
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option(
            "prefs",
            {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
            },
        )

        if window_size:
            options.add_argument(f"--window-size={window_size[0]},{window_size[1]}")

        if download_dir:
            options.add_experimental_option(
                "prefs",
                {
                    "download.default_directory": str(download_dir),
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "safebrowsing.enabled": True,
                },
            )

        if additional_options:
            for option in additional_options:
                options.add_argument(option)

        return options

    @classmethod
    def _get_firefox_options(
        cls,
        headless: bool,
        window_size: tuple[int, int] | None,
        download_dir: Path | None,
        additional_options: list[str] | None,
    ) -> FirefoxOptions:
        """Get Firefox options with common settings."""
        options = FirefoxOptions()

        if headless:
            options.add_argument("--headless")

        if window_size:
            options.add_argument(f"--width={window_size[0]}")
            options.add_argument(f"--height={window_size[1]}")

        # Firefox preferences
        if download_dir:
            options.set_preference("browser.download.folderList", 2)
            options.set_preference("browser.download.dir", str(download_dir))
            options.set_preference(
                "browser.helperApps.neverAsk.saveToDisk",
                "application/pdf,text/csv,application/vnd.ms-excel",
            )

        if additional_options:
            for option in additional_options:
                options.add_argument(option)

        return options

    @classmethod
    def _get_edge_options(
        cls,
        headless: bool,
        window_size: tuple[int, int] | None,
        download_dir: Path | None,
        additional_options: list[str] | None,
    ) -> EdgeOptions:
        """Get Edge options with common settings."""
        options = EdgeOptions()

        if headless:
            options.add_argument("--headless")

        # Edge uses similar options to Chrome
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-notifications")

        if window_size:
            options.add_argument(f"--window-size={window_size[0]},{window_size[1]}")

        if download_dir:
            options.add_experimental_option(
                "prefs",
                {
                    "download.default_directory": str(download_dir),
                    "download.prompt_for_download": False,
                },
            )

        if additional_options:
            for option in additional_options:
                options.add_argument(option)

        return options

    @classmethod
    def _configure_driver(
        cls, driver: WebDriver, window_size: tuple[int, int] | None
    ) -> None:
        """Apply post-creation configuration to the driver."""
        if window_size:
            driver.set_window_size(window_size[0], window_size[1])
        else:
            driver.maximize_window()

        # Set implicit wait to 0 - we'll use explicit waits
        driver.implicitly_wait(0)

        logger.info(f"Created WebDriver: {driver.name} at {driver.current_url}")
