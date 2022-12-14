from imports import json, os, ET, folders
with open("metadata.json", encoding='utf-8') as json_file:
    metadata = json.load(json_file)
for key in metadata:
    pathFull = os.path.join(folders['xml'],metadata[key]['file'])
    with open(pathFull) as xmlfile:
        try:
            needsChange = 0
            parser = ET.XMLParser(encoding="utf-8")
            tree = ET.parse(xmlfile,parser)
            metaXML = tree.getroot().find('meta')
            metaJSON = metadata[key]
            # check name in XML
            name_XML = metaXML.find('name').text    
            shortname_XML = metaXML.find('short_name').text        
            if metaJSON['name'] != name_XML:
                needsChange+=1
                print(key,'difference on name')
                name_XML = metaJSON['name']
            if metaJSON['short_name'] != shortname_XML:
                needsChange+=1
                print(key,'difference on short name')
                shortname_XML = metaJSON['short_name']
            # check type in XML
            type_XML = metaXML.find('type').text
            if metaJSON['type'] != type_XML:
                needsChange+=1
                print(key,'difference on type')
                typeXML = metaJSON['type']
            # check status
            status_XML = metaXML.find('status').text
            if metaJSON['status'] != status_XML:
                needsChange+=1
                print(key, 'difference on status')
                status_XML = metaJSON['status']
            # check notification
            notification_XML = metaXML.find('notification').text
            if metaJSON['notification'] != notification_XML:
                needsChange+=1
                print(key, 'difference on notifcation status')
                notification_XML = metaJSON['notification']
            # check date of signature
            signature_XML = metaXML.find('date_signed').text
            if metaJSON['date-signature'] != signature_XML:
                needsChange+=1
                print(key, 'difference on date signed')
                signature_XML = metaJSON['date-signature']            
            # check date of entry into force
            entry_force = metaXML.find('date_into_force').text
            if metaJSON['date-into-force'] != entry_force:
                needsChange+=1
                print(key, 'difference on date of entry into force')
                entry_force = metaJSON['date-into-force']            
            # check date of notification
            date_notification = metaXML.find('date_notification').text
            if metaJSON['date-notification'] != date_notification:
                needsChange+=1
                print(key, 'difference on date of notifcation')
                date_notification = metaJSON['date-notification']                        
            # check end of implementation
            end_implementation = metaXML.find('end_implementation').text
            if metaJSON['end-implementation'] != end_implementation:
                needsChange+=1
                print(key, 'difference on implementation end date')
                end_implementation = metaJSON['notification']                        
            # check date inactive
            date_inactive = metaXML.find('date_inactive').text
            if metaJSON['date-inactive'] != date_inactive and date_inactive!=None:
                needsChange+=1
                print(key, 'difference on inactivity date')
                date_inactive = metaJSON['date-inactive']                        
            # check composition
            composition = metaXML.find('composition').text
            if metaJSON['composition'] != composition:
                needsChange+=1
                print(key, 'difference on composition')
                composition = metaJSON['composition']                        
            # check region
            region = metaXML.find('region').text
            if metaJSON['region'] != region:
                needsChange+=1
                print(key, 'difference on regional distribution')
                notification_XML = metaJSON['notification']                        
            # check parties wto
            parties_wto = metaXML.find('parties_wto').text
            if metaJSON['parties-wto'] != parties_wto:
                needsChange+=1
                print(key, 'difference on wto membership status')
                parties_wto = metaJSON['parties-wto']                                    
            # check crossregional
            crossregional = metaXML.find('crossregional').text
            if metaJSON['crossregional'] != crossregional:
                needsChange+=1
                print(key, 'difference on notifcation status')
                crossregional = metaJSON['crossregional']  
            # check for new members
            for party in metadata[key]['parties']:
                notFound = False
                for country in metaXML.find('parties').findall('partyisocode'):
                    if metadata[key]['parties'][party]['isocode'] in country.text: notFound = True
                if notFound==False:
                    needsChange+=1
                    countryList = metaXML.find('parties').findall('partyisocode')
                    newMember = ET.SubElement(metaXML.find('parties'),'partyisocode',n=countryList[-1].attrib['n']+1,accession=party['date-accession'],withdrawal=("NA" if party['date-withdrawal']=="" else party['date-withdrawal']))
                    newMember.text = party['isocode']
            if needsChange > 0:
                os.remove(pathFull)
                print(pathFull)
                tree.write(pathFull,encoding='utf-8')
        except Exception as e: print(e)




