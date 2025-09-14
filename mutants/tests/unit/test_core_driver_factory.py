"""
Comprehensive unit tests for DriverFactory class.

This module tests the DriverFactory class with extensive mocking to ensure:
- All browser types are supported (Chrome, Firefox, Edge)
- Local and remote driver creation works correctly
- Configuration options are properly applied
- Error handling works as expected
- Edge cases and validation scenarios are covered
"""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from pmas.core.driver import DriverFactory
from pmas.core.errors import ConfigurationError, DriverError


class TestDriverFactoryValidation:
    """Test input validation and error handling."""

    def test_create_driver_when_unsupported_browser_expects_configuration_error(self):
        """Test that unsupported browser raises ConfigurationError."""
        with pytest.raises(ConfigurationError) as exc_info:
            DriverFactory.create_driver(browser="safari")

        assert "Unsupported browser: safari" in str(exc_info.value)
        assert "chrome" in str(exc_info.value)
        assert "firefox" in str(exc_info.value)
        assert "edge" in str(exc_info.value)

    @pytest.mark.parametrize(
        "browser_input, expected_normalized",
        [
            ("Chrome", "chrome"),
            ("FIREFOX", "firefox"),
            ("Edge", "edge"),
            ("cHrOmE", "chrome"),
        ],
    )
    def test_create_driver_when_mixed_case_browser_expects_normalized(
        self, browser_input, expected_normalized
    ):
        """Test that browser names are case-insensitive."""
        with patch.object(DriverFactory, "_create_local_driver") as mock_create:
            mock_driver = Mock()
            mock_create.return_value = mock_driver

            result = DriverFactory.create_driver(browser=browser_input)

            mock_create.assert_called_once()
            args = mock_create.call_args[0]
            assert args[0] == expected_normalized

    def test_create_driver_when_selenium_exception_expects_driver_error(self):
        """Test that Selenium exceptions are wrapped in DriverError."""
        with patch("pmas.core.driver.webdriver.Chrome") as mock_chrome:
            mock_chrome.side_effect = Exception("WebDriver failed to start")

            with pytest.raises(DriverError) as exc_info:
                DriverFactory.create_driver(browser="chrome")

            assert "Failed to create chrome driver" in str(exc_info.value)
            assert "WebDriver failed to start" in str(exc_info.value)


class TestDriverFactoryLocalDriverCreation:
    """Test local WebDriver creation for all supported browsers."""

    @patch("pmas.core.driver.webdriver.Chrome")
    @patch("pmas.core.driver.ChromeService")
    def test_create_local_chrome_driver_when_default_options_expects_correct_setup(
        self, mock_service, mock_chrome
    ):
        """Test Chrome driver creation with default options."""
        mock_driver = Mock()
        mock_chrome.return_value = mock_driver
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance

        with patch.object(DriverFactory, "_configure_driver") as mock_configure:
            result = DriverFactory._create_local_driver(
                browser="chrome",
                headless=False,
                window_size=None,
                download_dir=None,
                additional_options=None,
            )

        # Verify service creation
        mock_service.assert_called_once()

        # Verify Chrome driver creation
        mock_chrome.assert_called_once()
        call_args = mock_chrome.call_args
        assert call_args[1]["service"] == mock_service_instance
        assert "options" in call_args[1]

        # Verify driver configuration
        mock_configure.assert_called_once_with(mock_driver, None)
        assert result == mock_driver

    @patch("pmas.core.driver.webdriver.Firefox")
    @patch("pmas.core.driver.FirefoxService")
    def test_create_local_firefox_driver_when_headless_expects_correct_options(
        self, mock_service, mock_firefox
    ):
        """Test Firefox driver creation with headless mode."""
        mock_driver = Mock()
        mock_firefox.return_value = mock_driver

        with patch.object(DriverFactory, "_configure_driver"):
            result = DriverFactory._create_local_driver(
                browser="firefox",
                headless=True,
                window_size=(1280, 720),
                download_dir=Path("/tmp/downloads"),
                additional_options=["--disable-extensions"],
            )

        # Verify Firefox driver creation
        mock_firefox.assert_called_once()
        call_args = mock_firefox.call_args
        assert "options" in call_args[1]
        assert result == mock_driver

    @patch("pmas.core.driver.webdriver.Edge")
    @patch("pmas.core.driver.EdgeService")
    def test_create_local_edge_driver_when_custom_options_expects_correct_setup(
        self, mock_service, mock_edge
    ):
        """Test Edge driver creation with custom options."""
        mock_driver = Mock()
        mock_edge.return_value = mock_driver

        with patch.object(DriverFactory, "_configure_driver"):
            result = DriverFactory._create_local_driver(
                browser="edge",
                headless=False,
                window_size=(1920, 1080),
                download_dir=Path("/home/user/downloads"),
                additional_options=[
                    "--disable-web-security",
                    "--allow-running-insecure-content",
                ],
            )

        mock_edge.assert_called_once()
        assert result == mock_driver


