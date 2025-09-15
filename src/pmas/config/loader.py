"""
Configuration loader with layered precedence: CLI > ENV > TOML > Defaults.
"""

import argparse
import logging
import os
import tomllib
from pathlib import Path
from typing import Any

from ..core.errors import ConfigurationError
from .model import (
    BrowserConfig,
    Config,
    CredentialsConfig,
    EnvironmentConfig,
    LoggingConfig,
    ReportingConfig,
    TestingConfig,
    WebDriverConfig,
)

logger = logging.getLogger(__name__)


class ConfigLoader:
    """
    Loads configuration from multiple sources with proper precedence.

    Precedence order (highest to lowest):
    1. Command line arguments
    2. Environment variables
    3. TOML configuration file
    4. Default values
    """

    DEFAULT_CONFIG_PATHS = [
        Path.cwd() / "pmas.toml",
        Path.cwd() / "config" / "pmas.toml",
        Path.home() / ".pmas" / "config.toml",
    ]

    ENV_PREFIX = "PMAS_"

    def __init__(self, config_path: str | Path | None = None) -> None:
        self.config_path = Path(config_path) if config_path else None
        self.cli_args: argparse.Namespace | None = None

    def load(self, cli_args: list[str] | None = None) -> Config:
        """
        Load configuration from all sources.

        Args:
            cli_args: Optional CLI arguments to parse

        Returns:
            Fully loaded and validated configuration
        """
        # Start with defaults
        config_dict = self._get_default_config()

        # Layer 1: TOML file
        toml_config = self._load_toml_config()
        if toml_config:
            config_dict = self._merge_configs(config_dict, toml_config)

        # Layer 2: Environment variables
        env_config = self._load_env_config()
        if env_config:
            config_dict = self._merge_configs(config_dict, env_config)

        # Layer 3: CLI arguments
        if cli_args is not None:
            self.cli_args = self._parse_cli_args(cli_args)
            cli_config = self._cli_args_to_config()
            if cli_config:
                config_dict = self._merge_configs(config_dict, cli_config)

        # Create and validate configuration
        try:
            config = self._dict_to_config(config_dict)
            errors = config.validate()
            if errors:
                raise ConfigurationError(f"Configuration validation failed: {errors}")

            logger.info(
                f"Configuration loaded successfully from {self._get_config_sources()}"
            )
            return config

        except Exception as e:
            raise ConfigurationError(f"Failed to create configuration: {e}") from e

    def _get_default_config(self) -> dict[str, Any]:
        """Get default configuration values."""
        return {
            "browser": {
                "name": "chrome",
                "headless": False,
                "window_width": 1920,
                "window_height": 1080,
                "additional_options": [],
            },
            "webdriver": {
                "remote_url": None,
                "implicit_wait": 0.0,
                "page_load_timeout": 30.0,
                "script_timeout": 30.0,
            },
            "test": {
                "default_timeout": 10.0,
                "retry_attempts": 3,
                "retry_delay": 1.0,
                "take_screenshot_on_failure": True,
                "capture_logs_on_failure": True,
                "parallel_execution": False,
                "max_workers": 4,
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "file_path": None,
                "max_file_size": 10 * 1024 * 1024,
                "backup_count": 5,
                "console_output": True,
            },
            "reporting": {
                "output_dir": str(Path.cwd() / "test_reports"),
                "html_report": True,
                "allure_report": True,
                "junit_xml": True,
                "screenshot_dir": str(Path.cwd() / "screenshots"),
            },
            "environment": {
                "name": "dev",
                "base_url": "",
                "api_base_url": "",
                "database_url": None,
            },
            "credentials": {
                "username": None,
                "password": None,
                "api_key": None,
                "token": None,
            },
            "custom": {},
        }

    def _load_toml_config(self) -> dict[str, Any] | None:
        """Load configuration from TOML file."""
        if tomllib is None:
            logger.warning(
                "TOML support not available. Install 'tomli' for Python < 3.11"
            )
            return None

        config_file = self._find_config_file()
        if not config_file:
            logger.debug("No TOML configuration file found")
            return None

        try:
            with open(config_file, "rb") as f:
                config = tomllib.load(f)
            logger.debug(f"Loaded TOML configuration from {config_file}")
            return config
        except Exception as e:
            logger.warning(f"Failed to load TOML config from {config_file}: {e}")
            return None

    def _find_config_file(self) -> Path | None:
        """Find the configuration file to use."""
        if self.config_path and self.config_path.exists():
            return self.config_path

        for path in self.DEFAULT_CONFIG_PATHS:
            if path.exists():
                return path

        return None

    def _load_env_config(self) -> dict[str, Any]:
        """Load configuration from environment variables."""
        config = {}

        # Map environment variables to config structure
        env_mappings = {
            f"{self.ENV_PREFIX}BROWSER_NAME": ("browser", "name"),
            f"{self.ENV_PREFIX}BROWSER_HEADLESS": ("browser", "headless"),
            f"{self.ENV_PREFIX}BROWSER_WIDTH": ("browser", "window_width"),
            f"{self.ENV_PREFIX}BROWSER_HEIGHT": ("browser", "window_height"),
            f"{self.ENV_PREFIX}WEBDRIVER_REMOTE_URL": ("webdriver", "remote_url"),
            f"{self.ENV_PREFIX}WEBDRIVER_PAGE_LOAD_TIMEOUT": (
                "webdriver",
                "page_load_timeout",
            ),
            f"{self.ENV_PREFIX}TEST_TIMEOUT": ("test", "default_timeout"),
            f"{self.ENV_PREFIX}TEST_RETRY_ATTEMPTS": ("test", "retry_attempts"),
            f"{self.ENV_PREFIX}TEST_PARALLEL": ("test", "parallel_execution"),
            f"{self.ENV_PREFIX}LOG_LEVEL": ("logging", "level"),
            f"{self.ENV_PREFIX}LOG_FILE": ("logging", "file_path"),
            f"{self.ENV_PREFIX}ENVIRONMENT": ("environment", "name"),
            f"{self.ENV_PREFIX}BASE_URL": ("environment", "base_url"),
            f"{self.ENV_PREFIX}API_BASE_URL": ("environment", "api_base_url"),
            f"{self.ENV_PREFIX}USERNAME": ("credentials", "username"),
            f"{self.ENV_PREFIX}PASSWORD": ("credentials", "password"),
            f"{self.ENV_PREFIX}API_KEY": ("credentials", "api_key"),
            f"{self.ENV_PREFIX}TOKEN": ("credentials", "token"),
        }

        for env_var, (section, key) in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                if section not in config:
                    config[section] = {}
                config[section][key] = self._convert_env_value(value, key)

        return config

    def _convert_env_value(self, value: str, key: str) -> Any:
        """Convert environment variable string to appropriate type."""
        # Boolean values
        if key in [
            "headless",
            "parallel_execution",
            "take_screenshot_on_failure",
            "capture_logs_on_failure",
            "html_report",
            "allure_report",
            "junit_xml",
            "console_output",
        ]:
            return value.lower() in ("true", "1", "yes", "on")

        # Integer values
        if key in [
            "window_width",
            "window_height",
            "retry_attempts",
            "max_workers",
            "max_file_size",
            "backup_count",
        ]:
            try:
                return int(value)
            except ValueError:
                logger.warning(f"Invalid integer value for {key}: {value}")
                return value

        # Float values
        if key in [
            "implicit_wait",
            "page_load_timeout",
            "script_timeout",
            "default_timeout",
            "retry_delay",
        ]:
            try:
                return float(value)
            except ValueError:
                logger.warning(f"Invalid float value for {key}: {value}")
                return value

        return value

    def _parse_cli_args(self, args: list[str]) -> argparse.Namespace:
        """Parse command line arguments."""
        parser = argparse.ArgumentParser(description="PMAS Test Framework")

        # Browser options
        parser.add_argument(
            "--browser",
            choices=["chrome", "firefox", "edge"],
            help="Browser to use for testing",
        )
        parser.add_argument(
            "--headless", action="store_true", help="Run browser in headless mode"
        )
        parser.add_argument("--remote-url", help="Selenium Grid remote URL")

        # Test options
        parser.add_argument("--timeout", type=float, help="Default timeout in seconds")
        parser.add_argument(
            "--retry-attempts", type=int, help="Number of retry attempts"
        )
        parser.add_argument(
            "--parallel", action="store_true", help="Enable parallel execution"
        )
        parser.add_argument("--max-workers", type=int, help="Maximum parallel workers")

        # Environment options
        parser.add_argument(
            "--environment",
            choices=["dev", "sat", "fat", "prod"],
            help="Test environment",
        )
        parser.add_argument("--base-url", help="Base URL for the application")

        # Logging options
        parser.add_argument(
            "--log-level",
            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            help="Logging level",
        )
        parser.add_argument("--log-file", help="Log file path")

        # Configuration file
        parser.add_argument("--config", help="Configuration file path")

        return parser.parse_args(args)

    def _cli_args_to_config(self) -> dict[str, Any]:
        """Convert CLI arguments to configuration dictionary."""
        if not self.cli_args:
            return {}

        config = {}

        # Browser configuration
        if self.cli_args.browser:
            config.setdefault("browser", {})["name"] = self.cli_args.browser
        if self.cli_args.headless:
            config.setdefault("browser", {})["headless"] = True

        # WebDriver configuration
        if self.cli_args.remote_url:
            config.setdefault("webdriver", {})["remote_url"] = self.cli_args.remote_url

        # Test configuration
        if self.cli_args.timeout:
            config.setdefault("test", {})["default_timeout"] = self.cli_args.timeout
        if self.cli_args.retry_attempts is not None:
            config.setdefault("test", {})["retry_attempts"] = (
                self.cli_args.retry_attempts
            )
        if self.cli_args.parallel:
            config.setdefault("test", {})["parallel_execution"] = True
        if self.cli_args.max_workers:
            config.setdefault("test", {})["max_workers"] = self.cli_args.max_workers

        # Environment configuration
        if self.cli_args.environment:
            config.setdefault("environment", {})["name"] = self.cli_args.environment
        if self.cli_args.base_url:
            config.setdefault("environment", {})["base_url"] = self.cli_args.base_url

        # Logging configuration
        if self.cli_args.log_level:
            config.setdefault("logging", {})["level"] = self.cli_args.log_level
        if self.cli_args.log_file:
            config.setdefault("logging", {})["file_path"] = self.cli_args.log_file

        return config

    def _merge_configs(
        self, base: dict[str, Any], override: dict[str, Any]
    ) -> dict[str, Any]:
        """Merge two configuration dictionaries, with override taking precedence."""
        result = base.copy()

        for key, value in override.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value

        return result

    def _dict_to_config(self, config_dict: dict[str, Any]) -> Config:
        """Convert configuration dictionary to Config object."""
        return Config(
            browser=BrowserConfig(**config_dict.get("browser", {})),
            webdriver=WebDriverConfig(**config_dict.get("webdriver", {})),
            test=TestingConfig(**config_dict.get("test", {})),
            logging=LoggingConfig(**config_dict.get("logging", {})),
            reporting=ReportingConfig(**config_dict.get("reporting", {})),
            environment=EnvironmentConfig(**config_dict.get("environment", {})),
            credentials=CredentialsConfig(**config_dict.get("credentials", {})),
            custom=config_dict.get("custom", {}),
        )

    def _get_config_sources(self) -> str:
        """Get a description of configuration sources used."""
        sources = []

        if self._find_config_file():
            sources.append(f"TOML file ({self._find_config_file()})")

        env_vars = [key for key in os.environ.keys() if key.startswith(self.ENV_PREFIX)]
        if env_vars:
            sources.append(f"Environment variables ({len(env_vars)} vars)")

        if self.cli_args:
            cli_args = [
                key for key, value in vars(self.cli_args).items() if value is not None
            ]
            if cli_args:
                sources.append(f"CLI arguments ({len(cli_args)} args)")

        return ", ".join(sources) if sources else "defaults only"


def load_config(
    config_path: str | Path | None = None, cli_args: list[str] | None = None
) -> Config:
    """
    Convenience function to load configuration.

    Args:
        config_path: Optional path to configuration file
        cli_args: Optional CLI arguments to parse

    Returns:
        Loaded and validated configuration
    """
    loader = ConfigLoader(config_path)
    return loader.load(cli_args)
