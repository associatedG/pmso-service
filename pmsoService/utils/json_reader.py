import json


def read_file(filename):
    """
    Open a json file
    """
    with open(filename, "r", encoding="utf8") as file:
        data = json.load(file)
    return data
