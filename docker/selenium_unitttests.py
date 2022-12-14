from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Remote(
    command_executor="http://54.146.247.54:4445",
    desired_capabilities={
        "browserName":"chrome"
    }
)
driver.quit()
#driver.get("https://github.com")