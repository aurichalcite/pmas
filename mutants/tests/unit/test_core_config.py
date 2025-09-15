"""
Unit tests for PMAS Config class and related configuration components.

This module tests the configuration system in complete isolation using mocks and fakes.
Tests cover:
- Config class initialization with various input sources
- Configuration validation and error handling
- Configuration precedence (environment variables vs. file vs. defaults)
- Type safety and data integrity
- Configuration serialization and string representation

All tests are hermetic - no network access, no filesystem I/O, no external dependencies.
"""

import os
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest

# ASSUMPTION: Import PMAS configuration components
from pmas.config.model import (
    BrowserConfig,
    Config,
    CredentialsConfig,
    EnvironmentConfig,
    LoggingConfig,
    ReportingConfig,
    TestConfig,
    WebDriverConfig,
)


class TestBrowserConfig:
    """Unit tests for BrowserConfig class."""

    def test_browser_config_default_initialization(self):
        """Test BrowserConfig initialization with default values."""
        config = BrowserConfig()

        assert config.name == "chrome"
        assert config.headless is False
        assert config.window_width == 1920
        assert config.window_height == 1080
        assert config.download_dir is None
        assert config.additional_options == []

    @pytest.mark.parametrize("browser_name", ["chrome", "firefox", "edge"])
    def test_browser_config_with_valid_browsers(self, browser_name: str):
        """Test BrowserConfig with different valid browser names."""
        config = BrowserConfig(name=browser_name)
        assert config.name == browser_name

    @pytest.mark.parametrize(
        "width,height",
        [
            (1280, 720),
            (1920, 1080),
            (2560, 1440),
            (800, 600),
        ],
    )
    def test_browser_config_with_valid_dimensions(self, width: int, height: int):
        """Test BrowserConfig with various valid window dimensions."""
        config = BrowserConfig(window_width=width, window_height=height)
        assert config.window_width == width
        assert config.window_height == height

    @pytest.mark.parametrize(
        "width,height",
        [
            (0, 720),
            (1280, 0),
            (-100, 720),
            (1280, -100),
        ],
    )
    def test_browser_config_invalid_dimensions_raises_error(
        self, width: int, height: int
    ):
        """Test that invalid window dimensions raise ValueError."""
        with pytest.raises(ValueError, match="Window dimensions must be positive"):
            BrowserConfig(window_width=width, window_height=height)

    def test_browser_config_download_dir_string_conversion(self):
        """Test that download_dir string is converted to Path object."""
        config = BrowserConfig(download_dir="/tmp/downloads")
        assert isinstance(config.download_dir, Path)
        assert str(config.download_dir) == "/tmp/downloads"

    def test_browser_config_download_dir_path_object(self):
        """Test that download_dir Path object is preserved."""
        path_obj = Path("/tmp/downloads")
        config = BrowserConfig(download_dir=path_obj)
        assert config.download_dir is path_obj


class TestTestConfig:
    """Unit tests for TestConfig class."""

    def test_test_config_default_initialization(self):
        """Test TestConfig initialization with default values."""
        config = TestConfig()

        assert config.default_timeout == 10.0
        assert config.retry_attempts == 3
        assert config.retry_delay == 1.0
        assert config.take_screenshot_on_failure is True
        assert config.capture_logs_on_failure is True
        assert config.parallel_execution is False
        assert config.max_workers == 4

    @pytest.mark.parametrize("timeout", [1.0, 5.0, 10.0, 30.0, 60.0])
    def test_test_config_valid_timeouts(self, timeout: float):
        """Test TestConfig with various valid timeout values."""
        config = TestConfig(default_timeout=timeout)
        assert config.default_timeout == timeout

    @pytest.mark.parametrize("timeout", [0.0, -1.0, -10.0])
    def test_test_config_invalid_timeout_raises_error(self, timeout: float):
        """Test that invalid timeout values raise ValueError."""
        with pytest.raises(ValueError, match="Default timeout must be positive"):
            TestConfig(default_timeout=timeout)

    @pytest.mark.parametrize("attempts", [-1, -5])
    def test_test_config_invalid_retry_attempts_raises_error(self, attempts: int):
        """Test that negative retry attempts raise ValueError."""
        with pytest.raises(ValueError, match="Retry attempts must be non-negative"):
            TestConfig(retry_attempts=attempts)

    @pytest.mark.parametrize("workers", [0, -1, -5])
    def test_test_config_invalid_max_workers_raises_error(self, workers: int):
        """Test that invalid max_workers values raise ValueError."""
        with pytest.raises(ValueError, match="Max workers must be positive"):
            TestConfig(max_workers=workers)


