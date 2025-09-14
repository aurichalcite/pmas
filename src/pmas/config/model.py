"""
Configuration data model using modern Python patterns with validation.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal
from urllib.parse import urlparse

# Type aliases for better readability
BrowserType = Literal["chrome", "firefox", "edge"]
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
Environment = Literal["dev", "sat", "fat", "prod"]


@dataclass
class BrowserConfig:
    """Browser-specific configuration."""

    name: BrowserType = "chrome"
    headless: bool = False
    window_width: int = 1920
    window_height: int = 1080
    download_dir: Path | None = None
    additional_options: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate browser configuration."""
        if self.download_dir and isinstance(self.download_dir, str):
            self.download_dir = Path(self.download_dir)

        if self.window_width <= 0 or self.window_height <= 0:
            raise ValueError("Window dimensions must be positive")


@dataclass
class WebDriverConfig:
    """WebDriver configuration."""

    remote_url: str | None = None
    implicit_wait: float = 0.0  # We prefer explicit waits
    page_load_timeout: float = 30.0
    script_timeout: float = 30.0

    def __post_init__(self) -> None:
        """Validate WebDriver configuration."""
        if self.remote_url:
            parsed = urlparse(self.remote_url)
            if not parsed.scheme or not parsed.netloc:
                raise ValueError(f"Invalid remote URL: {self.remote_url}")

        if any(
            timeout < 0
            for timeout in [
                self.implicit_wait,
                self.page_load_timeout,
                self.script_timeout,
            ]
        ):
            raise ValueError("Timeout values must be non-negative")


@dataclass
class TestingConfig:
    """Test execution configuration."""

    default_timeout: float = 10.0
    retry_attempts: int = 3
    retry_delay: float = 1.0
    take_screenshot_on_failure: bool = True
    capture_logs_on_failure: bool = True
    parallel_execution: bool = False
    max_workers: int = 4

    def __post_init__(self) -> None:
        """Validate test configuration."""
        if self.default_timeout <= 0:
            raise ValueError("Default timeout must be positive")

        if self.retry_attempts < 0:
            raise ValueError("Retry attempts must be non-negative")

        if self.max_workers <= 0:
            raise ValueError("Max workers must be positive")


@dataclass
class LoggingConfig:
    """Logging configuration."""

    level: LogLevel = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: Path | None = None
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    console_output: bool = True

    def __post_init__(self) -> None:
        """Validate logging configuration."""
        if self.file_path and isinstance(self.file_path, str):
            self.file_path = Path(self.file_path)

        if self.max_file_size <= 0:
            raise ValueError("Max file size must be positive")

        if self.backup_count < 0:
            raise ValueError("Backup count must be non-negative")


@dataclass
class ReportingConfig:
    """Test reporting configuration."""

    output_dir: Path = field(default_factory=lambda: Path.cwd() / "test_reports")
    html_report: bool = True
    allure_report: bool = True
    junit_xml: bool = True
    screenshot_dir: Path = field(default_factory=lambda: Path.cwd() / "screenshots")

    def __post_init__(self) -> None:
        """Validate and normalize paths."""
        if isinstance(self.output_dir, str):
            self.output_dir = Path(self.output_dir)

        if isinstance(self.screenshot_dir, str):
            self.screenshot_dir = Path(self.screenshot_dir)


@dataclass
class EnvironmentConfig:
    """Environment-specific configuration."""

    name: Environment = "dev"
    base_url: str = ""
    api_base_url: str = ""
    database_url: str | None = None

    def __post_init__(self) -> None:
        """Validate environment configuration."""
        if self.base_url:
            parsed = urlparse(self.base_url)
            if not parsed.scheme or not parsed.netloc:
                raise ValueError(f"Invalid base URL: {self.base_url}")

        if self.api_base_url:
            parsed = urlparse(self.api_base_url)
            if not parsed.scheme or not parsed.netloc:
                raise ValueError(f"Invalid API base URL: {self.api_base_url}")


@dataclass
class CredentialsConfig:
    """Credentials configuration with security considerations."""

    username: str | None = None
    password: str | None = None
    api_key: str | None = None
    token: str | None = None

    def __post_init__(self) -> None:
        """Security validation and warnings."""
        # Check if credentials are loaded from environment variables
        if self.password and not self._is_from_env_var(self.password):
            import warnings

            warnings.warn(
                "Password appears to be hardcoded. Consider using environment variables.",
                UserWarning,
            )

        if self.api_key and not self._is_from_env_var(self.api_key):
            import warnings

            warnings.warn(
                "API key appears to be hardcoded. Consider using environment variables.",
                UserWarning,
            )

    @staticmethod
    def _is_from_env_var(value: str) -> bool:
        """Check if a value looks like it came from an environment variable."""
        # This is a simple heuristic - in practice, you might track this differently
        return value.startswith("${") and value.endswith("}")


@dataclass
class Config:
    """
    Main configuration class containing all framework settings.

    This class uses the dataclass pattern with validation to ensure
    configuration integrity and provide clear error messages.
    """

    browser: BrowserConfig = field(default_factory=BrowserConfig)
    webdriver: WebDriverConfig = field(default_factory=WebDriverConfig)
    test: TestingConfig = field(default_factory=TestingConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    reporting: ReportingConfig = field(default_factory=ReportingConfig)
    environment: EnvironmentConfig = field(default_factory=EnvironmentConfig)
    credentials: CredentialsConfig = field(default_factory=CredentialsConfig)

    # Additional custom settings
    custom: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Perform cross-field validation."""
        # Ensure screenshot directory is under reporting output directory
        if not self.reporting.screenshot_dir.is_absolute():
            self.reporting.screenshot_dir = (
                self.reporting.output_dir / self.reporting.screenshot_dir
            )

        # Set browser download directory if not specified
        if not self.browser.download_dir:
            self.browser.download_dir = self.reporting.output_dir / "downloads"

    @property
    def window_size(self) -> tuple[int, int]:
        """Get browser window size as a tuple."""
        return (self.browser.window_width, self.browser.window_height)

    def get_custom(self, key: str, default: Any = None) -> Any:
        """Get a custom configuration value."""
        return self.custom.get(key, default)

    def set_custom(self, key: str, value: Any) -> None:
        """Set a custom configuration value."""
        self.custom[key] = value

    def validate(self) -> list[str]:
        """
        Validate the entire configuration and return any errors.

        Returns:
            List of validation error messages
        """
        errors = []

        # Check required fields based on environment
        if not self.environment.base_url:
            errors.append("Base URL is required")

        if self.webdriver.remote_url and self.environment.name == "prod":
            # In production, we might want to ensure remote execution
            pass

        # Check for conflicting settings
        if self.browser.headless and self.test.take_screenshot_on_failure:
            import warnings

            warnings.warn(
                "Screenshots may not work properly in headless mode", UserWarning
            )

        return errors

    def to_dict(self) -> dict[str, Any]:
        """Convert configuration to dictionary format."""
        result = {}
        for field_name, field_value in self.__dict__.items():
            if hasattr(field_value, "__dict__"):
                # Convert dataclass fields to dict
                result[field_name] = field_value.__dict__.copy()
            else:
                result[field_name] = field_value
        return result

    def __str__(self) -> str:
        """String representation for debugging (without sensitive data)."""
        safe_dict = self.to_dict()

        # Remove sensitive information
        if "credentials" in safe_dict:
            creds = safe_dict["credentials"]
            for key in ["password", "api_key", "token"]:
                if key in creds and creds[key]:
                    creds[key] = "***REDACTED***"

        return f"Config({safe_dict})"
