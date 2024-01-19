#!/usr/bin/python
#
# mist_client.py
#
# Mist API client session.

import json, requests

# Mist CRUD operations
class MistSession(object):
    def __init__(self, token=''):
        self.session = requests.Session()
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + token
        }

    def get(self, url):
        session = self.session
        headers = self.headers

        print('GET {}'.format(url))
        response = session.get(url, headers=headers)

        if response.status_code != 200:
            print('Failed to GET')
            print('\tURL: {}'.format(url))
            print('\tResponse: {} ({})'.format(response.text, response.status_code))

            return False

        return json.loads(response.text)

    def post(self, url, payload, timeout=60):
        session = self.session
        headers = self.headers

        print('POST {}'.format(url))

        if 'file' in payload:
            del headers['Content-Type']

            filename = payload['file']
            jsondata = payload.get('json', '')

            files = {
                'json': (None, json.dumps(jsondata), 'application/json'),
                'file': open(filename, 'rb')
            }

            response = session.post(url, headers=headers, files=files, verify=False, timeout=timeout)
        else:
            response = session.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            print('Failed to POST')
            print('\tURL: {}'.format(url))
            print('\tPayload: {}'.format(payload))
            print('\tResponse: {} ({})'.format(response.text, response.status_code))

            return False

        return json.loads(response.text)

    def put(self, url, payload):
        session = self.session
        headers = self.headers

        print('PUT {}'.format(url))
        response = session.put(url, headers=headers, json=payload)

        if response.status_code != 200:
            print('Failed to PUT')
            print('\tURL: {}'.format(url))
            print('\tPayload: {}'.format(payload))
            print('\tResponse: {} ({})'.format(response.text, response.status_code))

            return False

        return json.loads(response.text)
