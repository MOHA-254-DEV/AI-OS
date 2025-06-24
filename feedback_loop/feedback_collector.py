# feedback_loop/feedback_collector.py

import json
from pathlib import Path

MEMORY_FILE = Path(__file__).parent / "correction_memory.json"

def load_feedback_memory():
    if not MEMORY_FILE.exists():
        return []
    with open(MEMORY_FILE, 'r') as f:
        return json.load(f)

def save_feedback_memory(data):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def collect_feedback(original_text, corrected_text, feedback_type):
    memory = load_feedback_memory()
    memory.append({
        "type": feedback_type,
        "original": original_text,
        "corrected": corrected_text
    })
    save_feedback_memory(memory)
    return True
