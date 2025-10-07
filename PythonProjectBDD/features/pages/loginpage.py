from selenium.webdriver.common.by import By

class LoginPage:
    username_field = (By.ID, "user-name")
    password_field = (By.ID, "password")
    login_button = (By.ID, "login-button")

    def __init__(self, driver):

        self.driver = driver
    def loadpage(self,url):
        self.driver.implicitly_wait(5)
        self.driver.get(url)
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)

    def input_username(self, username):
        username_input = self.driver.find_element(*LoginPage.username_field)
        username_input.clear()
        username_input.send_keys(username)

    def input_password(self, password):
        password_input = self.driver.find_element(*LoginPage.password_field)
        password_input.clear()
        password_input.send_keys(password)

    def click_login_button(self):
        self.driver.find_element(*LoginPage.login_button).click()