"""
SauceDemo cart page object demonstrating PMAS framework usage.
"""

import logging
from typing import Any

from ....core.locators import by_class_name, by_css_selector, by_id
from ....core.page import BasePage

logger = logging.getLogger(__name__)


class SauceDemoCartPage(BasePage):
    """
    SauceDemo cart page demonstrating modern page object patterns.
    """

    url_path = "/cart.html"

    # Locators
    CART_CONTENTS = by_id("cart_contents_container", "Cart contents container")
    CART_LIST = by_class_name("cart_list", "Cart list")
    CART_ITEMS = by_class_name("cart_item", "Cart items")

    # Buttons
    CONTINUE_SHOPPING_BUTTON = by_id("continue-shopping", "Continue shopping button")
    CHECKOUT_BUTTON = by_id("checkout", "Checkout button")

    # Item elements
    CART_ITEM_NAMES = by_class_name("inventory_item_name", "Cart item names")
    CART_ITEM_PRICES = by_class_name("inventory_item_price", "Cart item prices")
    CART_ITEM_QUANTITIES = by_class_name("cart_quantity", "Cart item quantities")

    # Remove buttons (template)
    REMOVE_BUTTON_TEMPLATE = by_css_selector(
        '[data-test="remove-{}"]', "Remove button: {}"
    )

    def __init__(
        self, driver, base_url: str = "https://www.saucedemo.com", timeout: float = 10.0
    ) -> None:
        super().__init__(driver, base_url, timeout)

    def verify_page_loaded(self) -> bool:
        """Verify that the cart page has loaded correctly."""
        try:
            # Check for cart container and checkout button
            cart_container = self.find_element(self.CART_CONTENTS)
            checkout_button = self.find_element(self.CHECKOUT_BUTTON)

            return cart_container.is_displayed() and checkout_button.is_displayed()
        except Exception as e:
            logger.error(f"Cart page verification failed: {e}")
            return False

    def get_cart_items(self) -> list[dict[str, Any]]:
        """
        Get all items currently in the cart.

        Returns:
            List of dictionaries containing cart item details
        """
        items = []
        try:
            item_elements = self.find_elements(self.CART_ITEMS)

            for item_element in item_elements:
                # Extract item details from each cart item
                name_element = item_element.find_element(
                    "class name", "inventory_item_name"
                )
                price_element = item_element.find_element(
                    "class name", "inventory_item_price"
                )
                quantity_element = item_element.find_element(
                    "class name", "cart_quantity"
                )
                desc_element = item_element.find_element(
                    "class name", "inventory_item_desc"
                )

                items.append(
                    {
                        "name": name_element.text,
                        "description": desc_element.text,
                        "price": price_element.text,
                        "quantity": int(quantity_element.text),
                    }
                )

        except Exception as e:
            logger.error(f"Failed to get cart items: {e}")

        return items

    def get_cart_item_count(self) -> int:
        """
        Get the number of items in the cart.

        Returns:
            Number of items in cart
        """
        try:
            items = self.get_cart_items()
            return sum(item["quantity"] for item in items)
        except Exception as e:
            logger.error(f"Failed to get cart item count: {e}")
            return 0

    def remove_item_from_cart(self, item_slug: str) -> None:
        """
        Remove an item from the cart by its slug.

        Args:
            item_slug: The item slug (e.g., 'sauce-labs-backpack')
        """
        logger.info(f"Removing item from cart: {item_slug}")

        try:
            # Create locator for the specific remove button
            remove_button_locator = by_css_selector(
                f'[data-test="remove-{item_slug}"]',
                f"Remove from cart button: {item_slug}",
            )

            remove_button = self.get_button(remove_button_locator)
            remove_button.click()

            logger.info(f"Successfully removed {item_slug} from cart")

        except Exception as e:
            logger.error(f"Failed to remove item {item_slug} from cart: {e}")
            raise

    def continue_shopping(self) -> "SauceDemoInventoryPage":
        """
        Continue shopping by returning to the inventory page.

        Returns:
            Inventory page object
        """
        logger.info("Continuing shopping")

        try:
            continue_button = self.get_button(self.CONTINUE_SHOPPING_BUTTON)
            continue_button.click()

            self.wait_for_page_load()

            # Import here to avoid circular imports
            from .inventory_page import SauceDemoInventoryPage

            return SauceDemoInventoryPage(self.driver, self.base_url, self.timeout)

        except Exception as e:
            logger.error(f"Failed to continue shopping: {e}")
            raise

    def proceed_to_checkout(self) -> "SauceDemoCheckoutPage":
        """
        Proceed to checkout.

        Returns:
            Checkout page object
        """
        logger.info("Proceeding to checkout")

        try:
            checkout_button = self.get_button(self.CHECKOUT_BUTTON)
            checkout_button.click()

            self.wait_for_page_load()

            # Import here to avoid circular imports
            from .checkout_page import SauceDemoCheckoutPage

            return SauceDemoCheckoutPage(self.driver, self.base_url, self.timeout)

        except Exception as e:
            logger.error(f"Failed to proceed to checkout: {e}")
            raise

    def is_cart_empty(self) -> bool:
        """
        Check if the cart is empty.

        Returns:
            True if cart is empty, False otherwise
        """
        try:
            items = self.get_cart_items()
            return len(items) == 0
        except Exception:
            return True

    def get_cart_item_names(self) -> list[str]:
        """
        Get list of all item names in the cart.

        Returns:
            List of item names
        """
        try:
            name_elements = self.find_elements(self.CART_ITEM_NAMES)
            return [element.text for element in name_elements]
        except Exception as e:
            logger.error(f"Failed to get cart item names: {e}")
            return []

    def get_cart_total_price(self) -> float:
        """
        Calculate the total price of items in the cart.
        Note: This is a simple calculation based on displayed prices.

        Returns:
            Total price as float
        """
        try:
            items = self.get_cart_items()
            total = 0.0

            for item in items:
                # Extract price from string like "$29.99"
                price_str = item["price"].replace("$", "")
                price = float(price_str)
                total += price * item["quantity"]

            return total

        except Exception as e:
            logger.error(f"Failed to calculate cart total: {e}")
            return 0.0

    def clear_cart(self) -> None:
        """
        Remove all items from the cart.
        """
        logger.info("Clearing cart")

        try:
            items = self.get_cart_items()

            for item in items:
                # Convert item name to slug for removal
                item_slug = self._get_item_slug(item["name"])
                self.remove_item_from_cart(item_slug)

            logger.info("Successfully cleared cart")

        except Exception as e:
            logger.error(f"Failed to clear cart: {e}")
            raise

    def _get_item_slug(self, item_name: str) -> str:
        """
        Convert item name to slug format used in data-test attributes.

        Args:
            item_name: The display name of the item

        Returns:
            The slug version of the name
        """
        # Map of known item names to their slugs
        name_to_slug = {
            "Sauce Labs Backpack": "sauce-labs-backpack",
            "Sauce Labs Bike Light": "sauce-labs-bike-light",
            "Sauce Labs Bolt T-Shirt": "sauce-labs-bolt-t-shirt",
            "Sauce Labs Fleece Jacket": "sauce-labs-fleece-jacket",
            "Sauce Labs Onesie": "sauce-labs-onesie",
            "Test.allTheThings() T-Shirt (Red)": "test.allthethings()-t-shirt-(red)",
        }

        return name_to_slug.get(item_name, item_name.lower().replace(" ", "-"))

    def verify_item_in_cart(self, item_name: str) -> bool:
        """
        Verify that a specific item is in the cart.

        Args:
            item_name: Name of the item to verify

        Returns:
            True if item is in cart, False otherwise
        """
        try:
            cart_items = self.get_cart_items()
            return any(item["name"] == item_name for item in cart_items)
        except Exception as e:
            logger.error(f"Failed to verify item in cart: {e}")
            return False
