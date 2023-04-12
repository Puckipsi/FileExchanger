import json


def write_json_to_file(replica_folder, filename, data):
    with open(f"{replica_folder}/{filename}.json", "w") as f:
        json.dump(data, f, indent=4)


def read_json_file(replica_folder, filename):
    with open(f"{replica_folder}/{filename}.json", "r") as f:
        data = json.load(f)
    return data