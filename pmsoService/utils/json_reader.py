import json


def read_file(filename):
    """
    Open a json file
    """
    with open(filename, "r") as file:
        data = json.load(file)
    return data
