import csv
import collections

def read(filename):
    rows = []
    with open(filename, 'rt') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
    return rows