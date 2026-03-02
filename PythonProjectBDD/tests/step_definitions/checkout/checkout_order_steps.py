"""
tests/step_definitions/checkout/checkout_order_steps.py
─────────────────────────────────────────────────────────
pytest-bdd step definitions – Checkout Order Completion.

Stories  : MDP-312
Feature  : features/checkout/checkout_order.feature
Framework: pytest-bdd (migrated from Behave; suite now fully pytest-bdd)

Persona credentials (from SauceDemo):
    standard_user    / secret_sauce  → full access
    locked_out_user  / secret_sauce  → blocked at login
    problem_user     / secret_sauce  → degraded but reachable UI
"""

import pytest
from pytest_bdd import given, when, then, parsers, scenarios
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from features.pages.loginpage import LoginPage
from features.pages.checkoutpage import (
    InventoryPage,
    CartPage,
    CheckoutInfoPage,
    CheckoutOverviewPage,
    CheckoutCompletePage,
)
from POM_BDD.utilis import base_url

# ── Credentials map ───────────────────────────────────────────────
PERSONAS = {
    "standard_user":   "secret_sauce",
    "locked_out_user": "secret_sauce",
    "problem_user":    "secret_sauce",
}

# Bind all scenarios in the matching feature file
scenarios("../../../features/checkout/checkout_order.feature")


# ── Internal helpers ──────────────────────────────────────────────
def _login(driver, persona: str) -> None:
    """Navigate to SauceDemo and log in as the requested persona."""
    password = PERSONAS.get(persona, "secret_sauce")
    login = LoginPage(driver)
    login.loadpage(base_url)
    login.input_username(persona)
    login.input_password(password)
    login.click_login_button()


def _is_locked_out(driver) -> bool:
    """Return True when the login error banner is present (locked_out_user)."""
    try:
        driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
        return True
    except Exception:
        return False


# ── Background steps ──────────────────────────────────────────────
@given(parsers.parse('I am logged in as "{persona}"'))
def logged_in_as_persona(driver, persona):
    """
    Log in as the requested persona.
    locked_out_user will stop at the login error; this is
    asserted later in the persona outline step.
    """
    _login(driver, persona)


@given(parsers.parse('I have "{product}" in my cart'))
def product_in_cart(driver, product):
    InventoryPage(driver).add_item_to_cart(product)


@given(parsers.parse('I am on the "{page_title}" page'))
def navigate_to_named_page(driver, page_title):
    """Navigate to a named page by driving the UI (no hard URL jumps)."""
    if "Checkout: Your Information" in page_title:
        CartPage(driver).navigate_to_cart()
        CartPage(driver).click_checkout()
    # extend with additional page names as new scenarios require them


# ── Checkout info form ────────────────────────────────────────────
@when(parsers.parse('I enter first name "{value}"'))
def enter_first_name(driver, value):
    CheckoutInfoPage(driver).enter_first_name(value)


@when(parsers.parse('I enter last name "{value}"'))
def enter_last_name(driver, value):
    CheckoutInfoPage(driver).enter_last_name(value)


@when(parsers.parse('I enter postal code "{value}"'))
def enter_postal_code(driver, value):
    CheckoutInfoPage(driver).enter_postal_code(value)


@when("I leave the first name blank")
def leave_first_name_blank(driver):
    CheckoutInfoPage(driver).enter_first_name("")


@when("I leave the last name blank")
def leave_last_name_blank(driver):
    CheckoutInfoPage(driver).enter_last_name("")


@when("I leave the postal code blank")
def leave_postal_code_blank(driver):
    CheckoutInfoPage(driver).enter_postal_code("")


# ── Generic button click ──────────────────────────────────────────
@when(parsers.parse('I click "{button_label}"'))
def click_button_order(driver, button_label):
    label = button_label.strip().lower()
    if label == "continue":
        CheckoutInfoPage(driver).click_continue()
    elif label == "finish":
        CheckoutOverviewPage(driver).click_finish()
    elif label == "cancel":
        CheckoutInfoPage(driver).click_cancel()
    else:
        raise NotImplementedError(
            f"Button '{button_label}' is not mapped in checkout_order_steps. "
            "Add a handler or use a more specific step."
        )


