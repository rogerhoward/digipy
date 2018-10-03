#!/usr/bin/env python
import json
import uuid
import requests
from urllib.parse import urljoin
import time

class Client(object):
    BASE_URL = None
    USER_NAME = None
    PASSWORD = None

    def __init__(self, url, username, password):
        self.BASE_URL = url
        self.USER_NAME = username
        self.PASSWORD = password

    def importTermFile(self, file, fieldID):
        login = self.GetConnectionAccessKey()
        if login is False:
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
                latestNode = self.createTerm(fieldID, term, parent=parentNodes[-1], accesskey=login)
                lastLevel = level


    def GetConnectionAccessKey(self):
        url = urljoin(self.BASE_URL, 'dmm3bwsv3/ConnectService.js')
        method ='LogOn'

        payload = {'method': method, 'username': self.USER_NAME, 'password': self.PASSWORD}
        r = requests.request("POST", url, data=payload)

        res = r.json()
        if res['success'] == 'true':
            return res['items'][0]['accessKey']
        else:
            return False


    def getAssets(self, accesskey=None):
        url = urljoin(self.BASE_URL, 'dmm3bwsv3/SearchService.js')

        # If caller didn't pass in an access key, try to get one
        if accesskey is None:
            accesskey = self.GetConnectionAccessKey()
            if accesskey is False:
                return False

        # Create requests payload dictionary
        payload = {'SearchName': 'GetAssets', 'accessKey': accesskey}

        # Make POST request, passing accesskey as a query param and other payload as form encoded
        r = requests.request("POST", url, data=payload)
        res = r.json()

        # Return creeated term's ID if successful
        if res['success']:
            return res
        else:
            return False



    def getAssetURL(self, assetid, accesskey=None):

        print('getAssetURL', assetid )
        url = urljoin(self.BASE_URL, 'dmm3bwsv3/SearchService.js')

        # If caller didn't pass in an access key, try to get one
        if accesskey is None:
            accesskey = self.GetConnectionAccessKey()
            if accesskey is False:
                return False


        # Create requests payload dictionary
        payload = {'SearchName': 'GetAssets', 'accessKey': accesskey, 'sAssetId': assetid}

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
                        return self.getAssetURL(assetid, accesskey)
        else:
            return False


    def setKeywords(self, assetid, fieldid, values, accesskey=None):
        url = urljoin(self.BASE_URL, 'apiproxy/BatchUpdateService.js')

        # If caller didn't pass in an access key, try to get one
        if accesskey is None:
            accesskey = self.GetConnectionAccessKey()
            if accesskey is False:
                return False

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
        r = requests.request("POST", url, data=payload, params={'accesskey':accesskey})
        res = r.json()
        print(res)

        # Return creeated term's ID if successful
        if res['success']:
            return True
        else:
            return False


    def setIndexText(self, assetid, fieldid, text, accesskey=None):
        url = urljoin(self.BASE_URL, 'apiproxy/BatchUpdateService.js')

        # If caller didn't pass in an access key, try to get one
        if accesskey is None:
            accesskey = self.GetConnectionAccessKey()
            if accesskey is False:
                return False

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
        r = requests.request("POST", url, data=payload, params={'accesskey':accesskey})
        res = r.json()
        print(res)

        # Return creeated term's ID if successful
        if res['success']:
            return True
        else:
            return False



    def createTerm(self, field, term, parent=[0], accesskey=None):
        url = urljoin(self.BASE_URL, 'apiproxy/BatchUpdateService.js')

        # If caller didn't pass in an access key, try to get one
        if accesskey is None:
            accesskey = self.GetConnectionAccessKey()
            if accesskey is False:
                return False

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
        r = requests.request("POST", url, data=payload, params={'accesskey':accesskey})
        res = r.json()

        # Return creeated term's ID if successful
        if res['success']:
            return res['items'][0]['BaseId']
        else:
            return False