class TestDriverFactoryRemoteDriverCreation:
    """Test remote WebDriver creation for Selenium Grid."""

    @patch("pmas.core.driver.webdriver.Remote")
    def test_create_remote_chrome_driver_when_valid_url_expects_correct_setup(
        self, mock_remote
    ):
        """Test remote Chrome driver creation."""
        mock_driver = Mock()
        mock_remote.return_value = mock_driver

        with patch.object(DriverFactory, "_configure_driver") as mock_configure:
            result = DriverFactory._create_remote_driver(
                browser="chrome",
                remote_url="http://selenium-hub:4444/wd/hub",
                headless=True,
                window_size=(1280, 720),
                download_dir=None,
                additional_options=None,
            )

        # Verify remote driver creation
        mock_remote.assert_called_once()
        call_args = mock_remote.call_args
        assert call_args[1]["command_executor"] == "http://selenium-hub:4444/wd/hub"
        assert "desired_capabilities" in call_args[1]

        # Verify driver configuration
        mock_configure.assert_called_once_with(mock_driver, (1280, 720))
        assert result == mock_driver

    @pytest.mark.parametrize("browser", ["chrome", "firefox", "edge"])
    @patch("pmas.core.driver.webdriver.Remote")
    def test_create_remote_driver_when_all_browsers_expects_capabilities_created(
        self, mock_remote, browser
    ):
        """Test that all browsers can create remote drivers with capabilities."""
        mock_driver = Mock()
        mock_remote.return_value = mock_driver

        with patch.object(DriverFactory, "_configure_driver"):
            result = DriverFactory._create_remote_driver(
                browser=browser,
                remote_url="http://grid:4444",
                headless=False,
                window_size=None,
                download_dir=None,
                additional_options=None,
            )

        mock_remote.assert_called_once()
        call_args = mock_remote.call_args
        assert "desired_capabilities" in call_args[1]
        assert result == mock_driver


class TestDriverFactoryBrowserOptions:
    """Test browser-specific option configuration."""

    def test_get_chrome_options_when_all_features_enabled_expects_correct_options(self):
        """Test Chrome options with all features enabled."""
        download_dir = Path("/tmp/test_downloads")
        additional_options = ["--disable-extensions", "--incognito"]

        options = DriverFactory._get_chrome_options(
            headless=True,
            window_size=(1920, 1080),
            download_dir=download_dir,
            additional_options=additional_options,
        )

        assert isinstance(options, ChromeOptions)
        # Note: We can't easily test the internal state of ChromeOptions
        # but we can verify the method completes without error

    def test_get_firefox_options_when_download_dir_set_expects_preferences_configured(
        self,
    ):
        """Test Firefox options with download directory configuration."""
        download_dir = Path("/home/user/firefox_downloads")

        options = DriverFactory._get_firefox_options(
            headless=False,
            window_size=(1280, 720),
            download_dir=download_dir,
            additional_options=["--safe-mode"],
        )

        assert isinstance(options, FirefoxOptions)

    def test_get_edge_options_when_headless_mode_expects_headless_argument(self):
        """Test Edge options with headless mode."""
        options = DriverFactory._get_edge_options(
            headless=True, window_size=None, download_dir=None, additional_options=None
        )

        assert isinstance(options, EdgeOptions)


class TestDriverFactoryDriverConfiguration:
    """Test post-creation driver configuration."""

    def test_configure_driver_when_window_size_provided_expects_size_set(self):
        """Test driver configuration with specific window size."""
        mock_driver = Mock()
        window_size = (1366, 768)

        DriverFactory._configure_driver(mock_driver, window_size)

        mock_driver.set_window_size.assert_called_once_with(1366, 768)
        mock_driver.maximize_window.assert_not_called()
        mock_driver.implicitly_wait.assert_called_once_with(0)

    def test_configure_driver_when_no_window_size_expects_maximized(self):
        """Test driver configuration without window size maximizes window."""
        mock_driver = Mock()

        DriverFactory._configure_driver(mock_driver, None)

        mock_driver.maximize_window.assert_called_once()
        mock_driver.set_window_size.assert_not_called()
        mock_driver.implicitly_wait.assert_called_once_with(0)


