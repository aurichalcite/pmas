"""
Base page class for aviation domain with common aviation-specific functionality.
"""

import logging

from ....core.page import BasePage
from ..constants import ARINC_DIRECT_TITLES

logger = logging.getLogger(__name__)


class BaseAviationPage(BasePage):
    """
    Base page class for all aviation domain pages.
    Provides aviation-specific functionality and navigation patterns.
    """

    expected_titles = ARINC_DIRECT_TITLES

    def __init__(self, driver, base_url: str = "", timeout: float = 10.0) -> None:
        super().__init__(driver, base_url, timeout)
        self.page_errors: dict[str, list] = {}
        self.page_notes: dict[str, list] = {}

    def log_note(self, text: str) -> None:
        """Log decisions made by the test, to be printed when test ends."""
        page_type = str(type(self))
        if page_type not in self.page_notes:
            self.page_notes[page_type] = []
        self.page_notes[page_type].append(text)
        logger.info(f"##### {text}")

    def add_error_text(self, text: str | None, screenshot: bool = True) -> None:
        """Print and add one error: 1 text string + make screenshot."""
        page_type = str(type(self))
        if page_type not in self.page_errors:
            self.page_errors[page_type] = []

        if not text:
            return  # just added page type to errors (to list visited pages)

        self.page_errors[page_type].append(text)
        logger.error(f"Page error: {text}")

        if screenshot:
            try:
                screenshot_path = self.take_screenshot()
                logger.info(f"Error screenshot saved: {screenshot_path}")
            except Exception as e:
                logger.warning(f"Failed to take error screenshot: {e}")

    def get_logged_user(self) -> tuple[str, str]:
        """
        Get the currently logged in user information.

        Returns:
            Tuple of (company, username)
        """
        # This would need to be implemented based on the actual page structure
        # For now, return placeholder values
        try:
            # Look for user info in the page - this would need actual locators
            company = "Unknown Company"
            username = "Unknown User"
            return company, username
        except Exception as e:
            logger.warning(f"Could not get logged user info: {e}")
            return "Unknown Company", "Unknown User"

    def goto_tab(self, tab_name: str) -> "BaseAviationPage":
        """
        Navigate to a specific tab in the aviation application.

        Args:
            tab_name: Name of the tab to navigate to

        Returns:
            Page object for the target tab
        """
        # This would need to be implemented with actual tab navigation logic
        logger.info(f"Navigating to tab: {tab_name}")

        # For now, just click on the tab link
        try:
            from ....core.locators import by_link_text

            tab_locator = by_link_text(tab_name, f"Tab: {tab_name}")
            tab_element = self.get_button(tab_locator)
            tab_element.click()

            # Wait for page to load
            self.wait_for_page_load()

            # Return appropriate page object based on tab name
            return self._get_page_for_tab(tab_name)

        except Exception as e:
            logger.error(f"Failed to navigate to tab {tab_name}: {e}")
            raise

    def _get_page_for_tab(self, tab_name: str) -> "BaseAviationPage":
        """
        Get the appropriate page object for a given tab.

        Args:
            tab_name: Name of the tab

        Returns:
            Page object for the tab
        """
        # This would map tab names to page classes
        # For now, return self as a placeholder
        return self

    def verify_page_loaded(self) -> bool:
        """
        Verify that the aviation page has loaded correctly.
        Checks for common aviation page elements.
        """
        try:
            # Check that we have one of the expected titles
            if not any(title in self.title for title in self.expected_titles):
                logger.warning(f"Unexpected page title: {self.title}")
                return False

            # Additional aviation-specific checks could go here
            return True

        except Exception as e:
            logger.error(f"Error verifying page load: {e}")
            return False

    def wait_for_ajax(self, timeout: float | None = None) -> None:
        """
        Wait for AJAX requests to complete.
        Common pattern in aviation application.
        """
        timeout = timeout or self.timeout

        try:
            # Wait for jQuery to be ready (if using jQuery)
            self.execute_script("""
                return (typeof jQuery !== 'undefined') ? jQuery.active === 0 : true;
            """)

            # Wait for any loading indicators to disappear
            # This would need actual locators for loading indicators

        except Exception as e:
            logger.debug(f"AJAX wait completed with warning: {e}")

    def handle_popup_if_present(self) -> bool:
        """
        Handle any popup dialogs that might appear.

        Returns:
            True if popup was handled, False if no popup
        """
        try:
            alert_text = self.handle_alert(timeout=1.0)
            if alert_text:
                logger.info(f"Handled popup alert: {alert_text}")
                return True
            return False
        except Exception:
            return False

    def get_page_errors(self) -> dict[str, list]:
        """Get all page errors collected during test execution."""
        return self.page_errors.copy()

    def get_page_notes(self) -> dict[str, list]:
        """Get all page notes collected during test execution."""
        return self.page_notes.copy()

    def clear_errors_and_notes(self) -> None:
        """Clear all collected errors and notes."""
        self.page_errors.clear()
        self.page_notes.clear()

    def show_errors(self) -> None:
        """Display all collected errors and notes."""
        if self.page_errors:
            logger.error("=== PAGE ERRORS ===")
            for page_type, errors in self.page_errors.items():
                logger.error(f"{page_type}:")
                for error in errors:
                    logger.error(f"  - {error}")

        if self.page_notes:
            logger.info("=== PAGE NOTES ===")
            for page_type, notes in self.page_notes.items():
                logger.info(f"{page_type}:")
                for note in notes:
                    logger.info(f"  - {note}")

    def timing(self, message: str = "action", reset: bool = False) -> str:
        """
        Timing utility for performance measurement.

        Args:
            message: Description of the action being timed
            reset: Whether to reset the timer

        Returns:
            Timing message string
        """
        import datetime

        if not hasattr(self, "_timing_start") or reset:
            self._timing_start = datetime.datetime.now()
            if reset:
                return f"Timer reset for: {message}"

        time_diff = datetime.datetime.now() - self._timing_start
        seconds = time_diff.total_seconds()

        msg = f"{message} took {seconds:.3f} seconds"
        logger.info(msg)
        return msg
