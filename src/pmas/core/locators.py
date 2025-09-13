"""
Typed locator system for web elements with modern Python patterns.
"""

from dataclasses import dataclass
from typing import Literal

from selenium.webdriver.common.by import By

# Type alias for locator strategies
LocatorStrategy = Literal[
    "id",
    "css",
    "xpath",
    "name",
    "class_name",
    "tag_name",
    "link_text",
    "partial_link_text",
]

# Mapping from our strategy names to Selenium By constants
STRATEGY_MAP = {
    "id": By.ID,
    "css": By.CSS_SELECTOR,
    "xpath": By.XPATH,
    "name": By.NAME,
    "class_name": By.CLASS_NAME,
    "tag_name": By.TAG_NAME,
    "link_text": By.LINK_TEXT,
    "partial_link_text": By.PARTIAL_LINK_TEXT,
}


@dataclass(frozen=True)
class Locator:
    """
    Immutable locator for web elements with type safety.

    Args:
        strategy: The locator strategy (id, css, xpath, etc.)
        value: The locator value/selector string
        description: Optional human-readable description for debugging

    Example:
        >>> login_button = Locator('id', 'login-btn', 'Login button')
        >>> username_field = Locator('css', 'input[name="username"]')
    """

    strategy: LocatorStrategy
    value: str
    description: str = ""

    def __post_init__(self) -> None:
        """Validate the locator strategy."""
        if self.strategy not in STRATEGY_MAP:
            raise ValueError(f"Invalid locator strategy: {self.strategy}")

    @property
    def selenium_by(self) -> str:
        """Get the Selenium By constant for this locator."""
        return STRATEGY_MAP[self.strategy]

    @property
    def selenium_locator(self) -> tuple[str, str]:
        """Get the (By, value) tuple for Selenium WebDriver methods."""
        return (self.selenium_by, self.value)

    def format(self, **kwargs: str | int) -> "Locator":
        """
        Create a new locator with formatted value using string interpolation.

        Args:
            **kwargs: Values to substitute in the locator value

        Returns:
            New Locator instance with formatted value

        Example:
            >>> template = Locator('xpath', '//button[@data-id="{button_id}"]')
            >>> specific = template.format(button_id='submit')
        """
        try:
            formatted_value = self.value.format(**kwargs)
            return Locator(
                strategy=self.strategy,
                value=formatted_value,
                description=self.description,
            )
        except KeyError as e:
            raise ValueError(f"Missing format parameter: {e}") from e

    def __str__(self) -> str:
        """String representation for debugging."""
        desc = f" ({self.description})" if self.description else ""
        return f"{self.strategy}='{self.value}'{desc}"


# Convenience factory functions for common locator types
def by_id(value: str, description: str = "") -> Locator:
    """Create an ID locator."""
    return Locator("id", value, description)


def by_css(value: str, description: str = "") -> Locator:
    """Create a CSS selector locator."""
    return Locator("css", value, description)


def by_xpath(value: str, description: str = "") -> Locator:
    """Create an XPath locator."""
    return Locator("xpath", value, description)


def by_name(value: str, description: str = "") -> Locator:
    """Create a name attribute locator."""
    return Locator("name", value, description)


def by_class(value: str, description: str = "") -> Locator:
    """Create a class name locator."""
    return Locator("class_name", value, description)


def by_tag(value: str, description: str = "") -> Locator:
    """Create a tag name locator."""
    return Locator("tag_name", value, description)


def by_link_text(value: str, description: str = "") -> Locator:
    """Create a link text locator."""
    return Locator("link_text", value, description)


def by_partial_link_text(value: str, description: str = "") -> Locator:
    """Create a partial link text locator."""
    return Locator("partial_link_text", value, description)
