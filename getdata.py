import csv


class Video:
    def __init__(self, values):
        vars(self).update(values)


def _read_data():
    arr = []
    with open('data.csv', newline='') as csvfile:
        datareader = csv.DictReader(csvfile, delimiter='\t')
        for row in datareader:
            arr.append(Video(row))
    return arr