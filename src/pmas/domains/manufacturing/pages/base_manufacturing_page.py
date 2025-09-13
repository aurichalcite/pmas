"""
Base page class for manufacturing manufacturing domain with common functionality.
"""

import logging
from typing import Any

from ....core.page import BasePage
from ..constants import FMS_TITLES

logger = logging.getLogger(__name__)


class BaseManufacturingPage(BasePage):
    """
    Base page class for all manufacturing manufacturing domain pages.
    Provides manufacturing-specific functionality and navigation patterns.
    """

    expected_titles = FMS_TITLES

    def __init__(self, driver, base_url: str = "", timeout: float = 10.0) -> None:
        super().__init__(driver, base_url, timeout)
        self.page_errors: dict[str, list] = {}
        self.page_notes: dict[str, list] = {}

    def log_production_note(self, text: str) -> None:
        """Log production decisions made by the test, to be printed when test ends."""
        page_type = str(type(self))
        if page_type not in self.page_notes:
            self.page_notes[page_type] = []
        self.page_notes[page_type].append(text)
        logger.info(f"##### PRODUCTION NOTE: {text}")

    def add_production_error(self, text: str | None, screenshot: bool = True) -> None:
        """Print and add one production error: 1 text string + make screenshot."""
        page_type = str(type(self))
        if page_type not in self.page_errors:
            self.page_errors[page_type] = []

        if not text:
            return  # just added page type to errors (to list visited pages)

        self.page_errors[page_type].append(text)
        logger.error(f"Production error: {text}")

        if screenshot:
            try:
                screenshot_path = self.take_screenshot()
                logger.info(f"Production error screenshot saved: {screenshot_path}")
            except Exception as e:
                logger.warning(f"Failed to take production error screenshot: {e}")

    def get_logged_factory_user(self) -> tuple[str, str]:
        """
        Get the currently logged in factory user information.

        Returns:
            Tuple of (factory, username)
        """
        try:
            # Look for user info in the page - this would need actual locators
            factory = "Unknown Factory"
            username = "Unknown User"
            return factory, username
        except Exception as e:
            logger.warning(f"Could not get logged factory user info: {e}")
            return "Unknown Factory", "Unknown User"

    def goto_production_tab(self, tab_name: str) -> "BaseManufacturingPage":
        """
        Navigate to a specific tab in the manufacturing application.

        Args:
            tab_name: Name of the production tab to navigate to

        Returns:
            Page object for the target tab
        """
        logger.info(f"Navigating to production tab: {tab_name}")

        try:
            from ....core.locators import by_link_text

            tab_locator = by_link_text(tab_name, f"Production Tab: {tab_name}")
            tab_element = self.get_button(tab_locator)
            tab_element.click()

            # Wait for page to load
            self.wait_for_page_load()

            # Return appropriate page object based on tab name
            return self._get_page_for_production_tab(tab_name)

        except Exception as e:
            logger.error(f"Failed to navigate to production tab {tab_name}: {e}")
            raise

    def _get_page_for_production_tab(self, tab_name: str) -> "BaseManufacturingPage":
        """
        Get the appropriate page object for a given production tab.

        Args:
            tab_name: Name of the production tab

        Returns:
            Page object for the tab
        """
        # This would map tab names to page classes
        # For now, return self as a placeholder
        return self

    def verify_page_loaded(self) -> bool:
        """
        Verify that the manufacturing manufacturing page has loaded correctly.
        Checks for common manufacturing manufacturing page elements.
        """
        try:
            # Check that we have one of the expected titles
            if not any(title in self.title for title in self.expected_titles):
                logger.warning(f"Unexpected page title: {self.title}")
                return False

            # Additional manufacturing manufacturing-specific checks could go here
            return True

        except Exception as e:
            logger.error(f"Error verifying manufacturing page load: {e}")
            return False

    def wait_for_production_ajax(self, timeout: float | None = None) -> None:
        """
        Wait for production system AJAX requests to complete.
        Common pattern in manufacturing manufacturing application.
        """
        timeout = timeout or self.timeout

        try:
            # Wait for jQuery to be ready (if using jQuery)
            self.execute_script("""
                return (typeof jQuery !== 'undefined') ? jQuery.active === 0 : true;
            """)

            # Wait for any production loading indicators to disappear
            # This would need actual locators for loading indicators

        except Exception as e:
            logger.debug(f"Production AJAX wait completed with warning: {e}")

    def handle_production_popup_if_present(self) -> bool:
        """
        Handle any production-related popup dialogs that might appear.

        Returns:
            True if popup was handled, False if no popup
        """
        try:
            alert_text = self.handle_alert(timeout=1.0)
            if alert_text:
                logger.info(f"Handled production popup alert: {alert_text}")
                return True
            return False
        except Exception:
            return False

    def check_production_line_status(self, line_id: str) -> dict[str, Any]:
        """
        Check the status of a specific production line.

        Args:
            line_id: Production line identifier

        Returns:
            Dictionary with line status information
        """
        logger.info(f"Checking production line status: {line_id}")

        try:
            # This would need actual implementation with production line status elements
            return {
                "line_id": line_id,
                "status": "OPERATIONAL",
                "current_order": "PO-2024-001",
                "capacity_utilization": 85.5,
                "estimated_completion": "2024-01-15 16:30:00",
            }
        except Exception as e:
            logger.error(f"Failed to check production line status: {e}")
            return {"line_id": line_id, "status": "UNKNOWN", "error": str(e)}

    def check_material_inventory(self, material_type: str) -> dict[str, Any]:
        """
        Check inventory levels for a specific material type.

        Args:
            material_type: Type of material to check

        Returns:
            Dictionary with inventory information
        """
        logger.info(f"Checking material inventory: {material_type}")

        try:
            # This would need actual implementation with inventory elements
            return {
                "material_type": material_type,
                "current_stock": 1250,
                "unit": "kg"
                if material_type == "WOOD"
                else "m2"
                if material_type == "FABRIC"
                else "units",
                "reorder_level": 500,
                "status": "ADEQUATE",
            }
        except Exception as e:
            logger.error(f"Failed to check material inventory: {e}")
            return {
                "material_type": material_type,
                "status": "UNKNOWN",
                "error": str(e),
            }

    def get_production_errors(self) -> dict[str, list]:
        """Get all production errors collected during test execution."""
        return self.page_errors.copy()

    def get_production_notes(self) -> dict[str, list]:
        """Get all production notes collected during test execution."""
        return self.page_notes.copy()

    def clear_production_errors_and_notes(self) -> None:
        """Clear all collected production errors and notes."""
        self.page_errors.clear()
        self.page_notes.clear()

    def show_production_errors(self) -> None:
        """Display all collected production errors and notes."""
        if self.page_errors:
            logger.error("=== PRODUCTION ERRORS ===")
            for page_type, errors in self.page_errors.items():
                logger.error(f"{page_type}:")
                for error in errors:
                    logger.error(f"  - {error}")

        if self.page_notes:
            logger.info("=== PRODUCTION NOTES ===")
            for page_type, notes in self.page_notes.items():
                logger.info(f"{page_type}:")
                for note in notes:
                    logger.info(f"  - {note}")

    def timing_production_operation(
        self, message: str = "production operation", reset: bool = False
    ) -> str:
        """
        Timing utility for production operation performance measurement.

        Args:
            message: Description of the production operation being timed
            reset: Whether to reset the timer

        Returns:
            Timing message string
        """
        import datetime

        if not hasattr(self, "_production_timing_start") or reset:
            self._production_timing_start = datetime.datetime.now()
            if reset:
                return f"Production timer reset for: {message}"

        time_diff = datetime.datetime.now() - self._production_timing_start
        seconds = time_diff.total_seconds()

        msg = f"Production {message} took {seconds:.3f} seconds"
        logger.info(msg)
        return msg

    def validate_production_order_data(self, order_data: dict[str, Any]) -> bool:
        """
        Validate production order data before submission.

        Args:
            order_data: Production order data to validate

        Returns:
            True if valid, False otherwise
        """
        required_fields = [
            "production_line_id",
            "source_factory",
            "destination_warehouse",
            "order_quantity",
        ]

        for field in required_fields:
            if field not in order_data or not order_data[field]:
                logger.error(f"Missing required field in production order: {field}")
                return False

        # Additional validation logic would go here
        return True
