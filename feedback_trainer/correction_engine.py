# feedback_trainer/correction_engine.py
from memory_store import save_correction, load_corrections
from difflib import SequenceMatcher

def find_applicable_correction(task_id: str, output: str):
    corrections = load_corrections()
    best_match = None
    best_score = 0

    for record in corrections:
        similarity = SequenceMatcher(None, output, record['original_output']).ratio()
        if similarity > best_score:
            best_score = similarity
            best_match = record

    if best_score > 0.7:
        return {
            "match_score": best_score,
            "suggested_output": best_match["corrected_output"],
            "original_output": best_match["original_output"]
        }
    return {"match_score": best_score, "suggested_output": output}

def register_correction(task_id, original, corrected, context=None):
    return save_correction(task_id, original, corrected, context)
