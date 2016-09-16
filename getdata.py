import json


class Video:
    def __init__(self, values):
        vars(self).update(values)


def _read_data():
    f = open('database.json', 'r', encoding='utf-8')
    database = json.load(f)
    arr = []
    for i in database:
        arr.append(Video(database[i]))
    return arr

print(_read_data()[0].URL)