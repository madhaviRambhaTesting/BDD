"""
tests/step_definitions/checkout/checkout_cart_steps.py
--------------------------------------------------------
pytest-bdd step definitions for: Checkout Cart Management.

Stories  : MDP-9  - [PayStream Q2] EPIC: Functional and Integration Testing
           MDP-14 - [PayStream Q2] Functional & Regression Testing Execution
Feature  : features/checkout/checkout_cart.feature
Framework: pytest-bdd + Selenium (headless Chrome; HEADLESS=false for local debug)

Persona matrix
--------------
  standard_user    / secret_sauce  -> full access, all scenarios
  problem_user     / secret_sauce  -> degraded UI but add-to-cart works; badge = 1
  locked_out_user  -> see dedicated @xfail scenario in checkout_order.feature
"""

from pytest_bdd import given, when, then, parsers, scenarios
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from features.pages.loginpage import LoginPage
from features.pages.checkoutpage import InventoryPage, CartPage
from POM_BDD.utilis import base_url

# ---------------------------------------------------------------------------
# Persona credentials
# ---------------------------------------------------------------------------
PERSONAS = {
    "standard_user":   "secret_sauce",
    "locked_out_user": "secret_sauce",
    "problem_user":    "secret_sauce",
}

# Bind all scenarios declared in the matching feature file
scenarios("../../../features/checkout/checkout_cart.feature")


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _login(driver, persona: str) -> None:
    """Navigate to SauceDemo and log in as the requested persona."""
    password = PERSONAS.get(persona, "secret_sauce")
    page = LoginPage(driver)
    page.loadpage(base_url)
    page.input_username(persona)
    page.input_password(password)
    page.click_login_button()


def _is_locked_out(driver) -> bool:
    """Return True when the login error banner is visible."""
    try:
        driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
        return True
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Background
# ---------------------------------------------------------------------------

@given(parsers.parse('I am logged in as "{persona}"'))
def logged_in_as_persona(driver, persona):
    """
    Log in as the requested persona.
    locked_out_user lands on the login page with an error banner --
    that behaviour is asserted in the dedicated @xfail scenario in
    checkout_order.feature, not here.
    """
    _login(driver, persona)


# ---------------------------------------------------------------------------
# Add / remove items
# ---------------------------------------------------------------------------

@when(parsers.parse('I add "{product}" to the cart'))
def add_product_to_cart(driver, product):
    InventoryPage(driver).add_item_to_cart(product)


@when(parsers.parse('I remove "{product}" from the cart'))
def remove_product_from_cart(driver, product):
    CartPage(driver).remove_item(product)


# ---------------------------------------------------------------------------
# Cart badge
# ---------------------------------------------------------------------------

@then(parsers.parse('the cart badge should show "{count}"'))
def verify_cart_badge(driver, count):
    actual = InventoryPage(driver).get_cart_badge_count()
    assert actual == count, (
        f"Expected cart badge '{count}' but got '{actual}'"
    )


# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------

@when("I navigate to the cart")
def navigate_to_cart(driver):
    CartPage(driver).navigate_to_cart()


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


# ---------------------------------------------------------------------------
# Cart item assertions
# ---------------------------------------------------------------------------

@then(parsers.parse('I should see "{product}" in the cart'))
def item_visible_in_cart(driver, product):
    items = CartPage(driver).get_cart_item_names()
    assert product in items, (
        f"Expected '{product}' in cart but found: {items}"
    )


@then(parsers.parse('I should not see "{product}" in the cart'))
def item_not_visible_in_cart(driver, product):
    items = CartPage(driver).get_cart_item_names()
    assert product not in items, (
        f"Expected '{product}' to be absent from cart but it was present."
    )


# ---------------------------------------------------------------------------
# Page title assertion
# ---------------------------------------------------------------------------

@then(parsers.parse('I should be on the "{page_title}" page'))
def verify_page_title_cart(driver, page_title):
    wait = WebDriverWait(driver, 10)
    title_el = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "title"))
    )
    assert title_el.text == page_title, (
        f"Expected page '{page_title}' but got '{title_el.text}'"
    )


# ---------------------------------------------------------------------------
# Empty-cart banner (AC-CART-3)
# ---------------------------------------------------------------------------

@then("the empty-cart banner should be visible")
def empty_cart_banner_visible(driver):
    """
    AC-CART-3: After the last item is removed (or Checkout is clicked on
    an empty cart) the element with data-test="cart-empty-banner" must be
    present and visible.

    Confirmed AUT selector: data-test="cart-empty-banner"
    (CartPage.is_empty_cart_banner_displayed() encapsulates this locator.)
    """
    cart = CartPage(driver)
    assert cart.is_empty_cart_banner_displayed(), (
        "Expected empty-cart banner (data-test='cart-empty-banner') to be "
        "visible after removing the last cart item, but it was not found."
    )


# ---------------------------------------------------------------------------
# Persona-outline outcome dispatcher
# ---------------------------------------------------------------------------

@then(parsers.parse('the cart outcome should be "{expected_outcome}"'))
def verify_cart_outcome(driver, expected_outcome):
    """
    Routes Scenario Outline 'expected_outcome' values:

      badge:<n>  -> assert cart badge count equals <n>
      locked_out -> assert login error banner is present
                   (for any row that somehow uses locked_out_user)
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
