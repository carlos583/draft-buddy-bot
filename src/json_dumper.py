import json

def dump(collection, filename):
    with open(filename, 'w') as file:
        json.dump(collection, file)
