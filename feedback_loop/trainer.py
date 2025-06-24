# feedback_loop/trainer.py

from feedback_collector import load_feedback_memory
import difflib

def learn_from_feedback():
    corrections = load_feedback_memory()
    patterns = []

    for item in corrections:
        diff = list(difflib.unified_diff(
            item["original"].splitlines(),
            item["corrected"].splitlines(),
            lineterm=""
        ))
        patterns.append({
            "type": item["type"],
            "diff": diff
        })

    return patterns

def print_diff_summary():
    patterns = learn_from_feedback()
    for p in patterns:
        print(f"\nFeedback Type: {p['type']}")
        print("\n".join(p["diff"]))
