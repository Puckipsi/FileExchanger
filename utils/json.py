import json


def write_json_to_file(filename, data):
    with open(f"application/replicated/{filename}.json", "w") as f:
        json.dump(data, f, indent=4)