from behave import given, when, then
from selenium.webdriver.common.by import By
from features.pages.loginpage import LoginPage
from POM_BDD.utilis import uname,passwd,base_url
@given('I am on the login page')
def step_open_login_page(context):
    context.login_page = LoginPage(context.driver)
    context.login_page.loadpage(base_url)


@when('I enter a valid username')
def step_enter_username(context):
    context.login_page.input_username(uname)


@when('I enter a valid password')
def step_enter_password(context):
    context.login_page.input_password(passwd)


@when('I click the login button')
def step_click_login_button(context):
    context.login_page.click_login_button()


@then('I should see the "Products" page')
def step_verify_products_page(context):
    context.driver.implicitly_wait(5)
    element = context.driver.find_element(By.XPATH, "//span[text()='Products']")
    assert element.text == "Products", "Login failed! 'Products' text not found."


@then('there should be only one window open')
def step_verify_single_window_open(context):
    # Verify there is only one browser window open
    window_handles = context.driver.window_handles
    print(f"Number of windows open: {len(window_handles)}")
    assert len(window_handles) == 1, "Unexpected number of windows open after login!"