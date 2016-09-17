import json
import requests
import time

import os

DIR = os.path.dirname(os.path.realpath(__file__))

_maxNumRetries = 10

class Video:
    def __init__(self, values):
        vars(self).update(values)


def _read_data():
    f = open(DIR + '/database.json', 'r', encoding='utf-8')
    database = json.load(f)
    arr = []
    for i in database:
        arr.append(Video(database[i]))
    return arr

def processRequest(method, url, json, data, headers, params):
    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:

        if method == 'patch':
            response = requests.patch(url, files=data, headers=headers)
        else:
            response = requests.request(method, url, json=json, data=data, headers=headers, params=params)

        if response.status_code == 429:

            print(response.json())

            if retries <= _maxNumRetries:
                time.sleep(1)
                retries += 1
                continue
            else:
                print('Error: failed after retrying!')
                break

        elif response.status_code == 200 or response.status_code == 201:

            if 'content-length' in response.headers and int(response.headers['content-length']) == 0:
                result = None
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str):
                if 'application/json' in response.headers['content-type'].lower():
                    result = response.json() if response.content else None
                elif 'image' in response.headers['content-type'].lower():
                    result = response.content

        elif response.status_code == 202:

            _getVideoData = response.headers['Operation-Location']
            if 'content-length' in response.headers and int(response.headers['content-length']) == 0:
                result = None
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str):
                if 'application/json' in response.headers['content-type'].lower():
                    result = response.json() if response.content else None
                elif 'image' in response.headers['content-type'].lower():
                    result = response.content
            print(_getVideoData)
            print(response.headers)
            print(response)

        else:
            print("Error code: %d" % (response.status_code))
            print(response.json())

        break

    return result

# print(_read_data()[0].URL)