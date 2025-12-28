from datetime import datetime
import random

from period_tracker import start_period, get_phase
from scheduler import add_task, view_day
from meetings import add_monthly_meeting, get_meetings
from journal import write_entry, view_entries
from games import guess_number, rock_paper_scissors

from agent_state import (
    set_pending_intent,
    clear_pending_intent,
    set_energy,
    get_state
)
from agent_actions import (
    plan_high_energy_day,
    plan_medium_energy_day,
    plan_tired_day
)

from agent_brain import reason
from pattern_logger import log_event
from trust_state import get_fun_when_tired, set_fun_when_tired


print("🌸 SIA Agent is active 🌸")
print("Talk naturally. Type 'help' for examples, 'exit' to quit.\n")


# ================= EXPLAINABILITY =================
last_reason = None


# ================= HELP =================
def show_help():
    print("""
You can talk naturally. Examples:

🗓️ Planning
- plan my day
- what should I do today

🌸 Period & Cycle
- start my period
- what phase am I in

📅 Meetings
- add a monthly meeting
- show my meetings

📝 Journal
- write a journal entry
- show my journal

🎮 Fun
- play a game

⚙️ Control
- change preferences
- why did you do that
""")


# ================= IDLE DETECTION =================
def is_idle_input(text: str) -> bool:
    idle_phrases = [
        "what you doing", "what are you doing",
        "idk", "nothing", "hmm", "ok", "okay", "..."
    ]
    return len(text.strip()) <= 3 or text in idle_phrases


def idle_response():
    return (
        "I’m here 😊\n"
        "We can chill, play a quick game, hear something funny, "
        "or I can help with your day.\n"
        "What feels right?"
    )


# ================= TIRED DETECTION =================
def is_tired_input(text: str) -> bool:
    tired_keywords = [
        "tired", "exhausted", "sleepy", "done",
        "ugh", "not today", "cant", "can't", "burnt", "burned"
    ]
    return any(word in text for word in tired_keywords)


def tired_fun_response():
    options = [
        "Okay, productivity is cancelled 🌸 Want a game or a joke?",
        "Low-energy moment detected 😌 Game or joke?",
        "Let’s not be productive right now 💤 Want something fun?"
    ]
    return random.choice(options)


# ================= MAIN LOOP =================
while True:
    user_input = input("You: ").strip().lower()

    if user_input in ["exit", "quit"]:
        print("Goodbye 🌸")
        break

    if user_input == "help":
        show_help()
        continue

    # =========== WHY DID YOU DO THAT ==========
    if "why" in user_input or "explain" in user_input:
        if last_reason:
            print(last_reason)
        else:
            print("Nothing specific yet — I was just listening 😊")
        continue

    # ========== CHANGE PREFERENCES ==========
    if "change preferences" in user_input or "preferences" in user_input:
        current = get_fun_when_tired()
        print(f"Fun-mode when tired is currently set to: {current}")
        print("1. Always ask first")
        print("2. Automatically switch to fun mode")

        choice = input("Choose (1/2): ").strip()
        if choice == "1":
            set_fun_when_tired("ask")
            print("Got it 🌸 I’ll ask before switching.")
        elif choice == "2":
            set_fun_when_tired("auto")
            print("Okay 🌸 I’ll handle low-energy moments automatically.")
        else:
            print("No changes made.")
        continue

    # ==========IDLE ==========
    if is_idle_input(user_input):
        log_event("idle_detected")
        print(idle_response())
        continue

    # ==========TIRED + TRUST =========
    if is_tired_input(user_input):
        log_event("tired_detected")
        mode = get_fun_when_tired()

        if mode == "auto":
            last_reason = (
                "You sounded tired, and earlier you allowed me to "
                "switch to fun mode automatically during low-energy moments."
            )
            print("I might be wrong, but it sounds like a low-energy moment 😌")
            print(tired_fun_response())
        else:
            print(
                "I might be wrong, but you sound tired 😌\n"
                "When this happens, people usually prefer something light.\n"
                "Want me to automatically switch to fun mode next time? (y/n)"
            )
            reply = input("You: ").strip().lower()
            if reply == "y":
                set_fun_when_tired("auto")
                print("Got it 🌸 I’ll handle low-energy moments gently from now on.")
        continue

    # ========== AGENT STATE CHECK ==========
    state = get_state()

    if state.get("pending_intent") == "PLAN_DAY":
        energy = user_input
        if energy in ["high", "medium", "tired"]:
            set_energy(energy)
            log_event("energy_set", {"energy": energy})
            clear_pending_intent()

            if energy == "high":
                last_reason = "You said your energy was high, so I planned a more intensive day."
                print(plan_high_energy_day())
            elif energy == "medium":
                last_reason = "You said your energy was medium, so I planned a balanced day."
                print(plan_medium_energy_day())
            else:
                last_reason = "You said your energy was low, so I planned a gentle day."
                print(plan_tired_day())
        else:
            print("Just say: high, medium, or tired 🌸")
        continue

    # ========== LLM REASONING ==========
    decision = reason(user_input)
    tool = decision.get("tool")
    args = decision.get("args", {})

    # ========== TOOLS ==========
    if tool == "plan_day":
        set_pending_intent("PLAN_DAY")
        print("How’s your energy right now? (high / medium / tired)")
        continue

    if tool == "start_period":
        date = args.get("date") or input("Start date (YYYY-MM-DD): ")
        print(start_period(date))
        continue

    if tool == "check_cycle":
        print(get_phase())
        continue

    if tool == "add_task":
        date = args.get("date") or input("Date (YYYY-MM-DD): ")
        time = args.get("time") or input("Time (HH:MM): ")
        task = args.get("task") or input("Task: ")
        print(add_task(date, time, task))
        continue

    if tool == "view_today":
        today = datetime.now().strftime("%Y-%m-%d")
        tasks = view_day(today)
        if not tasks:
            print("No tasks planned for today.")
        else:
            for t in tasks:
                print(f"- {t['time']} → {t['task']}")
        continue

    if tool == "add_meeting":
        name = args.get("name") or input("Meeting name: ")
        day = args.get("day") or input("Day of month: ")
        print(add_monthly_meeting(name, day))
        continue

    if tool == "view_meetings":
        meetings = get_meetings()
        if not meetings:
            print("No monthly meetings saved.")
        else:
            for m in meetings:
                print(f"- {m['name']} on day {m['day']}")
        continue

    if tool == "write_journal":
        text = args.get("text") or input("What would you like to write? ")
        mood = input("Mood (optional): ") or None
        print(write_entry(text, mood))
        continue

    if tool == "view_journal":
        entries = view_entries()
        if not entries:
            print("Journal is empty.")
        else:
            for e in entries:
                print(f"{e['date']} {e['time']} | {e.get('mood')} | {e['text']}")
        continue

    if tool == "play_game":
        choice = input("1 = Guess Number, 2 = Rock Paper Scissors: ")
        print(guess_number() if choice == "1" else rock_paper_scissors())
        continue

    # ========== HUMAN FALLBACK ==========
    print(
        "I’m here 😊\n"
        "I can help plan your day, manage tasks, journal, or just hang out.\n"
        "What do you feel like doing?"
    )
