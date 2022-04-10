import csv


def read_csv(path):
    with open(path, mode='r') as file:
        reader = csv.DictReader(file)
        return list(dict)
