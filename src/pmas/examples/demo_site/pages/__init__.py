"""
Demo site page objects for saucedemo.com examples.
"""

from .cart_page import SauceDemoCartPage
from .checkout_page import SauceDemoCheckoutPage
from .inventory_page import SauceDemoInventoryPage
from .login_page import SauceDemoLoginPage

__all__ = [
    "SauceDemoLoginPage",
    "SauceDemoInventoryPage",
    "SauceDemoCartPage",
    "SauceDemoCheckoutPage",
]
