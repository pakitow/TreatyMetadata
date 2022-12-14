from imports import download_xlsx, files, links, json, requests, pd, np, os, folders, ET, bs4, time, re, string
from bs4 import BeautifulSoup
from lxml import etree
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException as NoEleExc

with open("metadata.json",encoding="utf-8") as json_file_1:
    metadata = json.load(json_file_1)
with open("RTAI_website_html.json", encoding="utf-8") as json_file_2:
    rtais_id = json.load(json_file_2)

options = Options(); options.headless = True
driver = webdriver.Chrome(options=options)

driver.get(links['wto'])
WebDriverWait(driver,10).until(
    EC.element_to_be_clickable((By.ID, 'ContentPlaceHolder1_lnkSearchCriteria'))
)
searchButton = driver.find_element(by=By.ID,value='ContentPlaceHolder1_lnkSearchCriteria')
searchButton_href = searchButton.get_attribute('href')

def get_rta_card_url(metadata: dict, href: str, driver) -> str:
    for key in metadata:
        try:
            driver.get(href)
            WebDriverWait(driver,10).until(
                EC.element_to_be_clickable((By.ID,
                'ContentPlaceHolder1_txtAgrName'))
            )
            field = driver.find_element(By.ID, 'ContentPlaceHolder1_txtAgrName')
            if field.get_attribute('value') != None: field.clear()
            field.send_keys(metadata[key]['name'])
            WebDriverWait(driver,10).until(
                EC.element_to_be_clickable((By.ID,
                'ContentPlaceHolder1_btnSearch'))
            )
            driver.find_element(By.ID, 'ContentPlaceHolder1_btnSearch').click()
            WebDriverWait(driver,10).until(
                EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_grdRTAList_RTAIDHyperLink_0"))
            ); driver.find_element(By.ID,'ContentPlaceHolder1_grdRTAList_RTAIDHyperLink_0').click()
            WebDriverWait(driver,10).until(EC.url_changes(driver.current_url))
            return driver.current_url.rsplit("=")[0]
        except Exception as e: print(e)


rta_card_url = get_rta_card_url(metadata, searchButton_href, driver)
for key in metadata:
    driver.get(rta_card_url+"="+str(metadata[key]['wto_id']))
    WebDriverWait(driver,10).until(
        EC.element_to_be_clickable((By.CLASS_NAME,"panelValueBold"))
    )
    print(driver.current_url)




