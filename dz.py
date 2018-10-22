#!/usr/bin/env python
import json
import uuid
import requests
from urllib.parse import urljoin
import csv
from cached_property import cached_property
import time


class Client(object):
    BASE_URL = None
    USER_NAME = None
    PASSWORD = None

    def __init__(self, url, username, password):
        self.BASE_URL = url
        self.USER_NAME = username
        self.PASSWORD = password
        if not self.login:
            print('Login not successful. Check your credentials.')

    @cached_property
    def login(self):
        url = urljoin(self.BASE_URL, 'dmm3bwsv3/ConnectService.js')
        method ='LogOn'

        payload = {'method': method, 'username': self.USER_NAME, 'password': self.PASSWORD}
        r = requests.request("POST", url, data=payload)

        res = r.json()
        if res['success'] == 'true':
            return res['items'][0]['accessKey']
        else:
            return False


    def importTreeValues(self, file, fieldID):
        if not self.login:
            return False

        with open(file) as tree:
            parentNodes = [0, ]
            latestNode = 0
            lastLevel = 1

            for node in tree:
                level = node.rstrip().count('\t') + 1
                term = node.strip()
                print(term, level)

                if level > lastLevel:
                    # The last node processed is this node's parent, 
                    # add it to the stack
                    parentNodes.append(latestNode)
                elif level < lastLevel:
                    # Pop one or more parent nodes off the stack
                    # to match the current depth
                    [parentNodes.pop() for _ in range(lastLevel - level)]

                # Create a new term
                latestNode = self.addTreeValue(fieldID, term, parent=parentNodes[-1])
                lastLevel = level


    def importFlatValues(self, file, fieldID):
        with open(file) as csvfile:
            tab_reader = csv.DictReader(csvfile, delimiter='\t')
            rownum = 1
            for row in tab_reader:
                print(row['Label'], row['Value'])
                self.addFlatValue(fieldID, label=row['Label'], value=row['Value'], sort=rownum)
                rownum += 1


    def addFlatValue(self, field, label, sort=0, value=None):
        if not self.login:
            return False

        url = urljoin(self.BASE_URL, 'apiproxy/BatchUpdateService.js')

        payload_values = [{    "Id": "MetaDataUpdate0",    "FieldId": "MetaDataUpdate0",    "ContainerType": 1,    "RowId": 1,    "Values": [{"FieldId": "ispublic","Type": 2,"Values": [True]},{"FieldId": "visible","Type": 2,"Values": [True]}], "BaseId": 0 }]
        
        payload_values[0]['Values'].append( {"FieldId": 'item_metafield_labelid', "Type": 3, "Values": [field]} ) # Set Field ID
        payload_values[0]['Values'].append( {"FieldId": 'combovalue', "Type": 1, "Values": [label]} ) # Set value
        payload_values[0]['Values'].append( {"FieldId": 'optionvalue', "Type": 1, "Values": [value]} ) # Set Field ID
        payload_values[0]['Values'].append( {"FieldId": 'sortindex', "Type": 3, "Values": [sort]} ) # Set Sort order


        payload_xml = '<r><metacombo_definition fieldId="MetaDataUpdate0"><item_metafield_labelid fieldId="item_metafield_labelid"/><combovalue fieldId="combovalue"/><optionvalue fieldId="optionvalue"/><sortindex fieldId="sortindex"/><ispublic fieldId="ispublic"/><visible fieldId="visible"/></metacombo_definition></r>'

        # Create requests payload dictionary
        payload = {'updateXML': payload_xml, 'values': json.dumps(payload_values)}

        # Make POST request, passing accesskey as a query param and other payload as form encoded
        while True:
            try:
                r = requests.request("POST", url, data=payload, params={'accesskey': self.login}, timeout=10)
                break
            except requests.exceptions.Timeout as err:
                continue

        res = r.json()
        # print(res)

        # Return creeated term's ID if successful
        if res['success']:
            print('Successfully added term {} ({}) to field {}'.format(label, value, field))
            return res['items'][0]['BaseId']
        else:
            return False


    def addTreeValue(self, field, term, parent=[0]):
        if not self.login:
            return False

        url = urljoin(self.BASE_URL, 'apiproxy/BatchUpdateService.js')

        # Read in basic structure of "values" payload
        with open('templates/values.json') as json_file:
            payload_values = json.load(json_file)

        # Insert custom values into "values" payload
        payload_values[0]['Values'].append({"FieldId": "item_metafield_labelid", "Type": 3, "Values": field})
        payload_values[0]['Values'].append({"FieldId": "prevref", "Type": 3, "Values": parent})
        payload_values[0]['Values'].append({"FieldId": "treevalue", "Type": 1, "Values": [term]})
        payload_values[0]['Values'].append({"FieldId": "optionvalue", "Type": 1, "Values": [str(uuid.uuid4())]})

        # Read in XML contents for "updateXML" payload
        with open("templates/update.xml") as xml_file:
            payload_xml = xml_file.read()

        # Create requests payload dictionary
        payload = {'updateXML': payload_xml, 'values': json.dumps(payload_values)}

        # Make POST request, passing accesskey as a query param and other payload as form encoded
        while True:
            try:
                r = requests.request("POST", url, data=payload, params={'accesskey': self.login}, timeout=10)
                break
            except requests.exceptions.Timeout as err:
                continue
       
        res = r.json()

        # Return creeated term's ID if successful
        if res['success']:
            return res['items'][0]['BaseId']
        else:
            return False


