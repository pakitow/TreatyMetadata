from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

options = Options()
prefs = {"download.default_directory":"/home/ec2-user/selenium_test/downloads"}
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("enable-automation")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")
options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.get("https://rtais.wto.org/UI/PublicMaintainRTAHome.aspx")
WebDriverWait(driver,10).until(
    EC.element_to_be_clickable( (By.ID, "ContentPlaceHolder1_lnkExport" ))
)
driver.find_element(by=By.ID,value="ContentPlaceHolder1_lnkExport").click()
driver.quit()

