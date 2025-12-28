from datetime import datetime
from util import load_json, save_json

FILE = "data/journal.json"

def write_entry(text, mood=None):
    entries = load_json(FILE, [])
    entries.append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M"),
        "text": text,
        "mood": mood
    })
    save_json(FILE, entries)
    return "Journal entry saved."

def view_entries():
    return load_json(FILE, [])
