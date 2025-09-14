"""
PMAS - Production Management Automation Suite

A modern, reusable Web UI testing framework built on Python 3.11+ and Selenium 4+.
Provides domain-agnostic core components with specific domain adapters.
"""

__version__ = "1.0.0"
__author__ = "PMAS Development Team"

# Core framework imports for easy access
# Domain packages
from . import domains
from .config.loader import ConfigLoader
from .config.model import Config
from .core.driver import DriverFactory, WebDriverProtocol
from .core.elements import BaseElement, Button, Dropdown, TextInput
from .core.locators import Locator
from .core.page import BasePage

__all__ = [
    "DriverFactory",
    "WebDriverProtocol",
    "BasePage",
    "BaseElement",
    "Button",
    "TextInput",
    "Dropdown",
    "Locator",
    "Config",
    "ConfigLoader",
    "domains",
]
