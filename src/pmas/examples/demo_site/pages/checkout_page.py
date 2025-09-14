"""
SauceDemo checkout page object demonstrating PMAS framework usage.
"""

import logging
from typing import Any

from ....core.locators import by_class_name, by_css_selector, by_id
from ....core.page import BasePage

logger = logging.getLogger(__name__)


class SauceDemoCheckoutPage(BasePage):
    """
    SauceDemo checkout page demonstrating modern page object patterns.
    """

    url_path = "/checkout-step-one.html"

    # Step One - Information Form
    CHECKOUT_INFO_CONTAINER = by_id(
        "checkout_info_container", "Checkout info container"
    )
    FIRST_NAME_FIELD = by_id("first-name", "First name field")
    LAST_NAME_FIELD = by_id("last-name", "Last name field")
    POSTAL_CODE_FIELD = by_id("postal-code", "Postal code field")
    CONTINUE_BUTTON = by_id("continue", "Continue button")
    CANCEL_BUTTON = by_id("cancel", "Cancel button")

    # Step Two - Overview
    CHECKOUT_SUMMARY_CONTAINER = by_id(
        "checkout_summary_container", "Checkout summary container"
    )
    SUMMARY_INFO = by_class_name("summary_info", "Summary info")
    PAYMENT_INFO = by_css_selector('[data-test="payment-info-value"]', "Payment info")
    SHIPPING_INFO = by_css_selector(
        '[data-test="shipping-info-value"]', "Shipping info"
    )
    SUBTOTAL = by_class_name("summary_subtotal_label", "Subtotal")
    TAX = by_class_name("summary_tax_label", "Tax")
    TOTAL = by_class_name("summary_total_label", "Total")
    FINISH_BUTTON = by_id("finish", "Finish button")

    # Complete page
    CHECKOUT_COMPLETE_CONTAINER = by_id(
        "checkout_complete_container", "Checkout complete container"
    )
    COMPLETE_HEADER = by_class_name("complete-header", "Complete header")
    COMPLETE_TEXT = by_class_name("complete-text", "Complete text")
    BACK_HOME_BUTTON = by_id("back-to-products", "Back to products button")

    # Error handling
    ERROR_MESSAGE = by_css_selector('[data-test="error"]', "Error message")

    def __init__(
        self, driver, base_url: str = "https://www.saucedemo.com", timeout: float = 10.0
    ) -> None:
        super().__init__(driver, base_url, timeout)

    def verify_page_loaded(self) -> bool:
        """Verify that the checkout page has loaded correctly."""
        try:
            # Check for checkout info container (step one)
            if self.current_url.endswith("/checkout-step-one.html"):
                container = self.find_element(self.CHECKOUT_INFO_CONTAINER)
                return container.is_displayed()

            # Check for summary container (step two)
            elif self.current_url.endswith("/checkout-step-two.html"):
                container = self.find_element(self.CHECKOUT_SUMMARY_CONTAINER)
                return container.is_displayed()

            # Check for complete container (final step)
            elif self.current_url.endswith("/checkout-complete.html"):
                container = self.find_element(self.CHECKOUT_COMPLETE_CONTAINER)
                return container.is_displayed()

            return False

        except Exception as e:
            logger.error(f"Checkout page verification failed: {e}")
            return False

    def fill_checkout_information(
        self, first_name: str, last_name: str, postal_code: str
    ) -> None:
        """
        Fill out the checkout information form.

        Args:
            first_name: Customer's first name
            last_name: Customer's last name
            postal_code: Customer's postal code
        """
        logger.info(
            f"Filling checkout information: {first_name} {last_name}, {postal_code}"
        )

        try:
            # Fill form fields
            first_name_field = self.get_text_input(self.FIRST_NAME_FIELD)
            last_name_field = self.get_text_input(self.LAST_NAME_FIELD)
            postal_code_field = self.get_text_input(self.POSTAL_CODE_FIELD)

            first_name_field.clear()
            first_name_field.type_text(first_name)

            last_name_field.clear()
            last_name_field.type_text(last_name)

            postal_code_field.clear()
            postal_code_field.type_text(postal_code)

            logger.info("Successfully filled checkout information")

        except Exception as e:
            logger.error(f"Failed to fill checkout information: {e}")
            raise

    def continue_to_overview(self) -> None:
        """Continue from information step to overview step."""
        logger.info("Continuing to checkout overview")

        try:
            continue_button = self.get_button(self.CONTINUE_BUTTON)
            continue_button.click()

            self.wait_for_page_load()

            # Verify we're on the overview page
            if not self.current_url.endswith("/checkout-step-two.html"):
                raise Exception("Failed to navigate to checkout overview")

            logger.info("Successfully navigated to checkout overview")

        except Exception as e:
            logger.error(f"Failed to continue to overview: {e}")
            raise

    def get_order_summary(self) -> dict[str, Any]:
        """
        Get the order summary information from the overview page.

        Returns:
            Dictionary containing order summary details
        """
        logger.info("Getting order summary")

        try:
            # Extract summary information
            payment_info = self.find_element(self.PAYMENT_INFO).text
            shipping_info = self.find_element(self.SHIPPING_INFO).text
            subtotal_text = self.find_element(self.SUBTOTAL).text
            tax_text = self.find_element(self.TAX).text
            total_text = self.find_element(self.TOTAL).text

            # Parse monetary values
            subtotal = float(subtotal_text.split("$")[1])
            tax = float(tax_text.split("$")[1])
            total = float(total_text.split("$")[1])

            summary = {
                "payment_info": payment_info,
                "shipping_info": shipping_info,
                "subtotal": subtotal,
                "tax": tax,
                "total": total,
            }

            logger.info(f"Order summary: {summary}")
            return summary

        except Exception as e:
            logger.error(f"Failed to get order summary: {e}")
            return {}

    def finish_checkout(self) -> None:
        """Complete the checkout process."""
        logger.info("Finishing checkout")

        try:
            finish_button = self.get_button(self.FINISH_BUTTON)
            finish_button.click()

            self.wait_for_page_load()

            # Verify we're on the complete page
            if not self.current_url.endswith("/checkout-complete.html"):
                raise Exception("Failed to complete checkout")

            logger.info("Successfully completed checkout")

        except Exception as e:
            logger.error(f"Failed to finish checkout: {e}")
            raise

    def get_completion_message(self) -> dict[str, str]:
        """
        Get the checkout completion message.

        Returns:
            Dictionary with header and text of completion message
        """
        try:
            header = self.find_element(self.COMPLETE_HEADER).text
            text = self.find_element(self.COMPLETE_TEXT).text

            return {"header": header, "text": text}

        except Exception as e:
            logger.error(f"Failed to get completion message: {e}")
            return {"header": "", "text": ""}

    def back_to_products(self) -> "SauceDemoInventoryPage":
        """
        Return to the products page after checkout completion.

        Returns:
            Inventory page object
        """
        logger.info("Returning to products page")

        try:
            back_button = self.get_button(self.BACK_HOME_BUTTON)
            back_button.click()

            self.wait_for_page_load()

            # Import here to avoid circular imports
            from .inventory_page import SauceDemoInventoryPage

            return SauceDemoInventoryPage(self.driver, self.base_url, self.timeout)

        except Exception as e:
            logger.error(f"Failed to return to products: {e}")
            raise

    def cancel_checkout(self) -> "SauceDemoCartPage":
        """
        Cancel the checkout process and return to cart.

        Returns:
            Cart page object
        """
        logger.info("Cancelling checkout")

        try:
            cancel_button = self.get_button(self.CANCEL_BUTTON)
            cancel_button.click()

            self.wait_for_page_load()

            # Import here to avoid circular imports
            from .cart_page import SauceDemoCartPage

            return SauceDemoCartPage(self.driver, self.base_url, self.timeout)

        except Exception as e:
            logger.error(f"Failed to cancel checkout: {e}")
            raise

    def complete_full_checkout(
        self, first_name: str, last_name: str, postal_code: str
    ) -> dict[str, Any]:
        """
        Complete the entire checkout process from information to completion.

        Args:
            first_name: Customer's first name
            last_name: Customer's last name
            postal_code: Customer's postal code

        Returns:
            Dictionary with checkout results
        """
        logger.info("Starting complete checkout process")

        try:
            # Step 1: Fill information
            self.fill_checkout_information(first_name, last_name, postal_code)

            # Step 2: Continue to overview
            self.continue_to_overview()

            # Step 3: Get order summary
            order_summary = self.get_order_summary()

            # Step 4: Finish checkout
            self.finish_checkout()

            # Step 5: Get completion message
            completion_message = self.get_completion_message()

            result = {
                "success": True,
                "order_summary": order_summary,
                "completion_message": completion_message,
            }

            logger.info("Successfully completed full checkout process")
            return result

        except Exception as e:
            logger.error(f"Failed to complete full checkout: {e}")
            return {"success": False, "error": str(e)}

    def is_error_displayed(self) -> bool:
        """Check if an error message is displayed."""
        try:
            error_element = self.find_element(self.ERROR_MESSAGE, timeout=2.0)
            return error_element.is_displayed()
        except Exception:
            return False

    def get_error_message(self) -> str:
        """Get the error message text."""
        try:
            error_element = self.find_element(self.ERROR_MESSAGE)
            return error_element.text.strip()
        except Exception:
            return ""
