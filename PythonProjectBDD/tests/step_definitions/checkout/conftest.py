"""
conftest.py – pytest-bdd driver fixture for the Checkout test suite.

Provides:
  - `driver` fixture: launches Chrome, yields to the test, quits afterwards.
  - Feature-file base directory so pytest-bdd can resolve relative paths.

Stories: PAYSTRM-201, PAYSTRM-202
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="function")
def driver():
    """Spin up a Chrome WebDriver instance for each test function."""
    chrome_options = Options()
    # Uncomment the next line for headless execution in CI pipelines:
    # chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    _driver = webdriver.Chrome(options=chrome_options)
    _driver.implicitly_wait(10)
    yield _driver
    _driver.quit()
