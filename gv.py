
import os
import requests
import simplejson as json
import base64
from io import BytesIO

DEBUG = True

class GoogleVision(object):

    PAYLOAD_PROTO = {
      "requests": [
        {
          "image": {
              "source": {"imageUri": None }
            },
          "features": [

            {
              "type": "LABEL_DETECTION",
              "maxResults": 50
            },
          ]
        }
      ]
    }


    def __init__(self, key, url):
        if DEBUG:
            print('new GV client')
        self.key = key
        self.url = url


    def keywords(self):
        if DEBUG:
            print('new keywords request')

        url = 'https://vision.googleapis.com/v1/images:annotate?key={}'.format(self.key)
        payload = self.PAYLOAD_PROTO
        payload['requests'][0]['image']['source']['imageUri'] = self.url


        if DEBUG:
            print('payload', payload)
            print('url', url)

        r = requests.post(url, json=payload)
        result_data = r.json()
        if DEBUG:
            print('result_data', result_data)
        these_labels = result_data['responses'][0]['labelAnnotations']

        keywords = [x['description'] for x in these_labels]
        if DEBUG:
            print('keywords', keywords)
        return keywords


# if __name__ == '__main__':
#     apikey = os.environ.get('GOOGLE_VISION_API_KEY', None)
#     if not apikey:
#         return False

#     c = GoogleVision(apikey, 'http://acme.dzrho.com/dmm3bwsv3/2173_2_11_4_11_0_4a078007-f0c3-402e-8991-011c92a6ed84_False.jpg?mptdid=42813')
#     kw = c.keywords()
#     print(kw)