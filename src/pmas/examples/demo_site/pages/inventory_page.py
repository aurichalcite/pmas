"""
SauceDemo inventory page object demonstrating PMAS framework usage.
"""

import logging
from typing import TYPE_CHECKING, Any

from ....core.locators import by_class_name, by_css_selector, by_id
from ....core.page import BasePage

if TYPE_CHECKING:
    from .cart_page import SauceDemoCartPage
    from .login_page import SauceDemoLoginPage


logger = logging.getLogger(__name__)


class SauceDemoInventoryPage(BasePage):
    """
    SauceDemo inventory page demonstrating modern page object patterns.
    """

    url_path = "/inventory.html"

    # Locators
    INVENTORY_CONTAINER = by_id("inventory_container", "Inventory container")
    INVENTORY_LIST = by_class_name("inventory_list", "Inventory list")
    INVENTORY_ITEMS = by_class_name("inventory_item", "Inventory items")

    # Header elements
    SHOPPING_CART_LINK = by_class_name("shopping_cart_link", "Shopping cart link")
    SHOPPING_CART_BADGE = by_class_name("shopping_cart_badge", "Shopping cart badge")
    BURGER_MENU = by_id("react-burger-menu-btn", "Burger menu button")

    # Sort dropdown
    SORT_DROPDOWN = by_css_selector(
        '[data-test="product_sort_container"]', "Sort dropdown"
    )

    # Item elements (templates)
    ITEM_NAME_TEMPLATE = by_css_selector(
        '[data-test="inventory-item-name"]', "Item name: {}"
    )
    ITEM_PRICE_TEMPLATE = by_class_name("inventory_item_price", "Item price: {}")
    ADD_TO_CART_TEMPLATE = by_css_selector(
        '[data-test="add-to-cart-{}"]', "Add to cart button: {}"
    )
    REMOVE_FROM_CART_TEMPLATE = by_css_selector(
        '[data-test="remove-{}"]', "Remove from cart button: {}"
    )

    def __init__(
        self, driver, base_url: str = "https://www.saucedemo.com", timeout: float = 10.0
    ) -> None:
        super().__init__(driver, base_url, timeout)

    def verify_page_loaded(self) -> bool:
        """Verify that the inventory page has loaded correctly."""
        try:
            # Check for inventory container
            inventory_container = self.find_element(self.INVENTORY_CONTAINER)
            shopping_cart = self.find_element(self.SHOPPING_CART_LINK)

            return inventory_container.is_displayed() and shopping_cart.is_displayed()
        except Exception as e:
            logger.error(f"Inventory page verification failed: {e}")
            return False

    def get_inventory_items(self) -> list[dict[str, Any]]:
        """
        Get all inventory items with their details.

        Returns:
            List of dictionaries containing item details
        """
        items = []
        try:
            item_elements = self.find_elements(self.INVENTORY_ITEMS)

            for item_element in item_elements:
                # Extract item details from each inventory item
                name_element = item_element.find_element(
                    "css selector", '[data-test="inventory-item-name"]'
                )
                price_element = item_element.find_element(
                    "class name", "inventory_item_price"
                )
                desc_element = item_element.find_element(
                    "class name", "inventory_item_desc"
                )

                # Get the item slug from the name for button identification
                item_name = name_element.text
                item_slug = self._get_item_slug(item_name)

                items.append(
                    {
                        "name": item_name,
                        "description": desc_element.text,
                        "price": price_element.text,
                        "slug": item_slug,
                    }
                )

        except Exception as e:
            logger.error(f"Failed to get inventory items: {e}")

        return items

    def add_item_to_cart(self, item_slug: str) -> None:
        """
        Add an item to the cart by its slug.

        Args:
            item_slug: The item slug (e.g., 'sauce-labs-backpack')
        """
        logger.info(f"Adding item to cart: {item_slug}")

        try:
            # Create locator for the specific add to cart button
            add_button_locator = by_css_selector(
                f'[data-test="add-to-cart-{item_slug}"]',
                f"Add to cart button: {item_slug}",
            )

            add_button = self.get_button(add_button_locator)
            add_button.click()

            logger.info(f"Successfully added {item_slug} to cart")

        except Exception as e:
            logger.error(f"Failed to add item {item_slug} to cart: {e}")
            raise

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

    def is_item_in_cart(self, item_slug: str) -> bool:
        """
        Check if an item is currently in the cart.

        Args:
            item_slug: The item slug to check

        Returns:
            True if item is in cart, False otherwise
        """
        try:
            # If remove button exists, item is in cart
            remove_button_locator = by_css_selector(
                f'[data-test="remove-{item_slug}"]',
                f"Remove from cart button: {item_slug}",
            )

            remove_button = self.find_element(remove_button_locator, timeout=2.0)
            return remove_button.is_displayed()

        except Exception:
            return False

    def get_cart_item_count(self) -> int:
        """
        Get the number of items in the shopping cart.

        Returns:
            Number of items in cart
        """
        try:
            badge_element = self.find_element(self.SHOPPING_CART_BADGE, timeout=2.0)
            return int(badge_element.text)
        except Exception:
            return 0

    def go_to_cart(self) -> "SauceDemoCartPage":
        """
        Navigate to the shopping cart page.

        Returns:
            Cart page object
        """
        logger.info("Navigating to shopping cart")

        try:
            cart_link = self.get_button(self.SHOPPING_CART_LINK)
            cart_link.click()

            self.wait_for_page_load()

            # Import here to avoid circular imports
            from .cart_page import SauceDemoCartPage

            return SauceDemoCartPage(self.driver, self.base_url, self.timeout)

        except Exception as e:
            logger.error(f"Failed to navigate to cart: {e}")
            raise

    def sort_items(self, sort_option: str) -> None:
        """
        Sort inventory items by the given option.

        Args:
            sort_option: Sort option ('az', 'za', 'lohi', 'hilo')
        """
        logger.info(f"Sorting items by: {sort_option}")

        try:
            sort_dropdown = self.get_dropdown(self.SORT_DROPDOWN)
            sort_dropdown.select_by_value(sort_option)

            # Wait for items to be re-sorted
            self.wait_for_page_load()

        except Exception as e:
            logger.error(f"Failed to sort items: {e}")
            raise

    def get_item_names(self) -> list[str]:
        """
        Get list of all item names currently displayed.

        Returns:
            List of item names
        """
        try:
            name_elements = self.find_elements(
                by_css_selector('[data-test="inventory-item-name"]', "Item names")
            )
            return [element.text for element in name_elements]
        except Exception as e:
            logger.error(f"Failed to get item names: {e}")
            return []

    def get_item_prices(self) -> list[str]:
        """
        Get list of all item prices currently displayed.

        Returns:
            List of item prices
        """
        try:
            price_elements = self.find_elements(
                by_class_name("inventory_item_price", "Item prices")
            )
            return [element.text for element in price_elements]
        except Exception as e:
            logger.error(f"Failed to get item prices: {e}")
            return []

    def add_multiple_items_to_cart(self, item_slugs: list[str]) -> None:
        """
        Add multiple items to cart.

        Args:
            item_slugs: List of item slugs to add
        """
        logger.info(f"Adding multiple items to cart: {item_slugs}")

        for item_slug in item_slugs:
            self.add_item_to_cart(item_slug)

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

    def logout(self) -> "SauceDemoLoginPage":
        """
        Logout from the application.

        Returns:
            Login page object
        """
        logger.info("Logging out")

        try:
            # Open burger menu
            burger_menu = self.get_button(self.BURGER_MENU)
            burger_menu.click()

            # Wait for menu to open and click logout
            logout_link = self.wait_for_element(
                by_id("logout_sidebar_link", "Logout link")
            )
            logout_link.click()

            self.wait_for_page_load()

            # Import here to avoid circular imports
            from .login_page import SauceDemoLoginPage

            return SauceDemoLoginPage(self.driver, self.base_url, self.timeout)

        except Exception as e:
            logger.error(f"Failed to logout: {e}")
            raise
