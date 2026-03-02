"""
Step Definitions – Checkout Cart Management
Story: PAYSTRM-201
Feature: features/checkout/checkout_cart.feature
Framework: pytest-bdd  (Behave-compatible context reused via conftest fixture)
"""
import pytest
from pytest_bdd import given, when, then, parsers, scenarios

from features.pages.loginpage  import LoginPage
from features.pages.checkoutpage import InventoryPage, CartPage
from POM_BDD.utilis import base_url, uname, passwd

# Bind all scenarios in the matching feature file
scenarios("../../../features/checkout/checkout_cart.feature")


# ── Background ────────────────────────────────────────────────────
@given("I am logged in as a standard user")
def logged_in_standard_user(driver):
    """Navigate to SauceDemo and log in with the standard_user credentials."""
    login = LoginPage(driver)
    login.loadpage(base_url)
    login.input_username(uname)
    login.input_password(passwd)
    login.click_login_button()


# ── Add to cart ───────────────────────────────────────────────────
@when(parsers.parse('I add "{product}" to the cart'))
def add_product_to_cart(driver, product):
    inv = InventoryPage(driver)
    inv.add_item_to_cart(product)


# ── Cart badge ────────────────────────────────────────────────────
@then(parsers.parse('the cart badge should show "{count}"'))
def verify_cart_badge(driver, count):
    inv = InventoryPage(driver)
    actual = inv.get_cart_badge_count()
    assert actual == count, (
        f"Expected cart badge '{count}' but got '{actual}'"
    )


# ── Navigate to cart ──────────────────────────────────────────────
@when("I navigate to the cart")
def navigate_to_cart(driver):
    cart = CartPage(driver)
    cart.navigate_to_cart()


# ── Assert item present in cart ───────────────────────────────────
@then(parsers.parse('I should see "{product}" in the cart'))
def item_visible_in_cart(driver, product):
    cart = CartPage(driver)
    items = cart.get_cart_item_names()
    assert product in items, (
        f"Expected '{product}' in cart but found: {items}"
    )


# ── Assert item NOT in cart ───────────────────────────────────────
@then(parsers.parse('I should not see "{product}" in the cart'))
def item_not_visible_in_cart(driver, product):
    cart = CartPage(driver)
    items = cart.get_cart_item_names()
    assert product not in items, (
        f"Expected '{product}' to be absent from cart but it was present."
    )


# ── Remove item ───────────────────────────────────────────────────
@when(parsers.parse('I remove "{product}" from the cart'))
def remove_product_from_cart(driver, product):
    cart = CartPage(driver)
    cart.remove_item(product)


# ── Click Checkout / generic button ──────────────────────────────
@when(parsers.parse('I click "{button_label}"'))
def click_button(driver, button_label):
    """Generic step: delegate to the correct page action based on label."""
    label = button_label.strip().lower()
    if label == "checkout":
        CartPage(driver).click_checkout()
    else:
        raise NotImplementedError(
            f"Button '{button_label}' is not mapped in checkout_cart_steps. "
            "Add a handler or use a more specific step."
        )


# ── Page assertion ────────────────────────────────────────────────
@then(parsers.parse('I should be on the "{page_title}" page'))
def verify_page_title(driver, page_title):
    from selenium.webdriver.common.by import By
    driver.implicitly_wait(5)
    title_el = driver.find_element(By.CLASS_NAME, "title")
    assert title_el.text == page_title, (
        f"Expected page '{page_title}' but got '{title_el.text}'"
    )


# ── Empty cart warning ────────────────────────────────────────────
@then(parsers.parse('I should see the message "{message}"'))
def see_message(driver, message):
    """
    SauceDemo does not display a native 'Your cart is empty' banner.
    This step verifies via the absence of items and a guard assertion.
    ⚠️ Open Question OQ-1: confirm whether a custom empty-cart message
       was added to the AUT, or adjust assertion strategy accordingly.
    """
    cart = CartPage(driver)
    if message == "Your cart is empty":
        assert cart.is_empty_cart_message_displayed(), (
            "Expected cart to be empty but items were present."
        )
    else:
        from selenium.webdriver.common.by import By
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert message in body_text, (
            f"Expected message '{message}' not found on page."
        )
