# scheduler/test_scheduler.py

from scheduler.task_queue import TaskQueue
from scheduler.task_scheduler import TaskScheduler
from scheduler.priority_levels import Priority

from agent_manager.plugin_loader import load_plugins
from agent_manager.agent_core import Agent
from agent_manager.agent_registry import AgentRegistry
from agent_manager.task_delegator import TaskDelegator

# Setup
plugins = load_plugins()
registry = AgentRegistry()
for plugin_name, plugin_instance in plugins.items():
    agent_name = plugin_name.split('_')[0]
    registry.register(agent_name, Agent(agent_name, plugin_instance))

delegator = TaskDelegator(registry)
queue = TaskQueue()
scheduler = TaskScheduler(queue, delegator)

# Enqueue tasks
queue.add_task({"type": "design", "data": "Build UI Mockup"}, Priority.HIGH)
queue.add_task({"type": "marketing", "data": "Post on Twitter"}, Priority.LOW)
queue.add_task({"type": "design", "data": "Create Product Banner"}, Priority.MEDIUM)

# Run
scheduler.start()

# Run for 10 seconds then stop
import time
time.sleep(10)
scheduler.stop()
