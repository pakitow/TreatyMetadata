from cgitb import html
from imports import requests, links, json, unicodedata
from bs4 import BeautifulSoup
html_text = requests.get(links['country-codes']).content
soup = BeautifulSoup(html_text,'html.parser')
tableTag = soup.table
tableHead = tableTag.thead.tr
tableBody = tableTag.tbody.find_all('tr')
countries = {}
codes = {}
for tr in tableBody:
    tdata = tr.find_all('td')
    tname = tdata[0].get_text()
    tcode = tdata[2].get_text()
    countries[tname] = tcode#{"Name": tname, "ISOCode": tcode}
    codes[tcode] = tname

#print(countries)
with open("countryToCode.json","w",encoding='utf-8') as outf: 
    json.dump(countries, outf, ensure_ascii=False)
with open("codeToCountries.json","w",encoding='utf-8') as outf:
    json.dump(codes,outf,ensure_ascii=False)
