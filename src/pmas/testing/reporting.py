"""
Test reporting and failure artifact capture.
"""

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import pytest

from ..config.model import Config
from ..core.utils.file_utils import ensure_directory, safe_filename

logger = logging.getLogger(__name__)


def setup_reporting(config: Config) -> None:
    """
    Set up test reporting based on configuration.

    Args:
        config: Framework configuration
    """
    # Ensure output directories exist
    ensure_directory(config.reporting.output_dir)
    ensure_directory(config.reporting.screenshot_dir)

    # Configure logging
    setup_test_logging(config.logging)

    logger.info(f"Test reporting configured: {config.reporting.output_dir}")


def setup_test_logging(logging_config) -> None:
    """Set up logging configuration for tests."""
    import logging.handlers

    # Set the root logger level
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, logging_config.level))

    # Clear existing handlers
    root_logger.handlers.clear()

    # Console handler
    if logging_config.console_output:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, logging_config.level))
        formatter = logging.Formatter(logging_config.format)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

    # File handler
    if logging_config.file_path:
        ensure_directory(Path(logging_config.file_path).parent)
        file_handler = logging.handlers.RotatingFileHandler(
            logging_config.file_path,
            maxBytes=logging_config.max_file_size,
            backupCount=logging_config.backup_count,
        )
        file_handler.setLevel(getattr(logging, logging_config.level))
        formatter = logging.Formatter(logging_config.format)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)


def capture_failure_artifacts(
    driver, config: Config, request: pytest.FixtureRequest
) -> dict[str, str]:
    """
    Capture artifacts when a test fails.

    Args:
        driver: WebDriver instance
        config: Framework configuration
        request: Pytest request object

    Returns:
        Dictionary of captured artifact paths
    """
    artifacts = {}

    if not (
        config.test.take_screenshot_on_failure or config.test.capture_logs_on_failure
    ):
        return artifacts

    # Generate safe filename based on test name
    test_name = safe_filename(request.node.name)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_filename = f"{test_name}_{timestamp}"

    try:
        # Capture screenshot
        if config.test.take_screenshot_on_failure:
            screenshot_path = capture_screenshot(driver, config, base_filename)
            if screenshot_path:
                artifacts["screenshot"] = str(screenshot_path)

        # Capture browser logs
        if config.test.capture_logs_on_failure:
            logs_path = capture_browser_logs(driver, config, base_filename)
            if logs_path:
                artifacts["browser_logs"] = str(logs_path)

        # Capture page source
        page_source_path = capture_page_source(driver, config, base_filename)
        if page_source_path:
            artifacts["page_source"] = str(page_source_path)

        # Capture test metadata
        metadata_path = capture_test_metadata(config, request, base_filename, artifacts)
        if metadata_path:
            artifacts["metadata"] = str(metadata_path)

        logger.info(f"Captured failure artifacts: {list(artifacts.keys())}")

    except Exception as e:
        logger.error(f"Failed to capture failure artifacts: {e}")

    return artifacts


def capture_screenshot(driver, config: Config, base_filename: str) -> Path | None:
    """Capture a screenshot of the current page."""
    try:
        screenshot_path = config.reporting.screenshot_dir / f"{base_filename}.png"
        success = driver.get_screenshot_as_file(str(screenshot_path))

        if success:
            logger.debug(f"Screenshot captured: {screenshot_path}")
            return screenshot_path
        else:
            logger.warning("Failed to capture screenshot")
            return None

    except Exception as e:
        logger.error(f"Error capturing screenshot: {e}")
        return None


def capture_browser_logs(driver, config: Config, base_filename: str) -> Path | None:
    """Capture browser console logs."""
    try:
        logs_path = config.reporting.output_dir / f"{base_filename}_browser_logs.json"

        # Get different types of logs
        log_types = ["browser", "driver", "client", "server"]
        all_logs = {}

        for log_type in log_types:
            try:
                logs = driver.get_log(log_type)
                if logs:
                    all_logs[log_type] = logs
            except Exception as e:
                logger.debug(f"Could not get {log_type} logs: {e}")

        if all_logs:
            with open(logs_path, "w") as f:
                json.dump(all_logs, f, indent=2, default=str)

            logger.debug(f"Browser logs captured: {logs_path}")
            return logs_path

    except Exception as e:
        logger.error(f"Error capturing browser logs: {e}")

    return None


def capture_page_source(driver, config: Config, base_filename: str) -> Path | None:
    """Capture the current page source."""
    try:
        source_path = config.reporting.output_dir / f"{base_filename}_page_source.html"

        page_source = driver.page_source
        with open(source_path, "w", encoding="utf-8") as f:
            f.write(page_source)

        logger.debug(f"Page source captured: {source_path}")
        return source_path

    except Exception as e:
        logger.error(f"Error capturing page source: {e}")
        return None


