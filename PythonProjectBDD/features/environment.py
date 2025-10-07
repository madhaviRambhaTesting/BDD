from selenium import webdriver
def before_scenario(context):
    context.driver = webdriver.Chrome()



def after_scenario(context):
    context.driver.quit()