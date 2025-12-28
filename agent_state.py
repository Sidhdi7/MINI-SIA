from util import load_json, save_json

FILE = "data/agent_state.json"

def get_state():
    return load_json(FILE, {
        "pending_intent": None,
        "energy": None
    })

def set_pending_intent(intent):
    state = get_state()
    state["pending_intent"] = intent
    save_json(FILE, state)

def clear_pending_intent():
    state = get_state()
    state["pending_intent"] = None
    save_json(FILE, state)

def set_energy(level):
    state = get_state()
    state["energy"] = level
    save_json(FILE, state)
