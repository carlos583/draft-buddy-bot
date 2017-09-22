import json

def dump(collection, filename):
    with open(filename, 'w') as file:
        print("Writing collection to", filename)
        json.dump(collection, file)

def load(filename):
    data = {}
    with open(filename, 'rt') as jsonfile:
        data = json.load(jsonfile)

    return data
