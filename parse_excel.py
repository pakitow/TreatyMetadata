from imports import *
#The AllRTAs.xlsx, produced by the WTO, consists of 2 worksheets:
# (1) a comprehensive table for each active RTA, with fields being
"""
-> {'RTA ID', 'RTA Name', 'Coverage', 'Type', 'Notification', 'Status',
'Date of Signature (G)', 'Date of Signature (S)', 
'Date of Notification (G)', 'Date of Notification (S)', 
'Date of Entry into Force (G)', 'Date of Entry into Force (S)', 
'Inactive Date', 
'Accession?', 
'RTA Composition', 'Region', 'Cross-regional', 
'All Parties WTO members?', 
'Current signatories', 'Original signatories', 
'Specific Entry/Exit dates', 
'WTO Consideration Process (G)', 'Consideration Date (G)', 
'WTO Consideration Process (S)', 'Consideration Date (S)', 
'End of implementation period (G)', 'End of implementation period (S)', 
'Remarks'}
"""
# (2) a table list for each notification record
"""
-> {'RTA ID', 'RTA Name', 
'Parties concerned', 'Changes affect', 
'Date of notification of changes', 'Date of signature of changes', 'Date of entry into force of changes',
'Remarks'}
"""
#The AgreementsList*.xlsx, produced by UNESCAP, consists of 1 worksheet with fields being
"""
-> {'fileName': (str) xml name,
'text_available': boolean, 
'ptaName': (str) treaty name,
'date_signed': date,
'escap_member': boolean,
'treaty_identifier_TINA': int,
'treaty_identifier_wto': int,
'treaty_identifier_desta': int,
'treaty_identifier_tota': int,
'chapter_id': EMPTY
'article_id': EMPTY
'source_lang': (str) ['en','es','fr']
'comments': str | EMPTY
'ASSIGNED TO...': str | EMPTY
'Status': (str) ['Done','In progress',EMPTY]
}
"""


# initial import
data_wto_treaty = pd.read_excel(io = files['spreadsheet'],sheet_name = 0)
data_escap = pd.read_excel(io = files['dataset'], sheet_name = 0)
data_wto_notification = pd.read_excel(io = files['spreadsheet'], sheet_name = 1)

# conditions for WTO.xlsx interaction
wto = {'not-accession': data_wto_treaty['Accession?']=="No", 'active':data_wto_treaty['Status']!="Inactive"}
escap = {'in-wto': [pd.isna(data_escap['treaty_identifier_wto'].str.contains("NA")),
pd.isna(data_escap['treaty_identifier_wto'])==False]}

# adjust for WTO interaction
data_wto_treaty = data_wto_treaty[wto['active']]#[wto['not-accession'] & wto['active']]
data_escap = data_escap[escap['in-wto'][0] & escap['in-wto'][1]]

# store all WTO treaties present in ESCAP
escap_in_wto = data_escap['treaty_identifier_wto'].values.tolist()
wto_in_escap = data_wto_treaty['RTA ID'].values.tolist()

x = data_wto_treaty['RTA ID'].isin(escap_in_wto)==False
y = data_escap['treaty_identifier_wto'].isin(wto_in_escap)==False
print(data_escap[y]['treaty_identifier_wto'])


#print(len(data_wto_treaty['RTA ID']))