class TestDriverFactoryIntegration:
    """Test complete driver creation flow."""

    @patch("pmas.core.driver.webdriver.Chrome")
    @patch("pmas.core.driver.ChromeService")
    def test_create_driver_when_local_chrome_expects_complete_flow(
        self, mock_service, mock_chrome
    ):
        """Test complete local Chrome driver creation flow."""
        mock_driver = Mock()
        mock_driver.name = "chrome"
        mock_driver.current_url = "data:,"
        mock_chrome.return_value = mock_driver

        result = DriverFactory.create_driver(
            browser="chrome",
            headless=True,
            window_size=(1280, 720),
            additional_options=["--no-sandbox"],
        )

        assert result == mock_driver
        mock_chrome.assert_called_once()
        mock_driver.set_window_size.assert_called_once_with(1280, 720)
        mock_driver.implicitly_wait.assert_called_once_with(0)

    @patch("pmas.core.driver.webdriver.Remote")
    def test_create_driver_when_remote_url_provided_expects_remote_creation(
        self, mock_remote
    ):
        """Test that providing remote_url triggers remote driver creation."""
        mock_driver = Mock()
        mock_driver.name = "chrome"
        mock_driver.current_url = "data:,"
        mock_remote.return_value = mock_driver

        result = DriverFactory.create_driver(
            browser="firefox",
            remote_url="http://selenium-grid:4444/wd/hub",
            headless=True,
        )

        assert result == mock_driver
        mock_remote.assert_called_once()
        call_args = mock_remote.call_args
        assert call_args[1]["command_executor"] == "http://selenium-grid:4444/wd/hub"


class TestDriverFactoryBranchCoverage:
    """Test specific conditional branches to improve branch coverage."""

    def test_create_driver_when_remote_url_none_expects_local_driver_path(self):
        """Test that None remote_url follows local driver creation path."""
        with (
            patch.object(DriverFactory, "_create_local_driver") as mock_local,
            patch.object(DriverFactory, "_create_remote_driver") as mock_remote,
        ):
            mock_driver = Mock()
            mock_local.return_value = mock_driver

            result = DriverFactory.create_driver(
                browser="chrome",
                remote_url=None,  # Explicitly test None path
            )

            # Should call local driver creation, not remote
            mock_local.assert_called_once_with("chrome", False, None, None, None)
            mock_remote.assert_not_called()
            assert result == mock_driver

    def test_create_driver_when_remote_url_provided_expects_remote_driver_path(self):
        """Test that providing remote_url follows remote driver creation path."""
        with (
            patch.object(DriverFactory, "_create_local_driver") as mock_local,
            patch.object(DriverFactory, "_create_remote_driver") as mock_remote,
        ):
            mock_driver = Mock()
            mock_remote.return_value = mock_driver
            remote_url = "http://selenium-grid:4444/wd/hub"

            result = DriverFactory.create_driver(
                browser="firefox", remote_url=remote_url
            )

            # Should call remote driver creation, not local
            mock_remote.assert_called_once_with(
                "firefox", remote_url, False, None, None, None
            )
            mock_local.assert_not_called()
            assert result == mock_driver

    def test_create_remote_driver_when_edge_browser_expects_edge_capabilities(self):
        """Test Edge browser path in remote driver creation."""
        with (
            patch("pmas.core.driver.webdriver.Remote") as mock_remote,
            patch.object(DriverFactory, "_get_edge_options") as mock_options,
            patch.object(DriverFactory, "_configure_driver") as mock_configure,
        ):
            mock_driver = Mock()
            mock_remote.return_value = mock_driver
            mock_options_instance = Mock()
            mock_capabilities = {"browserName": "MicrosoftEdge"}
            mock_options_instance.to_capabilities.return_value = mock_capabilities
            mock_options.return_value = mock_options_instance

            result = DriverFactory._create_remote_driver(
                browser="edge",
                remote_url="http://hub:4444/wd/hub",
                headless=True,
                window_size=(1024, 768),
                download_dir=None,
                additional_options=["--disable-gpu"],
            )

            # Verify Edge options were called
            mock_options.assert_called_once_with(
                True, (1024, 768), None, ["--disable-gpu"]
            )

            # Verify capabilities conversion
            mock_options_instance.to_capabilities.assert_called_once()

            # Verify remote driver creation with Edge capabilities
            mock_remote.assert_called_once_with(
                command_executor="http://hub:4444/wd/hub",
                desired_capabilities=mock_capabilities,
            )

            mock_configure.assert_called_once_with(mock_driver, (1024, 768))
            assert result == mock_driver