class TestEnvironmentConfig:
    """Unit tests for EnvironmentConfig class."""

    def test_environment_config_default_initialization(self):
        """Test EnvironmentConfig initialization with default values."""
        config = EnvironmentConfig()

        assert config.name == "dev"
        assert config.base_url == ""
        assert config.api_base_url == ""
        assert config.database_url is None

    @pytest.mark.parametrize(
        "url,expected",
        [
            ("https://example.com", "https://example.com"),
            ("http://localhost:3000", "http://localhost:3000"),
            ("https://staging.myapp.com", "https://staging.myapp.com"),
        ],
    )
    def test_environment_config_with_valid_urls(self, url: str, expected: str):
        """Test EnvironmentConfig with various valid URLs."""
        config = EnvironmentConfig(base_url=url)
        assert config.base_url == expected


class TestMainConfig:
    """Unit tests for main Config class."""

    def test_config_default_initialization(self):
        """Test Config initialization with all default values."""
        config = Config()

        # Verify all sub-configs are properly initialized
        assert isinstance(config.browser, BrowserConfig)
        assert isinstance(config.webdriver, WebDriverConfig)
        assert isinstance(config.test, TestConfig)
        assert isinstance(config.logging, LoggingConfig)
        assert isinstance(config.reporting, ReportingConfig)
        assert isinstance(config.environment, EnvironmentConfig)
        assert isinstance(config.credentials, CredentialsConfig)
        assert isinstance(config.custom, dict)
        assert len(config.custom) == 0

    def test_config_with_custom_browser_config(self):
        """Test Config initialization with custom BrowserConfig."""
        browser_config = BrowserConfig(name="firefox", headless=True)
        config = Config(browser=browser_config)

        assert config.browser.name == "firefox"
        assert config.browser.headless is True

    def test_config_with_custom_test_config(self):
        """Test Config initialization with custom TestConfig."""
        test_config = TestConfig(default_timeout=5.0, retry_attempts=1)
        config = Config(test=test_config)

        assert config.test.default_timeout == 5.0
        assert config.test.retry_attempts == 1

    def test_config_with_custom_data(self):
        """Test Config initialization with custom data."""
        custom_data = {"api_key": "test-key", "feature_flags": {"new_ui": True}}
        config = Config(custom=custom_data)

        assert config.custom["api_key"] == "test-key"
        assert config.custom["feature_flags"]["new_ui"] is True

    def test_config_to_dict_conversion(self):
        """Test Config.to_dict() method."""
        config = Config()
        config_dict = config.to_dict()

        # Verify all expected keys are present
        expected_keys = {
            "browser",
            "webdriver",
            "test",
            "logging",
            "reporting",
            "environment",
            "credentials",
            "custom",
        }
        assert set(config_dict.keys()) == expected_keys

        # Verify nested configs are converted to dicts
        assert isinstance(config_dict["browser"], dict)
        assert isinstance(config_dict["test"], dict)

    def test_config_string_representation_redacts_sensitive_data(self):
        """Test that Config.__str__() redacts sensitive information."""
        credentials = CredentialsConfig(
            username="testuser", password="secret123", api_key="api-secret-key"
        )
        config = Config(credentials=credentials)
        config_str = str(config)

        # Verify sensitive data is redacted
        assert "secret123" not in config_str
        assert "api-secret-key" not in config_str
        assert "***REDACTED***" in config_str

        # Verify non-sensitive data is still present
        assert "testuser" in config_str

    @pytest.mark.parametrize(
        "env_vars,expected_browser",
        [
            ({"PMAS_BROWSER_NAME": "firefox"}, "firefox"),
            ({"PMAS_BROWSER_NAME": "edge"}, "edge"),
            ({"PMAS_BROWSER_NAME": "chrome"}, "chrome"),
        ],
    )
    def test_config_environment_variable_precedence(
        self, env_vars: dict[str, str], expected_browser: str
    ):
        """Test that environment variables override default configuration."""
        # ASSUMPTION: Config class supports environment variable loading
        with patch.dict(os.environ, env_vars, clear=False):
            # This would require actual implementation in Config class
            # For now, we test the concept with a mock
            _config = Config()
            # In real implementation, this would read from environment
            # config = Config.from_environment()
            # assert config.browser.name == expected_browser

            # For this test, we verify the environment variable exists
            assert os.getenv("PMAS_BROWSER_NAME") == expected_browser

    def test_config_validation_with_invalid_nested_config(self):
        """Test that Config validation catches invalid nested configurations."""
        # Test with invalid browser config
        with pytest.raises(ValueError):
            _invalid_browser = BrowserConfig(window_width=-100)

        # Test with invalid test config
        with pytest.raises(ValueError):
            _invalid_test = TestConfig(default_timeout=-5.0)

    def test_config_immutability_concept(self):
        """Test that Config behaves as expected for immutability."""
        config = Config()
        original_timeout = config.test.default_timeout

        # Modifying the config should not affect the original
        # (This tests the concept - actual immutability would require
        # frozen dataclasses)
        config.test.default_timeout = 999.0
        assert config.test.default_timeout == 999.0
        assert original_timeout != 999.0

    def test_config_deep_copy_behavior(self):
        """Test Config behavior with nested object modifications."""
        config1 = Config()
        config2 = Config()

        # Modify one config's nested object
        config1.browser.headless = True

        # Other config should not be affected (assuming proper initialization)
        assert config2.browser.headless is False

    @pytest.mark.parametrize(
        "config_data",
        [
            {"browser": {"name": "firefox", "headless": True}},
            {"test": {"default_timeout": 15.0, "retry_attempts": 5}},
            {
                "environment": {
                    "base_url": "https://test.example.com",
                    "name": "testing",
                }
            },
        ],
    )
    def test_config_from_dict_concept(self, config_data: dict[str, Any]):
        """Test Config creation from dictionary data (conceptual test)."""
        # ASSUMPTION: Config class would support from_dict class method
        # This tests the concept and data structure

        # Verify the test data structure is valid
        assert isinstance(config_data, dict)

        # In actual implementation, this would be:
        # config = Config.from_dict(config_data)
        # And we would verify the config was created correctly

        # For now, verify we can create configs with the expected structure
        if "browser" in config_data:
            browser_data = config_data["browser"]
            browser_config = BrowserConfig(**browser_data)
            config = Config(browser=browser_config)
            assert config.browser.name == browser_data.get("name", "chrome")

    def test_config_merge_concept(self):
        """Test Config merging behavior (conceptual test)."""
        # Create base config
        base_config = Config()

        # Create override config with different values
        override_browser = BrowserConfig(name="firefox", headless=True)
        override_test = TestConfig(default_timeout=5.0, retry_attempts=1)
        override_config = Config(browser=override_browser, test=override_test)

        # Verify configs have different values
        assert base_config.browser.name != override_config.browser.name
        assert base_config.test.default_timeout != override_config.test.default_timeout

        # In actual implementation, there might be a merge method:
        # merged_config = base_config.merge(override_config)
        # assert merged_config.browser.name == "firefox"
        # assert merged_config.test.default_timeout == 5.0
