from imports import download_xlsx, files, links, json, requests, pd, np, os, folders, ET
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from lxml import etree

metadata = {}

data_escap = pd.read_excel(io = files['dataset'], sheet_name = 0)
escap = {'in-wto': [pd.isna(data_escap['treaty_identifier_wto'].str.contains("NA")),
pd.isna(data_escap['treaty_identifier_wto'])==False]}
data_escap = data_escap[escap['in-wto'][0] & escap['in-wto'][1]]
data_wto = pd.read_excel(io = files['spreadsheet'], sheet_name = 0)


for index, row in data_escap.iterrows():
        metadata[row['fileName'].rsplit('.')[0]] = {
            "file": row['fileName'],
            "name": "",
            "wto_id": row["treaty_identifier_wto"],
            "type": "",
            "status": "",
            "notification": "",
            "date-signature": "",
            "date-into-force":"",
            "date-notification": "",
            "end-implementation": "",
            "date-inactive": "",
            "composition": "",
            "region": "",
            "parties-wto": "",
            "crossregional": "",
            "parties": {
            }
    }

with open("metadata.json","w",encoding='utf-8') as outf: 
    json.dump(metadata, outf, ensure_ascii=False)
with open("codeToCountries.json",encoding='utf-8') as codes:
    codeDict = json.load(codes)
with open("countryToCode.json",encoding='utf-8') as countries:
    countryDict = json.load(countries)

def lookCountryCode(country):
    for k in countryDict:
        if country in k:
            return countryDict[k]

with open("metadata.json", encoding='utf-8') as json_file:
    metadata = json.load(json_file)
    for key in metadata:
        with open(os.path.join(folders['xml'],metadata[key]['file'])) as xmlfile:
            try:
                parser = ET.XMLParser(encoding='utf-8')
                tree = ET.parse(xmlfile,parser)
                treaty = tree.getroot()
            except Exception as e:
                pass
            meta = treaty.find('meta')
            metadata[key]['name'] = (meta.find('name').text.replace('Turkey','Türkiye') if "Turkey" in meta.find('name').text else meta.find('name').text)
            metadata[key]['short_name'] = (meta.find('short_name').text.replace('Turkey','Türkiye') if "Turkey" in meta.find('short_name').text else meta.find('short_name').text)
            metadata[key]['type'] = meta.find('type').text
            metadata[key]['status'] = meta.find('status').text
            metadata[key]['notification'] = meta.find('notification').text
            metadata[key]['date-signature'] = meta.find('date_signed').text
            metadata[key]['date-into-force'] = meta.find('date_into_force').text
            metadata[key]['type'] = meta.find('type').text
            metadata[key]['date-notification'] = meta.find('date_notification').text
            metadata[key]['end-implementation'] = meta.find('end_implementation').text
            metadata[key]['date-inactive'] = ("" if meta.find('date_inactive').text is None else meta.find('date_inactive').text)                
            metadata[key]['composition'] = meta.find('composition').text
            metadata[key]['region'] = meta.find('region').text
            metadata[key]['parties-wto'] = meta.find('parties_wto').text
            metadata[key]['crossregional'] = meta.find('crossregional').text
            parties = meta.find('parties').findall('partyisocode')
            for party in parties:
                attribs = party.attrib
                metadata[key]['parties'][codeDict[party.text]] = {
                    "date-accession": attribs['accession'],
                    "date-withdrawal": ("" if attribs['withdrawal']=="NA" else attribs['withdrawal']),
                    "isocode":party.text
                }
            for k, row in data_wto.iterrows():
                if metadata[key]['name'] in row['RTA Name'] and row['Accession?']=='Yes':
                    country = row['RTA Name'].rsplit('Accession of')[-1].strip()
                    country = (country.replace('Republic','').strip() if 'Republic' in country else country)
                    country = (country.replace('the ','').strip() if 'the ' in country else country)
                    country = (country.replace(' the','').strip() if ' the' in country else country)
                    country = (country.rsplit(" and ") if " and " in country else country)
                    if type(country)==list:
                        for c in country:
                            inMetadata = False
                            for party in metadata[key]['parties']: 
                                if c in party: inMetadata = True
                            if not inMetadata:
                                code = lookCountryCode(c)
                                metadata[key]['parties'][codeDict[code]] = {
                                    'date-accession': str(row['Date of Entry into Force (G)'].date()),
                                    'date-withdrawal': "",
                                    'isocode': code
                                }
                    else:
                        inMetadata = False
                        for party in metadata[key]['parties']:
                            if country in party: inMetadata = True
                        if not inMetadata:
                            code = lookCountryCode(country)
                            metadata[key]['parties'][codeDict[code]] = {
                                'date-accession': str(row['Date of Entry into Force (G)'].date()),
                                'date-withdrawal': "",
                                'isocode': code
                            }                        

with open("metadata.json","w",encoding='utf-8') as outf:  json.dump(metadata, outf, ensure_ascii=False)

#with open("metadata.json",encoding="utf-8") as json_file: metadata = json.load(json_file)
