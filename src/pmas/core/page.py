"""
Base page class providing common page operations and navigation patterns.
"""

import logging
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, TypeVar

from selenium.common.exceptions import (
    TimeoutException,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .elements import BaseElement, Button, Checkbox, Dropdown, RadioButton, TextInput
from .errors import ElementNotFoundError, PageLoadError
from .locators import Locator

logger = logging.getLogger(__name__)

# Type variable for page classes
PageType = TypeVar("PageType", bound="BasePage")


class BasePage(ABC):
    """
    Abstract base class for all page objects.
    Provides common functionality for page navigation, waits, and element interactions.
    """

    # Subclasses should override these
    url_path: str = ""
    expected_titles: list[str] = []

    def __init__(self, driver, base_url: str = "", timeout: float = 10.0) -> None:
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._elements_cache: dict[str, BaseElement] = {}

    @property
    def url(self) -> str:
        """Get the full URL for this page."""
        if self.url_path:
            return f"{self.base_url}/{self.url_path.lstrip('/')}"
        return self.base_url

    @property
    def current_url(self) -> str:
        """Get the current browser URL."""
        return self.driver.current_url

    @property
    def title(self) -> str:
        """Get the current page title."""
        return self.driver.title

    def navigate_to(self, url: str | None = None) -> "BasePage":
        """
        Navigate to the page URL.

        Args:
            url: Optional URL to navigate to, defaults to self.url
        """
        target_url = url or self.url
        if not target_url:
            raise ValueError("No URL specified and page has no default URL")

        logger.info(f"Navigating to: {target_url}")
        self.driver.get(target_url)
        return self

    def wait_for_page_load(self, timeout: float | None = None) -> "BasePage":
        """
        Wait for the page to load completely.
        Checks for expected titles if defined.
        """
        timeout = timeout or self.timeout

        if self.expected_titles:
            try:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(
                    lambda driver: any(
                        title in driver.title for title in self.expected_titles
                    )
                )
                logger.debug(f"Page loaded with title: {self.title}")
            except TimeoutException:
                raise PageLoadError(
                    expected_title=str(self.expected_titles),
                    actual_title=self.title,
                    url=self.current_url,
                )

        # Wait for document ready state
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
        except TimeoutException:
            logger.warning("Page did not reach complete ready state within timeout")

        return self

    def refresh(self) -> "BasePage":
        """Refresh the current page."""
        logger.debug("Refreshing page")
        self.driver.refresh()
        return self.wait_for_page_load()

    def go_back(self) -> "BasePage":
        """Navigate back in browser history."""
        logger.debug("Navigating back")
        self.driver.back()
        return self

    def go_forward(self) -> "BasePage":
        """Navigate forward in browser history."""
        logger.debug("Navigating forward")
        self.driver.forward()
        return self

    def wait_for_element(
        self, locator: Locator, timeout: float | None = None
    ) -> BaseElement:
        """
        Wait for an element to be present and return it.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = timeout or self.timeout
        element = BaseElement(self.driver, locator, timeout)
        element.wait_for_visible()
        return element

    def wait_for_elements(
        self, locator: Locator, timeout: float | None = None
    ) -> list[BaseElement]:
        """
        Wait for multiple elements and return them as a list.

        Args:
            locator: Element locator
            timeout: Wait timeout, defaults to page timeout
        """
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = locator.selenium_locator
            elements = wait.until(EC.presence_of_all_elements_located((by, value)))
            return [BaseElement(self.driver, locator, timeout) for _ in elements]
        except TimeoutException as e:
            raise ElementNotFoundError(str(locator), timeout) from e

    def is_element_present(self, locator: Locator) -> bool:
        """Check if an element is present on the page."""
        try:
            by, value = locator.selenium_locator
            self.driver.find_element(by, value)
            return True
        except:
            return False

    def is_element_visible(self, locator: Locator) -> bool:
        """Check if an element is visible on the page."""
        try:
            element = BaseElement(self.driver, locator, 1.0)  # Short timeout
            return element.is_displayed
        except:
            return False

    def get_button(self, locator: Locator) -> Button:
        """Get a button element."""
        return Button(self.driver, locator, self.timeout)

    def get_text_input(self, locator: Locator) -> TextInput:
        """Get a text input element."""
        return TextInput(self.driver, locator, self.timeout)

    def get_dropdown(self, locator: Locator) -> Dropdown:
        """Get a dropdown element."""
        return Dropdown(self.driver, locator, self.timeout)

    def get_checkbox(self, locator: Locator) -> Checkbox:
        """Get a checkbox element."""
        return Checkbox(self.driver, locator, self.timeout)

    def get_radio_button(self, locator: Locator) -> RadioButton:
        """Get a radio button element."""
        return RadioButton(self.driver, locator, self.timeout)

    def execute_script(self, script: str, *args) -> Any:
        """Execute JavaScript in the browser."""
        return self.driver.execute_script(script, *args)

    def scroll_to_top(self) -> "BasePage":
        """Scroll to the top of the page."""
        self.execute_script("window.scrollTo(0, 0);")
        return self

    def scroll_to_bottom(self) -> "BasePage":
        """Scroll to the bottom of the page."""
        self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        return self

    def take_screenshot(self, filename: str | Path | None = None) -> Path:
        """
        Take a screenshot of the current page.

        Args:
            filename: Optional filename, defaults to timestamp-based name

        Returns:
            Path to the saved screenshot
        """
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        screenshot_path = Path(filename)
        if not screenshot_path.is_absolute():
            screenshot_path = Path.cwd() / "screenshots" / screenshot_path

        # Ensure directory exists
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)

        success = self.driver.get_screenshot_as_file(str(screenshot_path))
        if success:
            logger.info(f"Screenshot saved: {screenshot_path}")
        else:
            logger.error(f"Failed to save screenshot: {screenshot_path}")

        return screenshot_path

    def handle_alert(self, accept: bool = True, timeout: float = 5.0) -> str | None:
        """
        Handle JavaScript alerts.

        Args:
            accept: Whether to accept (True) or dismiss (False) the alert
            timeout: How long to wait for alert to appear

        Returns:
            Alert text if alert was present, None otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            alert = wait.until(EC.alert_is_present())
            alert_text = alert.text

            if accept:
                alert.accept()
                logger.debug(f"Accepted alert: {alert_text}")
            else:
                alert.dismiss()
                logger.debug(f"Dismissed alert: {alert_text}")

            return alert_text
        except TimeoutException:
            return None

    def switch_to_window(self, window_handle: str) -> "BasePage":
        """Switch to a specific browser window."""
        self.driver.switch_to.window(window_handle)
        logger.debug(f"Switched to window: {window_handle}")
        return self

    def switch_to_new_window(self) -> "BasePage":
        """Switch to the most recently opened window."""
        all_windows = self.driver.window_handles
        if len(all_windows) > 1:
            self.driver.switch_to.window(all_windows[-1])
            logger.debug("Switched to new window")
        return self

    def close_current_window(self) -> "BasePage":
        """Close the current window and switch to the previous one."""
        all_windows = self.driver.window_handles
        if len(all_windows) > 1:
            self.driver.close()
            self.driver.switch_to.window(all_windows[-2])
            logger.debug("Closed current window")
        return self

    @abstractmethod
    def verify_page_loaded(self) -> bool:
        """
        Verify that the page has loaded correctly.
        Subclasses should implement this method to check page-specific elements.
        """
        pass

    def __str__(self) -> str:
        """String representation of the page."""
        return f"{self.__class__.__name__}(url={self.url}, title={self.title})"
