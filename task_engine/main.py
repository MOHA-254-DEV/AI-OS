# task_engine/main.py
from fastapi import FastAPI
from task_queue import add_task, get_next_task, list_tasks
from agent_feedback import update_feedback
from models import TaskInput

app = FastAPI()

@app.post("/submit-task")
def submit(task: TaskInput):
    return add_task(task)

@app.get("/next-task")
def next_task():
    return get_next_task()

@app.get("/tasks")
def tasks():
    return list_tasks()

@app.post("/agent-feedback")
def feedback(agent_id: str, task_id: str, score: float):
    return update_feedback(agent_id, task_id, score)
