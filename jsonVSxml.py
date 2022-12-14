from imports import download_xlsx, files, links, json, requests, pd, np, os, folders, ET, bs4, time, re, string, ParserCreate, ExpatError, errors
import subprocess
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException as NoEleExc

with open("metadata.json", encoding='utf-8') as json_file:
    metadata = json.load(json_file)

for key in metadata:
    p = os.path.join(folders['xml'],metadata[key]['file'])
    with open(p) as xmlfile:
        parser = ET.XMLParser()#encoding="utf-8")
        try:
            tree = ET.parse(xmlfile,parser)
            meta = tree.getroot().find('meta')
            x = meta.find('parties').findall('partyisocode')
        except ET.ParseError as e:
            print(key," -> ",e.msg)
            subprocess.call(['open','-a','/Applications/Visual Studio Code.app',p])
