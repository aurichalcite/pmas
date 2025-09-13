"""
Core framework components - domain-agnostic testing infrastructure.
"""

from .driver import DriverFactory, WebDriverProtocol
from .elements import BaseElement, Button, Dropdown, TextInput
from .errors import ConfigurationError, ElementNotFoundError, FrameworkError
from .locators import Locator
from .page import BasePage

__all__ = [
    "DriverFactory",
    "WebDriverProtocol",
    "BasePage",
    "BaseElement",
    "Button",
    "TextInput",
    "Dropdown",
    "Locator",
    "FrameworkError",
    "ElementNotFoundError",
    "ConfigurationError",
]
