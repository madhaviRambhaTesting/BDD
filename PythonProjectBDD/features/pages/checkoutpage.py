"""
Page Object: Checkout Pages
Covers cart page, checkout-information page, overview page, and confirmation page
on https://www.saucedemo.com
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    # Locators
    CART_ITEM_NAME    = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON   = (By.ID,         "checkout")
    CONTINUE_SHOPPING = (By.ID,         "continue-shopping")
    CART_BADGE        = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK         = (By.CLASS_NAME, "shopping_cart_link")
    REMOVE_BUTTON_TPL = "//div[text()='{name}']/ancestor::div[@class='cart_item']//button[contains(@id,'remove')]"

    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, 10)

    def navigate_to_cart(self):
        self.driver.find_element(*self.CART_LINK).click()

    def get_cart_badge_count(self):
        """Return the cart badge number as a string, or '0' if badge is absent."""
        try:
            badge = self.driver.find_element(*self.CART_BADGE)
            return badge.text
        except Exception:
            return "0"

    def get_cart_item_names(self):
        """Return a list of all item name strings currently in the cart."""
        items = self.driver.find_elements(*self.CART_ITEM_NAME)
        return [item.text for item in items]

    def click_checkout(self):
        self.driver.find_element(*self.CHECKOUT_BUTTON).click()

    def remove_item(self, product_name: str):
        xpath = self.REMOVE_BUTTON_TPL.format(name=product_name)
        self.driver.find_element(By.XPATH, xpath).click()

    def is_empty_cart_message_displayed(self):
        """
        SauceDemo does not natively show an 'empty cart' warning;
        this helper checks whether the cart item list is empty.
        """
        items = self.driver.find_elements(*self.CART_ITEM_NAME)
        return len(items) == 0


class InventoryPage:
    ADD_BUTTON_TPL    = "//div[text()='{name}']/ancestor::div[@class='inventory_item']//button[contains(@id,'add-to-cart')]"
    CART_BADGE        = (By.CLASS_NAME, "shopping_cart_badge")

    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, 10)

    def add_item_to_cart(self, product_name: str):
        xpath = self.ADD_BUTTON_TPL.format(name=product_name)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

    def get_cart_badge_count(self):
        try:
            badge = self.driver.find_element(*self.CART_BADGE)
            return badge.text
        except Exception:
            return "0"


class CheckoutInfoPage:
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

    def get_error_message(self):
        try:
            return self.driver.find_element(*self.ERROR_MSG).text
        except Exception:
            return ""

    def get_page_title(self):
        try:
            return self.driver.find_element(By.CLASS_NAME, "title").text
        except Exception:
            return ""


class CheckoutOverviewPage:
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

    def get_item_names(self):
        return [el.text for el in self.driver.find_elements(*self.ITEM_NAMES)]

    def get_item_prices(self):
        """Return item prices as a list of floats."""
        raw = self.driver.find_elements(*self.ITEM_PRICES)
        return [float(el.text.replace("$", "")) for el in raw]

    def get_subtotal(self):
        text = self.driver.find_element(*self.SUBTOTAL_LABEL).text
        return float(text.split("$")[-1])

    def get_tax(self):
        text = self.driver.find_element(*self.TAX_LABEL).text
        return float(text.split("$")[-1])

    def get_total(self):
        text = self.driver.find_element(*self.TOTAL_LABEL).text
        return float(text.split("$")[-1])

    def click_finish(self):
        self.driver.find_element(*self.FINISH_BTN).click()

    def get_page_title(self):
        try:
            return self.driver.find_element(By.CLASS_NAME, "title").text
        except Exception:
            return ""


class CheckoutCompletePage:
    CONFIRMATION_HEADER = (By.CLASS_NAME, "complete-header")
    BACK_HOME_BTN       = (By.ID,         "back-to-products")

    def __init__(self, driver):
        self.driver = driver

    def get_confirmation_message(self):
        try:
            return self.driver.find_element(*self.CONFIRMATION_HEADER).text
        except Exception:
            return ""

    def get_page_title(self):
        try:
            return self.driver.find_element(By.CLASS_NAME, "title").text
        except Exception:
            return ""
