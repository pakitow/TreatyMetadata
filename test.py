import json, requests, hashlib, io
from imports import links
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from urllib.request import FancyURLopener, urlopen, build_opener




#options = Options(); options.headless = True
#driver = webdriver.Chrome(options=options)

#driver.get(links['wto'])

headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.17 (KHTML, like Gecko)  Chrome/24.0.1312.57 Safari/537.17',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'
}

opener = build_opener()
opener.addheaders.append(('Cookie', 'ASP.NET_SessionId=garbagegarbagegarbagelol'))
f = opener.open("http://rtais.wto.org/UI/PublicAllRTAList.aspx")
html = f.read()
print(html)