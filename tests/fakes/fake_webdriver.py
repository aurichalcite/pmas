"""
Fake WebDriver implementation for fast unit and integration testing.

This module provides a FakeWebDriver class that mimics the essential Selenium WebDriver
API without actually launching a browser. It's designed for:
- Fast unit tests that need to verify WebDriver interactions
- Integration tests that test component interactions without browser overhead
- Deterministic testing with configurable failure modes

The FakeWebDriver implements the WebDriverProtocol interface and provides:
- State tracking for verification in tests
- Configurable responses and failure modes
- Helper methods for test setup and verification
"""

import time
from typing import Any

from selenium.common.exceptions import (
    NoSuchElementException,
    WebDriverException,
)


class FakeWebElement:
    """
    Fake WebElement that mimics Selenium WebElement behavior.

    This class provides a lightweight implementation of WebElement methods
    for testing element interactions without a real browser.
    """

    def __init__(
        self,
        tag_name: str = "div",
        text: str = "",
        attributes: dict[str, str] | None = None,
        is_displayed: bool = True,
        is_enabled: bool = True,
        is_selected: bool = False,
    ):
        self.tag_name = tag_name
        self.text = text
        self.attributes = attributes or {}
        self._is_displayed = is_displayed
        self._is_enabled = is_enabled
        self._is_selected = is_selected
        self._click_count = 0
        self._text_input = ""

    def click(self) -> None:
        """Simulate clicking the element."""
        if not self._is_enabled:
            raise WebDriverException("Element is not clickable")
        self._click_count += 1

    def send_keys(self, *value: str) -> None:
        """Simulate typing text into the element."""
        if not self._is_enabled:
            raise WebDriverException("Element is not enabled")
        self._text_input += "".join(str(v) for v in value)

    def clear(self) -> None:
        """Simulate clearing the element's text."""
        if not self._is_enabled:
            raise WebDriverException("Element is not enabled")
        self._text_input = ""

    def get_attribute(self, name: str) -> str | None:
        """Get an attribute value."""
        return self.attributes.get(name)

    def is_displayed(self) -> bool:
        """Check if element is displayed."""
        return self._is_displayed

    def is_enabled(self) -> bool:
        """Check if element is enabled."""
        return self._is_enabled

    def is_selected(self) -> bool:
        """Check if element is selected."""
        return self._is_selected

    @property
    def size(self) -> dict[str, int]:
        """Get element size."""
        return {"height": 20, "width": 100}

    @property
    def location(self) -> dict[str, int]:
        """Get element location."""
        return {"x": 0, "y": 0}


