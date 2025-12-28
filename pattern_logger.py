import json
import os
from datetime import datetime

FILE = "data/patterns.json"


def _load():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)


def _save(data):
    os.makedirs("data", exist_ok=True)
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)


def log_event(event_type: str, meta: dict | None = None):
    data = _load()

    entry = {
        "timestamp": datetime.now().isoformat(),
        "event": event_type,
        "meta": meta or {}
    }

    data.append(entry)
    _save(data)
