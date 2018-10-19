#!/usr/bin/env python
import json
import uuid
import requests
from urllib.parse import urljoin


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


    def importValuesToField(self, file, fieldID):
        login = self.GetConnectionAccessKey()
        if login is False:
            return False

        with open(file) as values:
            for line in values:
                # level = node.rstrip().count('\t') + 1
                # term = node.strip()
                # print(term, level)

                # if level > lastLevel:
                #     # The last node processed is this node's parent, 
                #     # add it to the stack
                #     parentNodes.append(latestNode)
                # elif level < lastLevel:
                #     # Pop one or more parent nodes off the stack
                #     # to match the current depth
                #     [parentNodes.pop() for _ in range(lastLevel - level)]

                # Create a new term
                self.addValue(fieldID, term, value, accesskey=login)




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


    def addValue(self, field, term, accesskey=None):
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


