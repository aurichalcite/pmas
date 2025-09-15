"""
Legacy page object compatibility shim.

Provides a compatibility layer for existing page objects to work with PMAS
while maintaining the legacy API surface.
"""

import warnings

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..core.driver import WebDriverProtocol
from ..core.page import BasePage


class LegacyPageObject(BasePage):
    """
    Compatibility shim for legacy page objects.

    This class provides the legacy API while internally using PMAS components.
    It allows gradual migration of existing page objects.
    """

    def __init__(self, driver: WebDriverProtocol, timeout: float = 10.0) -> None:
        """
        Initialize legacy page object.

        Args:
            driver: WebDriver instance
            timeout: Default timeout for waits
        """
        warnings.warn(
            "LegacyPageObject is deprecated. Please migrate to pmas.BasePage",
            DeprecationWarning,
            stacklevel=2,
        )

        super().__init__(driver, "", timeout)
        self.wait = WebDriverWait(driver, timeout)

    def find_element(self, by: By, value: str) -> WebElement:
        """
        Find element using legacy By locators.

        Args:
            by: Selenium By strategy
            value: Locator value

        Returns:
            WebElement instance
        """
        warnings.warn(
            "find_element is deprecated. Use PMAS locator system instead",
            DeprecationWarning,
            stacklevel=2,
        )

        return self.driver.find_element(by, value)

    def find_elements(self, by: By, value: str) -> list[WebElement]:
        """
        Find elements using legacy By locators.

        Args:
            by: Selenium By strategy
            value: Locator value

        Returns:
            List of WebElement instances
        """
        warnings.warn(
            "find_elements is deprecated. Use PMAS locator system instead",
            DeprecationWarning,
            stacklevel=2,
        )

        return self.driver.find_elements(by, value)

    def wait_for_element(
        self, locator: tuple[By, str], timeout: float | None = None
    ) -> WebElement:
        """
        Wait for element to be present.

        Args:
            locator: Tuple of (By, value)
            timeout: Optional timeout override

        Returns:
            WebElement when found
        """
        warnings.warn(
            "Legacy wait_for_element is deprecated. Use PMAS wait methods instead",
            DeprecationWarning,
            stacklevel=2,
        )

        wait_timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_timeout)
        return wait.until(EC.presence_of_element_located(locator))

    def wait_for_element_clickable(
        self, locator: tuple[By, str], timeout: float | None = None
    ) -> WebElement:
        """
        Wait for element to be clickable.

        Args:
            locator: Tuple of (By, value)
            timeout: Optional timeout override

        Returns:
            WebElement when clickable
        """
        warnings.warn(
            "Legacy wait_for_element_clickable is deprecated. "
            "Use PMAS wait methods instead",
            DeprecationWarning,
            stacklevel=2,
        )

        wait_timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_timeout)
        return wait.until(EC.element_to_be_clickable(locator))

    def wait_for_element_visible(
        self, locator: tuple[By, str], timeout: float | None = None
    ) -> WebElement:
        """
        Wait for element to be visible.

        Args:
            locator: Tuple of (By, value)
            timeout: Optional timeout override

        Returns:
            WebElement when visible
        """
        warnings.warn(
            "Legacy wait_for_element_visible is deprecated. "
            "Use PMAS wait methods instead",
            DeprecationWarning,
            stacklevel=2,
        )

        wait_timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    def click_element(self, locator: tuple[By, str]) -> None:
        """
        Click element using legacy locator.

        Args:
            locator: Tuple of (By, value)
        """
        warnings.warn(
            "click_element is deprecated. Use PMAS element abstractions instead",
            DeprecationWarning,
            stacklevel=2,
        )

        element = self.wait_for_element_clickable(locator)
        element.click()

    def send_keys_to_element(
        self, locator: tuple[By, str], text: str, clear_first: bool = True
    ) -> None:
        """
        Send keys to element using legacy locator.

        Args:
            locator: Tuple of (By, value)
            text: Text to send
            clear_first: Whether to clear field first
        """
        warnings.warn(
            "send_keys_to_element is deprecated. Use PMAS element abstractions instead",
            DeprecationWarning,
            stacklevel=2,
        )

        element = self.wait_for_element(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)

    def get_element_text(self, locator: tuple[By, str]) -> str:
        """
        Get text from element using legacy locator.

        Args:
            locator: Tuple of (By, value)

        Returns:
            Element text
        """
        warnings.warn(
            "get_element_text is deprecated. Use PMAS element abstractions instead",
            DeprecationWarning,
            stacklevel=2,
        )

        element = self.wait_for_element(locator)
        return element.text

    def get_element_attribute(
        self, locator: tuple[By, str], attribute: str
    ) -> str | None:
        """
        Get attribute from element using legacy locator.

        Args:
            locator: Tuple of (By, value)
            attribute: Attribute name

        Returns:
            Attribute value or None
        """
        warnings.warn(
            "get_element_attribute is deprecated. "
            "Use PMAS element abstractions instead",
            DeprecationWarning,
            stacklevel=2,
        )

        element = self.wait_for_element(locator)
        return element.get_attribute(attribute)

    def is_element_present(self, locator: tuple[By, str]) -> bool:
        """
        Check if element is present.

        Args:
            locator: Tuple of (By, value)

        Returns:
            True if element is present
        """
        warnings.warn(
            "is_element_present is deprecated. Use PMAS element abstractions instead",
            DeprecationWarning,
            stacklevel=2,
        )

        try:
            self.driver.find_element(*locator)
            return True
        except Exception:
            return False

    def is_element_visible(self, locator: tuple[By, str]) -> bool:
        """
        Check if element is visible.

        Args:
            locator: Tuple of (By, value)

        Returns:
            True if element is visible
        """
        warnings.warn(
            "is_element_visible is deprecated. Use PMAS element abstractions instead",
            DeprecationWarning,
            stacklevel=2,
        )

        try:
            element = self.driver.find_element(*locator)
            return element.is_displayed()
        except Exception:
            return False

    def scroll_to_element(self, locator: tuple[By, str]) -> None:
        """
        Scroll to element using legacy locator.

        Args:
            locator: Tuple of (By, value)
        """
        warnings.warn(
            "scroll_to_element is deprecated. Use PMAS element abstractions instead",
            DeprecationWarning,
            stacklevel=2,
        )

        element = self.wait_for_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def select_dropdown_by_value(self, locator: tuple[By, str], value: str) -> None:
        """
        Select dropdown option by value using legacy locator.

        Args:
            locator: Tuple of (By, value)
            value: Option value to select
        """
        warnings.warn(
            "select_dropdown_by_value is deprecated. "
            "Use PMAS dropdown abstraction instead",
            DeprecationWarning,
            stacklevel=2,
        )

        from selenium.webdriver.support.ui import Select

        element = self.wait_for_element(locator)
        select = Select(element)
        select.select_by_value(value)

    def select_dropdown_by_text(self, locator: tuple[By, str], text: str) -> None:
        """
        Select dropdown option by visible text using legacy locator.

        Args:
            locator: Tuple of (By, value)
            text: Option text to select
        """
        warnings.warn(
            "select_dropdown_by_text is deprecated. "
            "Use PMAS dropdown abstraction instead",
            DeprecationWarning,
            stacklevel=2,
        )

        from selenium.webdriver.support.ui import Select

        element = self.wait_for_element(locator)
        select = Select(element)
        select.select_by_visible_text(text)
