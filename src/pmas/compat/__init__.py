"""
Backward compatibility shims for legacy framework migration.

This module provides compatibility layers to ease migration from legacy
Selenium-based test frameworks to PMAS.
"""

from .legacy_config import LegacyConfig
from .legacy_driver import LegacyDriverManager
from .legacy_locators import LegacyLocators
from .legacy_page import LegacyPageObject

__all__ = ["LegacyPageObject", "LegacyLocators", "LegacyDriverManager", "LegacyConfig"]
