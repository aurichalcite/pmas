"""
Pytest integration and testing utilities.
"""

from .assertions import SoftAssertions
from .fixtures import config, driver
from .reporting import setup_reporting

__all__ = ["driver", "config", "SoftAssertions", "setup_reporting"]
