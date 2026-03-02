"""
Step Definitions – Checkout Order Completion
Story: PAYSTRM-202
Feature: features/checkout/checkout_order.feature
Framework: pytest-bdd  (Behave-compatible context reused via conftest fixture)
"""
import pytest
from pytest_bdd import given, when, then, parsers, scenarios

from features.pages.loginpage    import LoginPage
from features.pages.checkoutpage import (
    InventoryPage,
    CartPage,
    CheckoutInfoPage,
    CheckoutOverviewPage,
    CheckoutCompletePage,
)
from POM_BDD.utilis import base_url, uname, passwd

# Bind all scenarios in the matching feature file
scenarios("../../../features/checkout/checkout_order.feature")


# ── Background steps ─────────────────────────────────────────────
@given("I am logged in as a standard user")
def logged_in_standard_user(driver):
    login = LoginPage(driver)
    login.loadpage(base_url)
    login.input_username(uname)
    login.input_password(passwd)
    login.click_login_button()


@given(parsers.parse('I have "{product}" in my cart'))
def product_in_cart(driver, product):
    inv = InventoryPage(driver)
    inv.add_item_to_cart(product)


@given(parsers.parse('I am on the "{page_title}" page'))
def on_page(driver, page_title):
    """Navigate to the checkout info page by going through the cart."""
    if "Checkout: Your Information" in page_title:
        CartPage(driver).navigate_to_cart()
        CartPage(driver).click_checkout()
    # extend with more page names as needed


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


# ── Generic button click (Continue / Finish / Cancel) ────────────
@when(parsers.parse('I click "{button_label}"'))
def click_button(driver, button_label):
    label = button_label.strip().lower()
    if label == "continue":
        CheckoutInfoPage(driver).click_continue()
    elif label == "finish":
        CheckoutOverviewPage(driver).click_finish()
    elif label == "cancel":
        CheckoutInfoPage(driver).click_cancel()
    else:
        raise NotImplementedError(
            f"Button '{button_label}' is not mapped in checkout_order_steps."
        )


# ── Page title assertions ─────────────────────────────────────────
@then(parsers.parse('I should be on the "{page_title}" page'))
def verify_page_title(driver, page_title):
    from selenium.webdriver.common.by import By
    driver.implicitly_wait(5)
    title_el = driver.find_element(By.CLASS_NAME, "title")
    assert title_el.text == page_title, (
        f"Expected page '{page_title}' but got '{title_el.text}'"
    )


# ── Order summary assertions ──────────────────────────────────────
@then(parsers.parse('I should see "{product}" in the order summary'))
def product_in_order_summary(driver, product):
    overview = CheckoutOverviewPage(driver)
    items = overview.get_item_names()
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
        f"Subtotal ${subtotal} does not match sum of prices ${expected}"
    )


@then("the tax amount should be displayed")
def tax_displayed(driver):
    overview = CheckoutOverviewPage(driver)
    tax = overview.get_tax()
    assert tax > 0, "Expected a non-zero tax amount to be displayed."


@then("the order total should equal item total plus tax")
def total_equals_subtotal_plus_tax(driver):
    overview  = CheckoutOverviewPage(driver)
    subtotal  = overview.get_subtotal()
    tax       = overview.get_tax()
    total     = overview.get_total()
    expected  = round(subtotal + tax, 2)
    assert total == expected, (
        f"Order total ${total} != subtotal ${subtotal} + tax ${tax} = ${expected}"
    )


# ── Confirmation page ─────────────────────────────────────────────
@then(parsers.parse('I should see the message "{message}"'))
def see_message(driver, message):
    complete = CheckoutCompletePage(driver)
    if "Thank you for your order" in message:
        actual = complete.get_confirmation_message()
        assert message in actual or actual == message, (
            f"Expected confirmation '{message}' but got '{actual}'"
        )
    else:
        from selenium.webdriver.common.by import By
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert message in body_text, (
            f"Expected message '{message}' not found on page."
        )


# ── Error message assertions ──────────────────────────────────────
@then(parsers.parse('I should see the error message "{error_text}"'))
def see_error_message(driver, error_text):
    info   = CheckoutInfoPage(driver)
    actual = info.get_error_message()
    assert error_text in actual, (
        f"Expected error '{error_text}' but got '{actual}'"
    )


# ── Outline: generic result assertion ────────────────────────────
@then(parsers.parse('I should see the result "{expected_result}"'))
def see_result(driver, expected_result):
    """
    Handles the Scenario Outline 'expected_result' column.
    Routes to page-title check or error-message check.
    """
    if expected_result.startswith("Error:"):
        info   = CheckoutInfoPage(driver)
        actual = info.get_error_message()
        assert expected_result in actual, (
            f"Expected error '{expected_result}' but got '{actual}'"
        )
    else:
        from selenium.webdriver.common.by import By
        driver.implicitly_wait(5)
        title_el = driver.find_element(By.CLASS_NAME, "title")
        assert expected_result in title_el.text, (
            f"Expected page title containing '{expected_result}' "
            f"but got '{title_el.text}'"
        )


# ── Cart content on cancel ────────────────────────────────────────
@then(parsers.parse('I should see "{product}" in the cart'))
def item_in_cart(driver, product):
    cart  = CartPage(driver)
    items = cart.get_cart_item_names()
    assert product in items, (
        f"Expected '{product}' in cart but found: {items}"
    )
