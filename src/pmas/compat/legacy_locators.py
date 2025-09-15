"""
Legacy locator compatibility shim.

Provides compatibility for legacy locator patterns while encouraging
migration to the new PMAS locator system.
"""

import warnings

from selenium.webdriver.common.by import By

from ..core.locators import (
    Locator,
    by_class_name,
    by_css_selector,
    by_id,
    by_link_text,
    by_name,
    by_partial_link_text,
    by_tag_name,
    by_xpath,
)


class LegacyLocators:
    """
    Compatibility shim for legacy locator patterns.

    This class provides static methods that convert legacy locator tuples
    to PMAS Locator objects while issuing deprecation warnings.
    """

    @staticmethod
    def convert_legacy_locator(
        locator: tuple[By, str], description: str = ""
    ) -> Locator:
        """
        Convert legacy (By, value) tuple to PMAS Locator.

        Args:
            locator: Legacy locator tuple
            description: Optional description for the locator

        Returns:
            PMAS Locator object
        """
        warnings.warn(
            "Legacy locator tuples are deprecated. Use PMAS locator functions instead",
            DeprecationWarning,
            stacklevel=3,
        )

        by_strategy, value = locator
        desc = description or f"Legacy locator: {by_strategy.value}='{value}'"

        # Map legacy By strategies to PMAS locator functions
        strategy_map = {
            By.ID: by_id,
            By.CLASS_NAME: by_class_name,
            By.TAG_NAME: by_tag_name,
            By.NAME: by_name,
            By.XPATH: by_xpath,
            By.CSS_SELECTOR: by_css_selector,
            By.LINK_TEXT: by_link_text,
            By.PARTIAL_LINK_TEXT: by_partial_link_text,
        }

        if by_strategy in strategy_map:
            return strategy_map[by_strategy](value, desc)
        else:
            # Fallback for unknown strategies
            return Locator(by_strategy.value, value, desc)

    @staticmethod
    def id(value: str, description: str = "") -> Locator:
        """
        Create ID locator with deprecation warning.

        Args:
            value: ID value
            description: Optional description

        Returns:
            PMAS Locator object
        """
        warnings.warn(
            "LegacyLocators.id is deprecated. Use pmas.by_id instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return by_id(value, description or f"Legacy ID locator: {value}")

    @staticmethod
    def class_name(value: str, description: str = "") -> Locator:
        """
        Create class name locator with deprecation warning.

        Args:
            value: Class name value
            description: Optional description

        Returns:
            PMAS Locator object
        """
        warnings.warn(
            "LegacyLocators.class_name is deprecated. Use pmas.by_class_name instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return by_class_name(
            value, description or f"Legacy class name locator: {value}"
        )

    @staticmethod
    def tag_name(value: str, description: str = "") -> Locator:
        """
        Create tag name locator with deprecation warning.

        Args:
            value: Tag name value
            description: Optional description

        Returns:
            PMAS Locator object
        """
        warnings.warn(
            "LegacyLocators.tag_name is deprecated. Use pmas.by_tag_name instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return by_tag_name(value, description or f"Legacy tag name locator: {value}")

    @staticmethod
    def name(value: str, description: str = "") -> Locator:
        """
        Create name locator with deprecation warning.

        Args:
            value: Name value
            description: Optional description

        Returns:
            PMAS Locator object
        """
        warnings.warn(
            "LegacyLocators.name is deprecated. Use pmas.by_name instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return by_name(value, description or f"Legacy name locator: {value}")

    @staticmethod
    def xpath(value: str, description: str = "") -> Locator:
        """
        Create XPath locator with deprecation warning.

        Args:
            value: XPath value
            description: Optional description

        Returns:
            PMAS Locator object
        """
        warnings.warn(
            "LegacyLocators.xpath is deprecated. Use pmas.by_xpath instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return by_xpath(value, description or f"Legacy XPath locator: {value}")

    @staticmethod
    def css_selector(value: str, description: str = "") -> Locator:
        """
        Create CSS selector locator with deprecation warning.

        Args:
            value: CSS selector value
            description: Optional description

        Returns:
            PMAS Locator object
        """
        warnings.warn(
            "LegacyLocators.css_selector is deprecated. "
            "Use pmas.by_css_selector instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return by_css_selector(
            value, description or f"Legacy CSS selector locator: {value}"
        )

    @staticmethod
    def link_text(value: str, description: str = "") -> Locator:
        """
        Create link text locator with deprecation warning.

        Args:
            value: Link text value
            description: Optional description

        Returns:
            PMAS Locator object
        """
        warnings.warn(
            "LegacyLocators.link_text is deprecated. Use pmas.by_link_text instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return by_link_text(value, description or f"Legacy link text locator: {value}")

    @staticmethod
    def partial_link_text(value: str, description: str = "") -> Locator:
        """
        Create partial link text locator with deprecation warning.

        Args:
            value: Partial link text value
            description: Optional description

        Returns:
            PMAS Locator object
        """
        warnings.warn(
            "LegacyLocators.partial_link_text is deprecated. "
            "Use pmas.by_partial_link_text instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return by_partial_link_text(
            value, description or f"Legacy partial link text locator: {value}"
        )


# Legacy constants for backward compatibility
class LegacyBy:
    """
    Legacy By constants for backward compatibility.

    These constants provide the same interface as selenium.webdriver.common.by.By
    but issue deprecation warnings when used.
    """

    @property
    def ID(self) -> str:
        warnings.warn(
            "LegacyBy.ID is deprecated. Use pmas.by_id function instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return By.ID

    @property
    def CLASS_NAME(self) -> str:
        warnings.warn(
            "LegacyBy.CLASS_NAME is deprecated. "
            "Use pmas.by_class_name function instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return By.CLASS_NAME

    @property
    def TAG_NAME(self) -> str:
        warnings.warn(
            "LegacyBy.TAG_NAME is deprecated. Use pmas.by_tag_name function instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return By.TAG_NAME

    @property
    def NAME(self) -> str:
        warnings.warn(
            "LegacyBy.NAME is deprecated. Use pmas.by_name function instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return By.NAME

    @property
    def XPATH(self) -> str:
        warnings.warn(
            "LegacyBy.XPATH is deprecated. Use pmas.by_xpath function instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return By.XPATH

    @property
    def CSS_SELECTOR(self) -> str:
        warnings.warn(
            "LegacyBy.CSS_SELECTOR is deprecated. "
            "Use pmas.by_css_selector function instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return By.CSS_SELECTOR

    @property
    def LINK_TEXT(self) -> str:
        warnings.warn(
            "LegacyBy.LINK_TEXT is deprecated. Use pmas.by_link_text function instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return By.LINK_TEXT

    @property
    def PARTIAL_LINK_TEXT(self) -> str:
        warnings.warn(
            "LegacyBy.PARTIAL_LINK_TEXT is deprecated. "
            "Use pmas.by_partial_link_text function instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return By.PARTIAL_LINK_TEXT


# Create singleton instance for backward compatibility
legacy_by = LegacyBy()
