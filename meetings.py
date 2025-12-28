from util import load_json, save_json

FILE = "data/meetings.json"

def add_monthly_meeting(name, day):
    data = load_json(FILE, [])
    data.append({"name": name, "day": day})
    save_json(FILE, data)
    return "Monthly meeting saved."

def get_meetings():
    return load_json(FILE, [])