class FakeWebDriver:
    """
    Fake WebDriver implementation that mimics essential Selenium WebDriver API.

    This class provides a lightweight, fast alternative to real WebDriver for testing.
    It implements the WebDriverProtocol interface and tracks state for verification.

    Key features:
    - Configurable failure modes for testing error scenarios
    - State tracking for verification in tests
    - Fast execution without browser overhead
    - Support for common WebDriver operations

    Example:
        driver = FakeWebDriver()
        driver.configure_response("get", success=True)
        driver.get("http://example.com")
        assert driver.current_url == "http://example.com"
    """

    def __init__(self):
        # State tracking
        self._current_url = "data:,"
        self._title = ""
        self._page_source = "<html><body></body></html>"
        self._window_size = {"width": 1280, "height": 720}
        self._is_quit = False

        # Operation tracking for test verification
        self.operation_log: list[dict[str, Any]] = []
        self._elements_registry: dict[str, FakeWebElement] = {}

        # Configurable responses and failure modes
        self._failure_modes: dict[str, dict[str, Any]] = {}
        self._response_delays: dict[str, float] = {}

        # Default elements for common selectors
        self._setup_default_elements()

    def _setup_default_elements(self) -> None:
        """Set up default elements for common test scenarios."""
        # Common login form elements
        self._elements_registry.update(
            {
                "id:username": FakeWebElement(
                    "input", attributes={"type": "text", "id": "username"}
                ),
                "id:password": FakeWebElement(
                    "input", attributes={"type": "password", "id": "password"}
                ),
                "id:login-button": FakeWebElement(
                    "button", text="Login", attributes={"id": "login-button"}
                ),
                "css:.login-form": FakeWebElement(
                    "form", attributes={"class": "login-form"}
                ),
                "xpath://button[@type='submit']": FakeWebElement(
                    "button", attributes={"type": "submit"}
                ),
            }
        )

    def _log_operation(self, operation: str, **kwargs) -> None:
        """Log an operation for test verification."""
        self.operation_log.append(
            {"operation": operation, "timestamp": time.time(), **kwargs}
        )

    def _check_failure_mode(self, operation: str) -> None:
        """Check if operation should fail based on configured failure modes."""
        if operation in self._failure_modes:
            failure_config = self._failure_modes[operation]
            if failure_config.get("should_fail", False):
                exception_type = failure_config.get("exception", WebDriverException)
                message = failure_config.get(
                    "message", f"Simulated failure in {operation}"
                )
                raise exception_type(message)

    def _apply_delay(self, operation: str) -> None:
        """Apply configured delay for operation."""
        if operation in self._response_delays:
            time.sleep(self._response_delays[operation])

    # Configuration methods for test setup

    def configure_failure_mode(
        self,
        operation: str,
        should_fail: bool = True,
        exception: type = WebDriverException,
        message: str = "",
    ) -> None:
        """
        Configure failure mode for specific operations.

        Args:
            operation: Operation name (e.g., 'get', 'find_element')
            should_fail: Whether the operation should fail
            exception: Exception type to raise
            message: Custom error message
        """
        self._failure_modes[operation] = {
            "should_fail": should_fail,
            "exception": exception,
            "message": message or f"Simulated failure in {operation}",
        }

    def configure_response_delay(self, operation: str, delay: float) -> None:
        """Configure response delay for operations."""
        self._response_delays[operation] = delay

    def add_element(self, selector: str, element: FakeWebElement) -> None:
        """Add an element to the registry."""
        self._elements_registry[selector] = element

    def remove_element(self, selector: str) -> None:
        """Remove an element from the registry."""
        self._elements_registry.pop(selector, None)

    # WebDriver API implementation

    def get(self, url: str) -> None:
        """Navigate to the specified URL."""
        if self._is_quit:
            raise WebDriverException("Driver has been quit")

        self._check_failure_mode("get")
        self._apply_delay("get")

        self._current_url = url
        # Simulate page title based on URL
        if "example.com" in url:
            self._title = "Example Domain"
        elif "login" in url.lower():
            self._title = "Login Page"
        else:
            self._title = "Test Page"

        self._log_operation("get", url=url)

    def find_element(self, by: str, value: str) -> FakeWebElement:
        """Find a single element."""
        if self._is_quit:
            raise WebDriverException("Driver has been quit")

        self._check_failure_mode("find_element")
        self._apply_delay("find_element")

        selector_key = f"{by}:{value}"
        element = self._elements_registry.get(selector_key)

        if element is None:
            self._log_operation("find_element", by=by, value=value, found=False)
            raise NoSuchElementException(f"Unable to locate element: {by}={value}")

        self._log_operation("find_element", by=by, value=value, found=True)
        return element

    def find_elements(self, by: str, value: str) -> list[FakeWebElement]:
        """Find multiple elements."""
        if self._is_quit:
            raise WebDriverException("Driver has been quit")

        self._check_failure_mode("find_elements")
        self._apply_delay("find_elements")

        selector_key = f"{by}:{value}"
        element = self._elements_registry.get(selector_key)

        elements = [element] if element else []
        self._log_operation("find_elements", by=by, value=value, count=len(elements))
        return elements

    @property
    def title(self) -> str:
        """Get the page title."""
        return self._title

    @property
    def current_url(self) -> str:
        """Get the current URL."""
        return self._current_url

    @property
    def page_source(self) -> str:
        """Get the page source."""
        return self._page_source

    def quit(self) -> None:
        """Quit the driver and close all windows."""
        self._is_quit = True
        self._log_operation("quit")

    def close(self) -> None:
        """Close the current window."""
        if self._is_quit:
            raise WebDriverException("Driver has been quit")
        self._log_operation("close")

    def maximize_window(self) -> None:
        """Maximize the browser window."""
        if self._is_quit:
            raise WebDriverException("Driver has been quit")
        self._window_size = {"width": 1920, "height": 1080}
        self._log_operation("maximize_window")

    def set_window_size(self, width: int, height: int) -> None:
        """Set the window size."""
        if self._is_quit:
            raise WebDriverException("Driver has been quit")
        self._window_size = {"width": width, "height": height}
        self._log_operation("set_window_size", width=width, height=height)

    def get_window_size(self) -> dict[str, int]:
        """Get the window size."""
        return self._window_size.copy()

    # Helper methods for test verification

    def get_operation_count(self, operation: str) -> int:
        """Get the count of specific operations performed."""
        return len([op for op in self.operation_log if op["operation"] == operation])

    def get_last_operation(self, operation: str) -> dict[str, Any] | None:
        """Get the last occurrence of a specific operation."""
        matching_ops = [op for op in self.operation_log if op["operation"] == operation]
        return matching_ops[-1] if matching_ops else None

    def clear_operation_log(self) -> None:
        """Clear the operation log."""
        self.operation_log.clear()

    def reset_state(self) -> None:
        """Reset the driver to initial state."""
        self._current_url = "data:,"
        self._title = ""
        self._page_source = "<html><body></body></html>"
        self._window_size = {"width": 1280, "height": 720}
        self._is_quit = False
        self.operation_log.clear()
        self._failure_modes.clear()
        self._response_delays.clear()
        self._setup_default_elements()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if not self._is_quit:
            self.quit()
