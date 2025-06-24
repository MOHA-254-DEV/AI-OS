# Store feedback
result = feedback_manager.store_feedback(feedback_input)
# Retrieve all feedback
all_feedback = feedback_manager.get_all_feedback()
import json
from models import FeedbackInput
from datetime import datetime

db_file = "feedback_trainer/feedback.json"

def store_feedback(fb: FeedbackInput):
    try:
        with open(db_file, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(fb.dict())
    with open(db_file, "w") as f:
        json.dump(data, f, indent=2, default=str)
    return {"status": "stored"}

def get_all_feedback():
    try:
        with open(db_file, "r") as f:
            return json.load(f)
    except:
        return []