class Asset(object):
    def __init__(self, client, assetid):
        self.client = client
        self.assetid = assetid


    def getAssetURL(self, assetid):
        if not self.client.login:
            return False

        print('getAssetURL', assetid )
        url = urljoin(self.BASE_URL, 'dmm3bwsv3/SearchService.js')

        # Create requests payload dictionary
        payload = {'SearchName': 'GetAssets', 'accessKey': self.client.login, 'sAssetId': assetid}

        # Make POST request, passing accesskey as a query param and other payload as form encoded
        r = requests.request("GET", url, params=payload)
        res = r.json()

        # Return creeated term's ID if successful
        if res['success']:
            for item in res['items']:                    
                # print('-------')
                # print(assetid)
                # print(item['displayitemId'])
                # print('-------')
                if item['assetId'] == str(assetid):
                    if len(item['imagePreview']) > 0:
                        print(item)
                        return item['displayitemId'], item['imagePreview']
                    else:
                        print('no imagePreview yet')
                        time.sleep(2)
                        return self.getAssetURL(assetid)
        else:
            return False


    def setKeywords(self, assetid, fieldid, values):
        if not self.client.login:
            return False

        url = urljoin(self.BASE_URL, 'apiproxy/BatchUpdateService.js')

        # Read in basic structure of "values" payload

        payload_values = [{    "Id": "Container1",    "FieldId": "Container1",    "ContainerType": 7,    "RowId": 1,    "Values": [],    "ItemIds": []}]
        payload_values[0]['Values'] = [{"FieldId": 'Container1Field1'.format(fieldid), "Type": 17, "Values": values}]
        payload_values[0]['ItemIds'] = [str(assetid)]

        print("---------------")
        print(payload_values)
        print("---------------")

        # Read in XML contents for "updateXML" payload
        # with open("templates/keywords.xml") as xml_file:  
        #     payload_xml = xml_file.read()

        payload_xml = '<r>    <asset fieldId="Container1">        <metafield fieldId="Container1Field1" labelId="10438"/>    </asset></r>'

        payload_xml = payload_xml.replace('FIELDID', fieldid)
        print(payload_xml)        
        print("---------------")

        # Create requests payload dictionary
        payload = {'updateXML': payload_xml, 'values': json.dumps(payload_values)}


        # Make POST request, passing accesskey as a query param and other payload as form encoded

        while True:
            try:
                r = requests.request("POST", url, data=payload, params={'accesskey': self.client.login}, timeout=10)
                break
            except requests.exceptions.Timeout as err:
                continue
        
        res = r.json()
        print(res)

        # Return creeated term's ID if successful
        if res['success']:
            return True
        else:
            return False


    def setIndexText(self, assetid, fieldid, text):
        if not self.client.login:
            return False

        url = urljoin(self.BASE_URL, 'apiproxy/BatchUpdateService.js')

        # Read in basic structure of "values" payload

        payload_values = [{"Id":"Container1","FieldId":"Container1","FieldName":"asset","ContainerType":7,"ItemIds":[assetid],"RowId":1,"Values":[{"FieldId":"Container1Field1","Type":1,"Values":[text]}]}]

        print("---------------")
        print(payload_values)
        print("---------------")

        # Read in XML contents for "updateXML" payload
        # with open("templates/keywords.xml") as xml_file:  
        #     payload_xml = xml_file.read()

        payload_xml = '<r><asset fieldId="Container1"><metafield fieldId="Container1Field1" labelId="51619"/></asset></r>'

        print(payload_xml)        
        print("---------------")

        # Create requests payload dictionary
        payload = {'updateXML': payload_xml, 'values': json.dumps(payload_values)}


        # Make POST request, passing accesskey as a query param and other payload as form encoded
        while True:
            try:
                r = requests.request("POST", url, data=payload, params={'accesskey': self.client.login}, timeout=10)
                break
            except requests.exceptions.Timeout as err:
                continue

        res = r.json()
        print(res)

        # Return creeated term's ID if successful
        if res['success']:
            return True
        else:
            return False

