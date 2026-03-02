"""
tests/step_definitions/login/login_steps.py
────────────────────────────────────────────
pytest-bdd step definitions for the Login feature.

Migration note
--------------
The original file at features/steps/login_steps.py used the Behave
framework (from behave import given, when, then).  This file is the
pytest-bdd equivalent so the full suite runs under a single runner.

Stories  : MDP-310 | MDP-312 (shared login prerequisite)
Feature  : features/login.feature
Framework: pytest-bdd
"""

import pytest
from pytest_bdd import given, when, then, parsers, scenarios
from selenium.webdriver.common.by import By

from features.pages.loginpage import LoginPage
from POM_BDD.utilis import base_url, uname, passwd

# Bind all scenarios declared in the login feature file
scenarios("../../../features/login.feature")


# ── Background / setup ────────────────────────────────────────────
@given("I am on the login page")
def step_open_login_page(driver):
    login_page = LoginPage(driver)
    login_page.loadpage(base_url)


# ── Actions ───────────────────────────────────────────────────────
@when("I enter a valid username")
def step_enter_username(driver):
    LoginPage(driver).input_username(uname)


@when("I enter a valid password")
def step_enter_password(driver):
    LoginPage(driver).input_password(passwd)


@when("I click the login button")
def step_click_login_button(driver):
    LoginPage(driver).click_login_button()


# ── Assertions ────────────────────────────────────────────────────
@then('I should see the "Products" page')
def step_verify_products_page(driver):
    driver.implicitly_wait(5)
    element = driver.find_element(By.XPATH, "//span[text()='Products']")
    assert element.text == "Products", "Login failed! 'Products' text not found."


@then("there should be only one window open")
def step_verify_single_window_open(driver):
    window_handles = driver.window_handles
    assert len(window_handles) == 1, (
        f"Expected 1 window but found {len(window_handles)} after login."
    )
