import json
import os

FILE = "data/trust.json"

DEFAULT = {
    "fun_when_tired": "ask"  # ask | auto
}


def load_trust():
    if not os.path.exists(FILE):
        return DEFAULT.copy()
    with open(FILE, "r") as f:
        return json.load(f)


def save_trust(data):
    os.makedirs("data", exist_ok=True)
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)


def set_fun_when_tired(mode: str):
    data = load_trust()
    data["fun_when_tired"] = mode
    save_trust(data)


def get_fun_when_tired():
    return load_trust().get("fun_when_tired", "ask")
