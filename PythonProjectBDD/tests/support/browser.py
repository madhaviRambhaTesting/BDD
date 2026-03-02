"""
tests/support/browser.py
────────────────────────
Shared browser-factory helper for the pytest-bdd checkout suite.

Stories : MDP-310 | MDP-312
Framework: pytest-bdd + Selenium

Usage
-----
    from tests.support.browser import make_chrome_driver

    driver = make_chrome_driver(headless=True)   # CI default
    driver = make_chrome_driver(headless=False)  # local debug
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def make_chrome_driver(headless: bool = True) -> webdriver.Chrome:
    """
    Build and return a configured Chrome WebDriver.

    Parameters
    ----------
    headless : bool
        Run in headless mode (default: True).  Set to False for local
        visual debugging.  Controlled via conftest.py fixture.
    """
    options = Options()

    if headless:
        # --headless=new is the Chromium-recommended flag (Chrome ≥ 112)
        options.add_argument("--headless=new")

    # Common CI/container flags
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver
