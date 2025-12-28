import json
import os

def load_json(path, default):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    if not os.path.exists(path):
        return default

    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as f:
        json.dump(data, f, indent=2)
