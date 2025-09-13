"""
Configuration management system with layered precedence.
"""

from .loader import ConfigLoader
from .model import Config

__all__ = ["Config", "ConfigLoader"]
