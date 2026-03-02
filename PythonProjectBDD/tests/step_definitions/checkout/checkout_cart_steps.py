"""
tests/step_definitions/checkout/checkout_cart_steps.py
────────────────────────────────────────────────────────
pytest-bdd step definitions – Checkout Cart Management.

Stories  : MDP-310
Feature  : features/checkout/checkout_cart.feature
Framework: pytest-bdd (migrated from Behave; suite now fully pytest-bdd)

Persona credentials (from SauceDemo):
    standard_user    / secret_sauce  → full access
    locked_out_user  / secret_sauce  → blocked at login
    problem_user     / secret_sauce  → degraded UI behaviour
"""

import pytest
from pytest_bdd import given, when, then, parsers, scenarios
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from features.pages.loginpage import LoginPage
from features.pages.checkoutpage import InventoryPage, CartPage
from POM_BDD.utilis import base_url

# ── Credentials map ───────────────────────────────────────────────
PERSONAS = {
    "standard_user":   "secret_sauce",
    "locked_out_user": "secret_sauce",
    "problem_user":    "secret_sauce",
}

# Bind all scenarios in the matching feature file
scenarios("../../../features/checkout/checkout_cart.feature")


# ── Helpers ───────────────────────────────────────────────────────
def _login(driver, persona: str) -> None:
    """Log in with the given SauceDemo persona."""
    password = PERSONAS.get(persona, "secret_sauce")
    login = LoginPage(driver)
    login.loadpage(base_url)
    login.input_username(persona)
    login.input_password(password)
    login.click_login_button()


def _is_locked_out(driver) -> bool:
    """Return True when the login error banner is visible (locked_out_user)."""
    try:
        driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
        return True
    except Exception:
        return False


# ── Background ────────────────────────────────────────────────────
@given(parsers.parse('I am logged in as "{persona}"'))
def logged_in_as_persona(driver, persona):
    """
    Log in as the requested persona.
    locked_out_user will land on the login page with an error — that is
    the expected behaviour and is asserted in the outline steps.
    """
    _login(driver, persona)


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
    CartPage(driver).navigate_to_cart()


# ── Assert item present ───────────────────────────────────────────
@then(parsers.parse('I should see "{product}" in the cart'))
def item_visible_in_cart(driver, product):
    items = CartPage(driver).get_cart_item_names()
    assert product in items, (
        f"Expected '{product}' in cart but found: {items}"
    )


# ── Assert item absent ────────────────────────────────────────────
@then(parsers.parse('I should not see "{product}" in the cart'))
def item_not_visible_in_cart(driver, product):
    items = CartPage(driver).get_cart_item_names()
    assert product not in items, (
        f"Expected '{product}' to be absent from cart but it was present."
    )


# ── Remove item ───────────────────────────────────────────────────
@when(parsers.parse('I remove "{product}" from the cart'))
def remove_product_from_cart(driver, product):
    CartPage(driver).remove_item(product)


# ── Click Checkout ────────────────────────────────────────────────
@when(parsers.parse('I click "{button_label}"'))
def click_button_cart(driver, button_label):
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
def verify_page_title_cart(driver, page_title):
    wait = WebDriverWait(driver, 10)
    title_el = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "title")))
    assert title_el.text == page_title, (
        f"Expected page '{page_title}' but got '{title_el.text}'"
    )


# ── Empty-cart banner (AC-CART-3) ─────────────────────────────────
@then("the empty-cart banner should be visible")
def empty_cart_banner_visible(driver):
    """
    AC-CART-3: after the last item is removed (or Checkout is clicked on
    an empty cart), the element with data-testid="empty-cart-banner" must
    be present and visible.
    """
    wait = WebDriverWait(driver, 10)
    banner = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "[data-testid='empty-cart-banner']")
        ),
        message="Expected empty-cart-banner (data-testid='empty-cart-banner') "
                "to be visible after removing the last cart item."
    )
    assert banner.is_displayed(), (
        "empty-cart-banner element found but is not displayed."
    )


# ── Persona-outline outcome ───────────────────────────────────────
@then(parsers.parse('the cart outcome should be "{expected_outcome}"'))
def verify_cart_outcome(driver, expected_outcome):
    """
    Routes outline expected_outcome values:
      badge:<n>  → assert cart badge count equals <n>
      locked_out → assert login error banner is present
    """
    if expected_outcome.startswith("badge:"):
        expected_count = expected_outcome.split(":")[1]
        actual = InventoryPage(driver).get_cart_badge_count()
        assert actual == expected_count, (
            f"Expected badge '{expected_count}' but got '{actual}'"
        )
    elif expected_outcome == "locked_out":
        assert _is_locked_out(driver), (
            "Expected locked_out_user to see login error but no error was found."
        )
    else:
        raise ValueError(
            f"Unrecognised cart outcome '{expected_outcome}'. "
            "Use 'badge:<n>' or 'locked_out'."
        )
