from datetime import datetime
from util import load_json, save_json

FILE = "data/calendar.json"

def add_task(date, time, task):
    data = load_json(FILE, {})
    data.setdefault(date, []).append({"time": time, "task": task})
    save_json(FILE, data)
    return "Task added."

def view_day(date):
    data = load_json(FILE, {})
    return data.get(date, [])
