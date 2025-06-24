# feedback_trainer/main.py
from fastapi import FastAPI
from models import FeedbackInput
from feedback_manager import store_feedback, get_all_feedback
from correction_engine import find_applicable_correction

app = FastAPI()

@app.post("/feedback")
def submit_feedback(fb: FeedbackInput):
    return store_feedback(fb)

@app.get("/feedback")
def feedback_log():
    return get_all_feedback()

@app.post("/correction")
def apply_correction(task_id: str, output: str):
    return find_applicable_correction(task_id, output)
