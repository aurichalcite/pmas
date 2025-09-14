"""
Base abstractions for web elements with common interaction patterns.
"""

import logging
import time
from abc import ABC
from typing import Any

from selenium.common.exceptions import (
    ElementNotInteractableException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from .errors import ElementNotFoundError, ElementNotInteractableError
from .locators import Locator

logger = logging.getLogger(__name__)


class BaseElement(ABC):
    """
    Abstract base class for all web element wrappers.
    Provides common functionality for element interaction with robust error handling.
    """

    def __init__(self, driver, locator: Locator, timeout: float = 10.0) -> None:
        self.driver = driver
        self.locator = locator
        self.timeout = timeout
        self._element: WebElement | None = None

    @property
    def element(self) -> WebElement:
        """Get the underlying WebElement, finding it if necessary."""
        if self._element is None or self._is_stale():
            self._element = self._find_element()
        return self._element

    def _find_element(self) -> WebElement:
        """Find the element using the locator."""
        try:
            wait = WebDriverWait(self.driver, self.timeout)
            by, value = self.locator.selenium_locator
            element = wait.until(EC.presence_of_element_located((by, value)))
            logger.debug(f"Found element: {self.locator}")
            return element
        except TimeoutException as e:
            raise ElementNotFoundError(str(self.locator), self.timeout) from e

    def _is_stale(self) -> bool:
        """Check if the current element reference is stale."""
        if self._element is None:
            return False
        try:
            # Accessing any property will raise StaleElementReferenceException if stale
            _ = self._element.tag_name
            return False
        except StaleElementReferenceException:
            return True

    def wait_for_visible(self, timeout: float | None = None) -> "BaseElement":
        """Wait for the element to be visible."""
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = self.locator.selenium_locator
            wait.until(EC.visibility_of_element_located((by, value)))
            return self
        except TimeoutException as e:
            raise ElementNotFoundError(f"{self.locator} (visible)", timeout) from e

    def wait_for_clickable(self, timeout: float | None = None) -> "BaseElement":
        """Wait for the element to be clickable."""
        timeout = timeout or self.timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            by, value = self.locator.selenium_locator
            wait.until(EC.element_to_be_clickable((by, value)))
            return self
        except TimeoutException as e:
            raise ElementNotFoundError(f"{self.locator} (clickable)", timeout) from e

    def scroll_into_view(self) -> "BaseElement":
        """Scroll the element into view."""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", self.element)
        time.sleep(0.1)  # Small delay for scroll to complete
        return self

    def highlight(self, duration: float = 1.0) -> "BaseElement":
        """Highlight the element for debugging purposes."""
        original_style = self.element.get_attribute("style")
        self.driver.execute_script(
            "arguments[0].style.border='3px solid red';", self.element
        )
        time.sleep(duration)
        self.driver.execute_script(
            f"arguments[0].style.border='{original_style}';", self.element
        )
        return self

    @property
    def text(self) -> str:
        """Get the text content of the element."""
        return self.element.text

    @property
    def is_displayed(self) -> bool:
        """Check if the element is displayed."""
        try:
            return self.element.is_displayed()
        except StaleElementReferenceException:
            self._element = None
            return self.element.is_displayed()

    @property
    def is_enabled(self) -> bool:
        """Check if the element is enabled."""
        return self.element.is_enabled()

    def get_attribute(self, name: str) -> str | None:
        """Get an attribute value from the element."""
        return self.element.get_attribute(name)

    def get_property(self, name: str) -> Any:
        """Get a property value from the element."""
        return self.element.get_property(name)


class Clickable(BaseElement):
    """Base class for clickable elements like buttons and links."""

    def click(self, force: bool = False) -> "Clickable":
        """
        Click the element.

        Args:
            force: If True, use JavaScript click instead of normal click
        """
        try:
            if force:
                self.driver.execute_script("arguments[0].click();", self.element)
            else:
                self.scroll_into_view()
                self.wait_for_clickable()
                self.element.click()
            logger.debug(f"Clicked element: {self.locator}")
            return self
        except ElementNotInteractableException as e:
            raise ElementNotInteractableError(str(self.locator), "click") from e

    def double_click(self) -> "Clickable":
        """Double-click the element."""
        self.scroll_into_view()
        self.wait_for_clickable()
        ActionChains(self.driver).double_click(self.element).perform()
        logger.debug(f"Double-clicked element: {self.locator}")
        return self

    def right_click(self) -> "Clickable":
        """Right-click the element."""
        self.scroll_into_view()
        self.wait_for_clickable()
        ActionChains(self.driver).context_click(self.element).perform()
        logger.debug(f"Right-clicked element: {self.locator}")
        return self


class Button(Clickable):
    """Represents a button element."""

    pass


class Link(Clickable):
    """Represents a link element."""

    @property
    def href(self) -> str | None:
        """Get the href attribute of the link."""
        return self.get_attribute("href")


class TextInput(BaseElement):
    """Represents a text input field."""

    def clear(self) -> "TextInput":
        """Clear the input field."""
        self.wait_for_visible()
        self.element.clear()
        logger.debug(f"Cleared input: {self.locator}")
        return self

    def type_text(self, text: str, clear_first: bool = True) -> "TextInput":
        """
        Type text into the input field.

        Args:
            text: Text to type
            clear_first: Whether to clear the field first
        """
        self.wait_for_visible()
        if clear_first:
            self.clear()
        self.element.send_keys(text)
        logger.debug(f"Typed '{text}' into input: {self.locator}")
        return self

    def append_text(self, text: str) -> "TextInput":
        """Append text to the existing content."""
        return self.type_text(text, clear_first=False)

    def press_key(self, key: str) -> "TextInput":
        """Press a special key (e.g., Keys.ENTER, Keys.TAB)."""
        self.element.send_keys(key)
        logger.debug(f"Pressed key '{key}' in input: {self.locator}")
        return self

    @property
    def value(self) -> str:
        """Get the current value of the input field."""
        return self.get_attribute("value") or ""


class Dropdown(BaseElement):
    """Represents a dropdown/select element."""

    @property
    def select(self) -> Select:
        """Get the Selenium Select object."""
        return Select(self.element)

    def select_by_text(self, text: str) -> "Dropdown":
        """Select an option by visible text."""
        self.wait_for_visible()
        self.select.select_by_visible_text(text)
        logger.debug(f"Selected '{text}' in dropdown: {self.locator}")
        return self

    def select_by_value(self, value: str) -> "Dropdown":
        """Select an option by value attribute."""
        self.wait_for_visible()
        self.select.select_by_value(value)
        logger.debug(f"Selected value '{value}' in dropdown: {self.locator}")
        return self

    def select_by_index(self, index: int) -> "Dropdown":
        """Select an option by index."""
        self.wait_for_visible()
        self.select.select_by_index(index)
        logger.debug(f"Selected index {index} in dropdown: {self.locator}")
        return self

    @property
    def selected_option_text(self) -> str:
        """Get the text of the currently selected option."""
        return self.select.first_selected_option.text

    @property
    def selected_option_value(self) -> str:
        """Get the value of the currently selected option."""
        return self.select.first_selected_option.get_attribute("value")

    @property
    def all_options_text(self) -> list[str]:
        """Get text of all available options."""
        return [option.text for option in self.select.options]


class Checkbox(BaseElement):
    """Represents a checkbox element."""

    def check(self) -> "Checkbox":
        """Check the checkbox if not already checked."""
        if not self.is_checked:
            self.scroll_into_view()
            self.wait_for_clickable()
            self.element.click()
            logger.debug(f"Checked checkbox: {self.locator}")
        return self

    def uncheck(self) -> "Checkbox":
        """Uncheck the checkbox if currently checked."""
        if self.is_checked:
            self.scroll_into_view()
            self.wait_for_clickable()
            self.element.click()
            logger.debug(f"Unchecked checkbox: {self.locator}")
        return self

    def toggle(self) -> "Checkbox":
        """Toggle the checkbox state."""
        self.scroll_into_view()
        self.wait_for_clickable()
        self.element.click()
        logger.debug(f"Toggled checkbox: {self.locator}")
        return self

    @property
    def is_checked(self) -> bool:
        """Check if the checkbox is currently checked."""
        return self.element.is_selected()


class RadioButton(BaseElement):
    """Represents a radio button element."""

    def select(self) -> "RadioButton":
        """Select the radio button."""
        if not self.is_selected:
            self.scroll_into_view()
            self.wait_for_clickable()
            self.element.click()
            logger.debug(f"Selected radio button: {self.locator}")
        return self

    @property
    def is_selected(self) -> bool:
        """Check if the radio button is currently selected."""
        return self.element.is_selected()
