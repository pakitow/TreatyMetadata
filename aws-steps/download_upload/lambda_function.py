import os, time
import boto3
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

def lambda_function(event, context):
    bucket = 'dependencies-pandas-selenium'
    prefs = {'download.default_directory':'/tmp/downloads', 'directory_updgrade':True}

    options = Options()
    options.binary_location = '/opt/headless-chromium'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option('prefs',prefs)

    driver = webdriver.Chrome('/opt/chromedriver',chrome_options=options)

    driver.command_executor._commands["send_command"] = ("POST","/session/$sessionId/chromium/send_command",)
    params = {"cmd":"Page.setDownloadBehavior","params":{"behavior":"allow","downloadPath":"/tmp/downloads"},}
    driver.execute("send_command",params)
    
    driver.get("http://rtais.wto.org/UI/PublicMaintainRTAHome.aspx")
    element = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.ID, "ContentPlaceHolder1_lnkExport"))
    driver.get(element.get_attribute('href'))

    while not os.path.exists("/tmp/downloads/AllRTAs.xls"):
        time.sleep(0.00001)
    
    s3 = boto3.resource('s3')
    s3.Object(bucket, 'AllRTAsWTO.xls').upload_file("/tmp/downloads/AllRTAs.xls")
    response = {
        "statusCode": 200,
    }
    driver.close()
    driver.quit()
    return response