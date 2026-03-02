"""
conftest.py – pytest-bdd driver fixture for the Checkout test suite.

Provides
--------
  driver   : headless Chrome by default (CI-safe).
             Set environment variable HEADLESS=false for local visual debug.

Stories  : MDP-310 | MDP-312
Framework: pytest-bdd
"""

import os
import pytest
from tests.support.browser import make_chrome_driver


@pytest.fixture(scope="function")
def driver():
    """
    Spin up a Chrome WebDriver for each test function.

    Headless mode is ON by default.
    Override locally:
        HEADLESS=false pytest tests/step_definitions/checkout/ -v
    """
    headless = os.environ.get("HEADLESS", "true").lower() != "false"
    _driver = make_chrome_driver(headless=headless)
    yield _driver
    _driver.quit()
