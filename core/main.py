# core/main.py

from core.tasks.task_queue import TaskQueue
from core.tasks.task_dispatcher import TaskDispatcher
from utils.logger import logger

def seed_tasks():
    return [
        {'name': 'Design Homepage', 'type': 'graphic_design'},
        {'name': 'Launch Ad Campaign', 'type': 'ads'},
        {'name': 'Deploy Backend API', 'type': 'api_dev'},
        {'name': 'Generate Budget Report', 'type': 'analytics'},
        {'name': 'SEO Optimization', 'type': 'seo'},
        {'name': 'Build React UI', 'type': 'full_stack'},
        {'name': 'Conduct Market Analysis', 'type': 'social_media'},
        {'name': 'Trade Simulation', 'type': 'trading'},
    ]

def main():
    logger.info("🚀 Starting Task Dispatch Engine...")

    queue = TaskQueue()
    dispatcher = TaskDispatcher()

    for i, task in enumerate(seed_tasks()):
        queue.add_task(task, priority=i)
        logger.info(f"[Queue] Task '{task['name']}' added with priority {i}")

    while queue.has_tasks():
        task = queue.get_next_task()
        logger.info(f"[System] Dispatching task: {task['name']} ({task['type']})")
        result = dispatcher.dispatch(task)
        logger.info(f"[System] Result: {result}")
        print(f"✅ {task['name']} → {result}")

    logger.info("✅ All tasks dispatched and processed.")

if __name__ == "__main__":
    main()
    main()
