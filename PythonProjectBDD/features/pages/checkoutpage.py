"""
features/pages/checkoutpage.py
Page Object classes for the SauceDemo checkout flow.

Classes
-------
  CartPage             - Shopping cart page (/cart.html)
  InventoryPage        - Products listing page (/)
  CheckoutInfoPage     - Checkout step 1: shipping info
  CheckoutOverviewPage - Checkout step 2: order overview
  CheckoutCompletePage - Checkout step 3: confirmation

Stories  : MDP-9 | MDP-14
Framework: pytest-bdd + Selenium (headless Chrome)

Locator note (AC-CART-3)
------------------------
  EMPTY_CART_BANNER uses data-test="cart-empty-banner" -- the confirmed
  AUT attribute.  Previous iterations used data-testid; corrected here.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    # ── Locators ──────────────────────────────────────────────────────────────
    CART_ITEM_NAME    = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON   = (By.ID,         "checkout")
    CONTINUE_SHOPPING = (By.ID,         "continue-shopping")
    CART_BADGE        = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK         = (By.CLASS_NAME, "shopping_cart_link")
    # AC-CART-3: confirmed AUT selector — data-test (NOT data-testid)
    EMPTY_CART_BANNER = (By.CSS_SELECTOR, "[data-test='cart-empty-banner']")
    REMOVE_BUTTON_TPL = (
        "//div[text()='{name}']"
        "/ancestor::div[@class='cart_item']"
        "//button[contains(@id,'remove')]"
    )

    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, 10)

    def navigate_to_cart(self):
        self.driver.find_element(*self.CART_LINK).click()

    def get_cart_badge_count(self):
        """Return the cart badge number as a string, or '0' if badge absent."""
        try:
            badge = self.driver.find_element(*self.CART_BADGE)
            return badge.text
        except Exception:
            return "0"

    def get_cart_item_names(self):
        """Return a list of all item-name strings currently in the cart."""
        items = self.driver.find_elements(*self.CART_ITEM_NAME)
        return [item.text for item in items]

    def click_checkout(self):
        self.driver.find_element(*self.CHECKOUT_BUTTON).click()

    def remove_item(self, product_name: str):
        xpath = self.REMOVE_BUTTON_TPL.format(name=product_name)
        self.driver.find_element(By.XPATH, xpath).click()

    def is_empty_cart_banner_displayed(self) -> bool:
        """
        AC-CART-3: Return True when the data-test='cart-empty-banner'
        element is present and visible after the last item is removed.
        Selector confirmed against AUT: data-test="cart-empty-banner".
        """
        try:
            banner = self.wait.until(
                EC.visibility_of_element_located(self.EMPTY_CART_BANNER)
            )
            return banner.is_displayed()
        except Exception:
            return False

    # ── Legacy alias (kept for backwards compatibility) ───────────────────────
    def is_empty_cart_message_displayed(self) -> bool:
        """Alias for is_empty_cart_banner_displayed()."""
        return self.is_empty_cart_banner_displayed()


class InventoryPage:
    # ── Locators ──────────────────────────────────────────────────────────────
    ADD_BUTTON_TPL = (
        "//div[text()='{name}']"
        "/ancestor::div[@class='inventory_item']"
        "//button[contains(@id,'add-to-cart')]"
    )
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, 10)

    def add_item_to_cart(self, product_name: str):
        xpath = self.ADD_BUTTON_TPL.format(name=product_name)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

    def get_cart_badge_count(self) -> str:
        """Return badge count as string, or '0' if badge is absent."""
        try:
            badge = self.driver.find_element(*self.CART_BADGE)
            return badge.text
        except Exception:
            return "0"


class CheckoutInfoPage:
    # ── Locators ──────────────────────────────────────────────────────────────
    FIRST_NAME_FIELD = (By.ID, "first-name")
    LAST_NAME_FIELD  = (By.ID, "last-name")
    POSTAL_CODE      = (By.ID, "postal-code")
    CONTINUE_BTN     = (By.ID, "continue")
    CANCEL_BTN       = (By.ID, "cancel")
    ERROR_MSG        = (By.CSS_SELECTOR, "h3[data-test='error']")

    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, 10)

    def enter_first_name(self, value: str):
        field = self.driver.find_element(*self.FIRST_NAME_FIELD)
        field.clear()
        if value:
            field.send_keys(value)

    def enter_last_name(self, value: str):
        field = self.driver.find_element(*self.LAST_NAME_FIELD)
        field.clear()
        if value:
            field.send_keys(value)

    def enter_postal_code(self, value: str):
        field = self.driver.find_element(*self.POSTAL_CODE)
        field.clear()
        if value:
            field.send_keys(value)

    def click_continue(self):
        self.driver.find_element(*self.CONTINUE_BTN).click()

    def click_cancel(self):
        self.driver.find_element(*self.CANCEL_BTN).click()

    def get_error_message(self) -> str:
        try:
            return self.driver.find_element(*self.ERROR_MSG).text
        except Exception:
            return ""

    def get_page_title(self) -> str:
        try:
            return self.driver.find_element(By.CLASS_NAME, "title").text
        except Exception:
            return ""


class CheckoutOverviewPage:
    # ── Locators ──────────────────────────────────────────────────────────────
    ITEM_NAMES     = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES    = (By.CLASS_NAME, "inventory_item_price")
    SUBTOTAL_LABEL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX_LABEL      = (By.CLASS_NAME, "summary_tax_label")
    TOTAL_LABEL    = (By.CLASS_NAME, "summary_total_label")
    FINISH_BTN     = (By.ID,         "finish")
    CANCEL_BTN     = (By.ID,         "cancel")

    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, 10)

    def get_item_names(self) -> list:
        return [el.text for el in self.driver.find_elements(*self.ITEM_NAMES)]

    def get_item_prices(self) -> list:
        """Return item prices as a list of floats."""
        raw = self.driver.find_elements(*self.ITEM_PRICES)
        return [float(el.text.replace("$", "")) for el in raw]

    def get_subtotal(self) -> float:
        text = self.driver.find_element(*self.SUBTOTAL_LABEL).text
        return float(text.split("$")[-1])

    def get_tax(self) -> float:
        text = self.driver.find_element(*self.TAX_LABEL).text
        return float(text.split("$")[-1])

    def get_total(self) -> float:
        text = self.driver.find_element(*self.TOTAL_LABEL).text
        return float(text.split("$")[-1])

    def click_finish(self):
        self.driver.find_element(*self.FINISH_BTN).click()

    def get_page_title(self) -> str:
        try:
            return self.driver.find_element(By.CLASS_NAME, "title").text
        except Exception:
            return ""


class CheckoutCompletePage:
    # ── Locators ──────────────────────────────────────────────────────────────
    CONFIRMATION_HEADER = (By.CLASS_NAME, "complete-header")
    BACK_HOME_BTN       = (By.ID,         "back-to-products")

    def __init__(self, driver):
        self.driver = driver

    def get_confirmation_message(self) -> str:
        try:
            return self.driver.find_element(*self.CONFIRMATION_HEADER).text
        except Exception:
            return ""

    def get_page_title(self) -> str:
        try:
            return self.driver.find_element(By.CLASS_NAME, "title").text
        except Exception:
            return ""