def capture_test_metadata(
    config: Config,
    request: pytest.FixtureRequest,
    base_filename: str,
    artifacts: dict[str, str],
) -> Path | None:
    """Capture test metadata and context information."""
    try:
        metadata_path = config.reporting.output_dir / f"{base_filename}_metadata.json"

        metadata = {
            "test_name": request.node.name,
            "test_file": str(request.node.fspath),
            "test_function": request.function.__name__
            if hasattr(request, "function")
            else None,
            "timestamp": datetime.now().isoformat(),
            "browser": config.browser.name,
            "environment": config.environment.name,
            "base_url": config.environment.base_url,
            "artifacts": artifacts,
            "config_summary": {
                "browser": config.browser.name,
                "headless": config.browser.headless,
                "window_size": config.window_size,
                "timeout": config.test.default_timeout,
                "retry_attempts": config.test.retry_attempts,
            },
        }

        # Add test parameters if available
        if hasattr(request, "param"):
            metadata["test_parameters"] = request.param

        # Add markers
        if request.node.iter_markers():
            metadata["markers"] = [
                marker.name for marker in request.node.iter_markers()
            ]

        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2, default=str)

        logger.debug(f"Test metadata captured: {metadata_path}")
        return metadata_path

    except Exception as e:
        logger.error(f"Error capturing test metadata: {e}")
        return None


class TestReporter:
    """Enhanced test reporter for collecting and organizing test results."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self.test_results: list[dict[str, Any]] = []
        self.start_time = time.time()

    def add_test_result(
        self,
        test_name: str,
        status: str,
        duration: float,
        error_message: str | None = None,
        artifacts: dict[str, str] | None = None,
    ) -> None:
        """Add a test result to the collection."""
        result = {
            "test_name": test_name,
            "status": status,
            "duration": duration,
            "timestamp": datetime.now().isoformat(),
            "error_message": error_message,
            "artifacts": artifacts or {},
        }
        self.test_results.append(result)

    def generate_summary_report(self) -> dict[str, Any]:
        """Generate a summary report of all test results."""
        total_tests = len(self.test_results)
        passed = len([r for r in self.test_results if r["status"] == "passed"])
        failed = len([r for r in self.test_results if r["status"] == "failed"])
        skipped = len([r for r in self.test_results if r["status"] == "skipped"])

        total_duration = sum(r["duration"] for r in self.test_results)
        execution_time = time.time() - self.start_time

        summary = {
            "execution_summary": {
                "total_tests": total_tests,
                "passed": passed,
                "failed": failed,
                "skipped": skipped,
                "success_rate": (passed / total_tests * 100) if total_tests > 0 else 0,
                "total_duration": total_duration,
                "execution_time": execution_time,
            },
            "environment": {
                "browser": self.config.browser.name,
                "environment": self.config.environment.name,
                "base_url": self.config.environment.base_url,
            },
            "test_results": self.test_results,
            "generated_at": datetime.now().isoformat(),
        }

        return summary

    def save_summary_report(self, filename: str | None = None) -> Path:
        """Save the summary report to a file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_summary_{timestamp}.json"

        report_path = self.config.reporting.output_dir / filename
        summary = self.generate_summary_report()

        with open(report_path, "w") as f:
            json.dump(summary, f, indent=2, default=str)

        logger.info(f"Test summary report saved: {report_path}")
        return report_path


# Pytest hooks for automatic reporting
def pytest_configure(config):
    """Configure pytest with custom reporting."""
    # This would be called automatically by pytest
    pass


def pytest_runtest_logreport(report):
    """Log test reports."""
    if report.when == "call":
        status = "passed" if report.passed else "failed" if report.failed else "skipped"
        logger.info(f"Test {report.nodeid}: {status} ({report.duration:.2f}s)")


def pytest_sessionfinish(session, exitstatus):
    """Called after whole test run finished."""
    logger.info(f"Test session finished with exit status: {exitstatus}")


# Allure integration helpers
def attach_allure_artifacts(artifacts: dict[str, str]) -> None:
    """Attach artifacts to Allure report if available."""
    try:
        import allure

        for artifact_type, artifact_path in artifacts.items():
            if artifact_type == "screenshot":
                allure.attach.file(
                    artifact_path,
                    name="Screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )
            elif artifact_type == "page_source":
                allure.attach.file(
                    artifact_path,
                    name="Page Source",
                    attachment_type=allure.attachment_type.HTML,
                )
            elif artifact_type == "browser_logs":
                allure.attach.file(
                    artifact_path,
                    name="Browser Logs",
                    attachment_type=allure.attachment_type.JSON,
                )

    except ImportError:
        # Allure not available
        pass
    except Exception as e:
        logger.warning(f"Failed to attach Allure artifacts: {e}")
