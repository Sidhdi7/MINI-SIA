from period_tracker import get_phase
from journal import view_entries
from agent_state import get_state

def build_context():
    phase = get_phase()
    journal = view_entries()[-1:]  # last entry
    state = get_state()

    return {
        "cycle_phase": phase,
        "recent_journal": journal,
        "agent_state": state
    }
