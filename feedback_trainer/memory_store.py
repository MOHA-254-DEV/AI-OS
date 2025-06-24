# feedback_trainer/memory_store.py
import json
from datetime import datetime

correction_file = "feedback_trainer/corrections.json"

def save_correction(task_id, original, corrected, context=None):
    record = {
        "id": task_id,
        "original_output": original,
        "corrected_output": corrected,
        "context": context,
        "timestamp": datetime.utcnow().isoformat()
    }

    try:
        with open(correction_file, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(record)
    with open(correction_file, "w") as f:
        json.dump(data, f, indent=2)

    return {"status": "saved"}

def load_corrections():
    try:
        with open(correction_file, "r") as f:
            return json.load(f)
    except:
        return []
