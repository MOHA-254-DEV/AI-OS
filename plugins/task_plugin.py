from core.task_manager import TaskManager
from utils.logger import log_task
import asyncio

taskman = TaskManager()

async def add_task(args):
    if len(args) < 1:
        return {"error": "Usage: add_task <command> [args...]"}
    command = args[0]
    args_pass = args[1:]
    task = taskman.add_task(command, args_pass)
    log_task("add_task", "queued", str(task))
    return task

async def run_task(args):
    await taskman.run_all()
    return {"status": "all_tasks_executed"}

async def queue_status(args):
    return taskman.list_status()

async def cancel_task(args):
    if not args:
        return {"error": "Usage: cancel_task <task_id>"}
    return taskman.cancel_task(int(args[0]))

async def save_queue(args):
    taskman._save_queue()
    return {"status": "queue_saved"}

def register():
    return {
        "add_task": add_task,
        "run_task": run_task,
        "queue_status": queue_status,
        "cancel_task": cancel_task,
        "save_queue": save_queue
    }
