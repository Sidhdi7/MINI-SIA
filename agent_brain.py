import json
from llm_client import ask_llm

SYSTEM_PROMPT = """
You are the reasoning brain of a personal AI assistant.

Choose EXACTLY one tool from the list.

Available tools:
- plan_day
- start_period
- check_cycle
- add_task
- view_today
- add_meeting
- view_meetings
- write_journal
- view_journal
- play_game
- unknown

Examples:
User: show my meetings
Output:
{"tool": "view_meetings", "args": {}}

User: view journal
Output:
{"tool": "view_journal", "args": {}}

Return ONLY valid JSON.
"""

def reason(user_input):
    raw = ask_llm(SYSTEM_PROMPT, user_input)

    try:
        decision = json.loads(raw)
        return decision
    except Exception:
        return {"tool": "unknown", "args": {}}
