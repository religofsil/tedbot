"""
Utility classes and functions
"""

import json
import requests
import time
import config
import random
import os

DIR = os.path.dirname(os.path.realpath(__file__))


class Video:
    """
    Store data for one ted talk from database.
    """
    def __init__(self, values):
        vars(self).update(values)


def read_data():
    """
    Create an array of Video instances: one instance for each ted talk.
    Returns:
        list of Video instances
    """
    with open(DIR + config.DATA, 'r', encoding='utf-8') as f:
        database = json.load(f)
    arr = []
    for i in database:
        arr.append(Video(database[i]))
    return arr


def get_key_words(text):
    """
    Get key phrases from text using Cognitive Services API.
    Args:
        text: string with a text in English
    Returns:
        a list of key phrases or None
    """
    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = config.KEYWORDS_KEY
    headers['Content-Type'] = 'application/json'
    params = None
    json_data = {
        "documents": [
            {
                "language": "en",
                "id": 'string',
                "text": text
            }
        ]
    }
    data = None
    time.sleep(random.choice([1, 2, 3, 4, 5, 6, 8, 10, 17, 15, 20]))

    result = process_request('post', config.KEYWORDS_URL, json_data, data, headers, params)
    if result and 'documents' in result:
        return result['documents'][0]["keyPhrases"]
    return None


def process_request(method, url, json, data, headers, params):
    """
    Helper function to process the request
    """
    result = None
    response = requests.request(method, url, json=json, data=data, headers=headers, params=params)

    if response.status_code == 200:

        if 'content-length' in response.headers and int(response.headers['content-length']) == 0:
            result = None
        elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str):
            if 'application/json' in response.headers['content-type'].lower():
                result = response.json() if response.content else None

    else:
        print("Error code: %d" % (response.status_code))
        print(response.json())

    return result
