from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dictionaries import links, files, html
import time, os


def run():
    if os.path.exists(files['spreadsheet']): os.remove(files['spreadsheet'])
    driver = webdriver.Chrome(files['chrome-driver'])
    driver.get(links['wto'])
    WebDriverWait(driver,10).until(
        EC.element_to_be_clickable( (By.ID, html['export-id'] ) )
    ); driver.find_element(by=By.ID,value=html['export-id']).click()
    while not os.path.exists(files['spreadsheet']): time.sleep(0.01)
    driver.quit()