from datetime import datetime, timedelta
from util import load_json, save_json

FILE = "data/period.json"

def start_period(date_str):
    data = {
        "last_period_start": date_str,
        "cycle_length": 28
    }
    save_json(FILE, data)
    return "Period start date saved."

def get_phase():
    data = load_json(FILE, {})
    if not data:
        return "No period data found."

    start = datetime.strptime(data["last_period_start"], "%Y-%m-%d")
    today = datetime.today()
    day = (today - start).days % data["cycle_length"]

    if day <= 5:
        return "Menstrual phase 🩸 — take it easy."
    elif day <= 13:
        return "Follicular phase 🌱 — good for focus."
    elif day <= 16:
        return "Ovulation phase ✨ — high energy."
    else:
        return "Luteal phase 🌙 — slow down a bit."
