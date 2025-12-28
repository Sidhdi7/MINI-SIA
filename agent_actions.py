from datetime import datetime
from scheduler import add_task, view_day
from agent_state import set_energy, clear_pending_intent

def suggest_light_day():
    today = datetime.now().strftime("%Y-%m-%d")
    add_task(today, "10:00", "Light study / revision")
    add_task(today, "18:00", "Rest & self-care")
    return "I planned a lighter day for you 💗"

def suggest_full_day():
    today = datetime.now().strftime("%Y-%m-%d")
    add_task(today, "10:00", "Focused work session")
    add_task(today, "14:00", "Meeting / study")
    add_task(today, "18:00", "Wrap-up + reflection")
    return "I planned a productive day ✨"


def plan_high_energy_day():
    today = datetime.now().strftime("%Y-%m-%d")

    add_task(today, "09:00", "Deep focus work")
    add_task(today, "12:00", "Meeting / collaboration")
    add_task(today, "15:00", "Skill building / coding")
    add_task(today, "18:00", "Workout / active break")

    return format_plan("High-energy", today)

def plan_medium_energy_day():
    today = datetime.now().strftime("%Y-%m-%d")

    add_task(today, "10:00", "Moderate work session")
    add_task(today, "14:00", "Study / reading")
    add_task(today, "18:00", "Light exercise or walk")

    return format_plan("Medium-energy", today)

def plan_tired_day():
    today = datetime.now().strftime("%Y-%m-%d")

    add_task(today, "11:00", "Light tasks / admin")
    add_task(today, "16:00", "Fun activity / hobby")
    add_task(today, "20:00", "Rest & self-care")

    return format_plan("Easy & fun", today)

def format_plan(label, date):
    tasks = view_day(date)
    response = f"I planned a **{label} day** for you 🌸\nHere’s your plan:\n"
    for t in tasks:
        response += f"- {t['time']} → {t['task']}\n"
    return response