# ── Page title assertions ─────────────────────────────────────────
@then(parsers.parse('I should be on the "{page_title}" page'))
def verify_page_title_order(driver, page_title):
    wait = WebDriverWait(driver, 10)
    title_el = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "title"))
    )
    assert title_el.text == page_title, (
        f"Expected page '{page_title}' but got '{title_el.text}'"
    )


# ── Order summary ─────────────────────────────────────────────────
@then(parsers.parse('I should see "{product}" in the order summary'))
def product_in_order_summary(driver, product):
    items = CheckoutOverviewPage(driver).get_item_names()
    assert product in items, (
        f"Expected '{product}' in order summary but found: {items}"
    )


@then("the item total should match the sum of all item prices")
def item_total_matches_sum(driver):
    overview = CheckoutOverviewPage(driver)
    prices   = overview.get_item_prices()
    subtotal = overview.get_subtotal()
    expected = round(sum(prices), 2)
    assert subtotal == expected, (
        f"Subtotal ${subtotal} does not match sum of item prices ${expected}"
    )


@then("the tax amount should be displayed")
def tax_displayed(driver):
    tax = CheckoutOverviewPage(driver).get_tax()
    assert tax > 0, "Expected a non-zero tax amount to be displayed."


@then("the order total should equal item total plus tax")
def total_equals_subtotal_plus_tax(driver):
    overview = CheckoutOverviewPage(driver)
    subtotal = overview.get_subtotal()
    tax      = overview.get_tax()
    total    = overview.get_total()
    expected = round(subtotal + tax, 2)
    assert total == expected, (
        f"Order total ${total} != subtotal ${subtotal} + tax ${tax} = ${expected}"
    )


# ── Confirmation page ─────────────────────────────────────────────
@then(parsers.parse('I should see the message "{message}"'))
def see_message(driver, message):
    if "Thank you for your order" in message:
        actual = CheckoutCompletePage(driver).get_confirmation_message()
        assert message in actual or actual == message, (
            f"Expected confirmation '{message}' but got '{actual}'"
        )
    else:
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert message in body_text, (
            f"Expected message '{message}' not found on page."
        )


# ── Error message assertions ──────────────────────────────────────
@then(parsers.parse('I should see the error message "{error_text}"'))
def see_error_message(driver, error_text):
    actual = CheckoutInfoPage(driver).get_error_message()
    assert error_text in actual, (
        f"Expected error '{error_text}' but got '{actual}'"
    )


# ── Cart content on cancel ────────────────────────────────────────
@then(parsers.parse('I should see "{product}" in the cart'))
def item_in_cart_after_cancel(driver, product):
    items = CartPage(driver).get_cart_item_names()
    assert product in items, (
        f"Expected '{product}' in cart but found: {items}"
    )


# ── Outline: generic result dispatcher ───────────────────────────
@then(parsers.parse('I should see the result "{expected_result}"'))
def see_result(driver, expected_result):
    """
    Routes the Scenario Outline 'expected_result' column:

      Checkout: Overview         → assert page title
      Error: <text>              → assert inline validation error
      locked_out                 → assert login error banner is present
                                   (locked_out_user never reaches checkout)
    """
    if expected_result == "locked_out":
        assert _is_locked_out(driver), (
            "Expected locked_out_user to see a login error banner, "
            "but no error element was found."
        )
    elif expected_result.startswith("Error:"):
        actual = CheckoutInfoPage(driver).get_error_message()
        assert expected_result in actual, (
            f"Expected error '{expected_result}' but got '{actual}'"
        )
    else:
        # Treat as a page title fragment
        wait = WebDriverWait(driver, 10)
        title_el = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "title"))
        )
        assert expected_result in title_el.text, (
            f"Expected page title containing '{expected_result}' "
            f"but got '{title_el.text}'"
        )
