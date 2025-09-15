"""
Example tests for SauceDemo shopping workflow demonstrating PMAS framework usage.
"""

import pytest

from ..pages.login_page import SauceDemoLoginPage


class TestSauceDemoShoppingWorkflow:
    """
    Test class demonstrating end-to-end shopping workflow testing with PMAS
    framework.
    """

    def test_complete_shopping_workflow(self, driver, config):
        """Test complete shopping workflow from login to checkout completion."""
        # Arrange
        login_page = SauceDemoLoginPage(driver, config.environment.base_url)
        login_page.navigate_to_login()

        # Act & Assert - Step 1: Login
        inventory_page = login_page.login_standard_user()
        assert inventory_page.verify_page_loaded()

        # Act & Assert - Step 2: Add items to cart
        items_to_add = ["sauce-labs-backpack", "sauce-labs-bike-light"]
        inventory_page.add_multiple_items_to_cart(items_to_add)

        # Verify items were added
        assert inventory_page.get_cart_item_count() == 2

        # Act & Assert - Step 3: Go to cart
        cart_page = inventory_page.go_to_cart()
        assert cart_page.verify_page_loaded()

        # Verify cart contents
        cart_items = cart_page.get_cart_items()
        assert len(cart_items) == 2

        # Act & Assert - Step 4: Proceed to checkout
        checkout_page = cart_page.proceed_to_checkout()
        assert checkout_page.verify_page_loaded()

        # Act & Assert - Step 5: Complete checkout
        checkout_result = checkout_page.complete_full_checkout(
            first_name="John", last_name="Doe", postal_code="12345"
        )

        assert checkout_result["success"]
        assert (
            checkout_result["completion_message"]["header"]
            == "Thank you for your order!"
        )

    def test_add_and_remove_items_from_inventory(self, driver, config):
        """Test adding and removing items from the inventory page."""
        # Arrange
        login_page = SauceDemoLoginPage(driver, config.environment.base_url)
        login_page.navigate_to_login()
        inventory_page = login_page.login_standard_user()

        # Act & Assert - Add item
        inventory_page.add_item_to_cart("sauce-labs-backpack")
        assert inventory_page.get_cart_item_count() == 1
        assert inventory_page.is_item_in_cart("sauce-labs-backpack")

        # Act & Assert - Remove item
        inventory_page.remove_item_from_cart("sauce-labs-backpack")
        assert inventory_page.get_cart_item_count() == 0
        assert not inventory_page.is_item_in_cart("sauce-labs-backpack")

    def test_add_and_remove_items_from_cart(self, driver, config):
        """Test adding items and removing them from the cart page."""
        # Arrange
        login_page = SauceDemoLoginPage(driver, config.environment.base_url)
        login_page.navigate_to_login()
        inventory_page = login_page.login_standard_user()

        # Add items and go to cart
        items_to_add = [
            "sauce-labs-backpack",
            "sauce-labs-bike-light",
            "sauce-labs-bolt-t-shirt",
        ]
        inventory_page.add_multiple_items_to_cart(items_to_add)
        cart_page = inventory_page.go_to_cart()

        # Act & Assert - Verify initial cart state
        assert cart_page.get_cart_item_count() == 3

        # Act & Assert - Remove one item
        cart_page.remove_item_from_cart("sauce-labs-bike-light")
        assert cart_page.get_cart_item_count() == 2

        # Verify specific items remain
        cart_item_names = cart_page.get_cart_item_names()
        assert "Sauce Labs Backpack" in cart_item_names
        assert "Sauce Labs Bolt T-Shirt" in cart_item_names
        assert "Sauce Labs Bike Light" not in cart_item_names

    def test_inventory_sorting(self, driver, config):
        """Test inventory sorting functionality."""
        # Arrange
        login_page = SauceDemoLoginPage(driver, config.environment.base_url)
        login_page.navigate_to_login()
        inventory_page = login_page.login_standard_user()

        # Act & Assert - Test A-Z sorting
        inventory_page.sort_items("az")
        item_names = inventory_page.get_item_names()
        assert item_names == sorted(item_names)

        # Act & Assert - Test Z-A sorting
        inventory_page.sort_items("za")
        item_names = inventory_page.get_item_names()
        assert item_names == sorted(item_names, reverse=True)

        # Act & Assert - Test price low to high
        inventory_page.sort_items("lohi")
        item_prices = inventory_page.get_item_prices()
        # Convert prices to floats for comparison
        price_values = [float(price.replace("$", "")) for price in item_prices]
        assert price_values == sorted(price_values)

        # Act & Assert - Test price high to low
        inventory_page.sort_items("hilo")
        item_prices = inventory_page.get_item_prices()
        price_values = [float(price.replace("$", "")) for price in item_prices]
        assert price_values == sorted(price_values, reverse=True)

    def test_continue_shopping_from_cart(self, driver, config):
        """Test continuing shopping from cart page."""
        # Arrange
        login_page = SauceDemoLoginPage(driver, config.environment.base_url)
        login_page.navigate_to_login()
        inventory_page = login_page.login_standard_user()

        # Add item and go to cart
        inventory_page.add_item_to_cart("sauce-labs-backpack")
        cart_page = inventory_page.go_to_cart()

        # Act
        returned_inventory_page = cart_page.continue_shopping()

        # Assert
        assert returned_inventory_page.verify_page_loaded()
        assert "inventory.html" in returned_inventory_page.current_url
        # Cart should still have the item
        assert returned_inventory_page.get_cart_item_count() == 1

    def test_checkout_with_missing_information(self, driver, config):
        """Test checkout validation with missing required information."""
        # Arrange
        login_page = SauceDemoLoginPage(driver, config.environment.base_url)
        login_page.navigate_to_login()
        inventory_page = login_page.login_standard_user()

        # Add item and proceed to checkout
        inventory_page.add_item_to_cart("sauce-labs-backpack")
        cart_page = inventory_page.go_to_cart()
        checkout_page = cart_page.proceed_to_checkout()

        # Act & Assert - Try to continue without filling information
        checkout_page.continue_to_overview()

        # Should show error message
        assert checkout_page.is_error_displayed()
        error_message = checkout_page.get_error_message()
        assert "first name is required" in error_message.lower()

    def test_cancel_checkout_returns_to_cart(self, driver, config):
        """Test that canceling checkout returns to cart."""
        # Arrange
        login_page = SauceDemoLoginPage(driver, config.environment.base_url)
        login_page.navigate_to_login()
        inventory_page = login_page.login_standard_user()

        # Add item and proceed to checkout
        inventory_page.add_item_to_cart("sauce-labs-backpack")
        cart_page = inventory_page.go_to_cart()
        checkout_page = cart_page.proceed_to_checkout()

        # Act
        returned_cart_page = checkout_page.cancel_checkout()

        # Assert
        assert returned_cart_page.verify_page_loaded()
        assert "cart.html" in returned_cart_page.current_url
        # Item should still be in cart
        assert returned_cart_page.get_cart_item_count() == 1

    def test_empty_cart_checkout_prevention(self, driver, config):
        """Test that empty cart prevents checkout."""
        # Arrange
        login_page = SauceDemoLoginPage(driver, config.environment.base_url)
        login_page.navigate_to_login()
        inventory_page = login_page.login_standard_user()

        # Go to cart without adding items
        cart_page = inventory_page.go_to_cart()

        # Assert
        assert cart_page.is_cart_empty()

        # The checkout button should still be present but clicking it
        # would lead to an empty checkout (this is SauceDemo behavior)
        # In a real application, this might be disabled

    @pytest.mark.parametrize(
        "items_to_add,expected_count",
        [
            (["sauce-labs-backpack"], 1),
            (["sauce-labs-backpack", "sauce-labs-bike-light"], 2),
            (
                [
                    "sauce-labs-backpack",
                    "sauce-labs-bike-light",
                    "sauce-labs-bolt-t-shirt",
                ],
                3,
            ),
            ([], 0),
        ],
    )
    def test_cart_item_count_accuracy(
        self, driver, config, items_to_add: list[str], expected_count: int
    ):
        """Parameterized test for cart item count accuracy."""
        # Arrange
        login_page = SauceDemoLoginPage(driver, config.environment.base_url)
        login_page.navigate_to_login()
        inventory_page = login_page.login_standard_user()

        # Act
        if items_to_add:
            inventory_page.add_multiple_items_to_cart(items_to_add)

        # Assert
        assert inventory_page.get_cart_item_count() == expected_count

        # Also verify from cart page
        cart_page = inventory_page.go_to_cart()
        assert cart_page.get_cart_item_count() == expected_count

    def test_logout_functionality(self, driver, config):
        """Test logout functionality."""
        # Arrange
        login_page = SauceDemoLoginPage(driver, config.environment.base_url)
        login_page.navigate_to_login()
        inventory_page = login_page.login_standard_user()

        # Act
        returned_login_page = inventory_page.logout()

        # Assert
        assert returned_login_page.verify_page_loaded()
        assert returned_login_page.current_url == config.environment.base_url + "/"

    def test_order_summary_calculation(self, driver, config):
        """Test that order summary calculations are correct."""
        # Arrange
        login_page = SauceDemoLoginPage(driver, config.environment.base_url)
        login_page.navigate_to_login()
        inventory_page = login_page.login_standard_user()

        # Add specific items with known prices
        inventory_page.add_item_to_cart("sauce-labs-backpack")  # $29.99
        inventory_page.add_item_to_cart("sauce-labs-bike-light")  # $9.99

        # Proceed to checkout overview
        cart_page = inventory_page.go_to_cart()
        checkout_page = cart_page.proceed_to_checkout()
        checkout_page.fill_checkout_information("John", "Doe", "12345")
        checkout_page.continue_to_overview()

        # Act
        order_summary = checkout_page.get_order_summary()

        # Assert
        expected_subtotal = 29.99 + 9.99  # $39.98
        assert order_summary["subtotal"] == expected_subtotal

        # Tax should be calculated (SauceDemo uses 8% tax)
        expected_tax = round(expected_subtotal * 0.08, 2)
        assert order_summary["tax"] == expected_tax

        # Total should be subtotal + tax
        expected_total = expected_subtotal + expected_tax
        assert order_summary["total"] == expected_total
