# /core/task_delegation/task_delegator.py

import random
from time import time
from core.task_delegation.agent_registry import agent_registry
from core.task_delegation.queue_manager import queue_manager
from core.agent_messaging.agent_protocol import AgentMessage
from core.agent_messaging.agent_messenger import agent_messenger

MAX_RETRY_COUNT = 3
RETRY_TRACKER = {}

class TaskDelegator:
    def __init__(self):
        pass

    def delegate(self):
        task = queue_manager.get_next_task()
        if not task:
            print("[Delegator] No tasks in queue.")
            return

        task_id, task_data = task
        required_skill = task_data.get("skill")
        if not required_skill:
            print(f"[Delegator] Task {task_id} missing skill requirement.")
            return

        candidates = agent_registry.get_idle_agents_with_skill(required_skill)
        if not candidates:
            retry_count = RETRY_TRACKER.get(task_id, 0)
            if retry_count >= MAX_RETRY_COUNT:
                print(f"[Delegator] Task {task_id} exceeded max retries. Dropping.")
                return

            print(f"[Delegator] No agents for skill '{required_skill}'. Requeuing task {task_id}.")
            RETRY_TRACKER[task_id] = retry_count + 1
            queue_manager.enqueue_task(task_data["priority"], task_id, task_data)
            return

        assigned_agent = random.choice(candidates)
        agent_registry.assign_task(assigned_agent, task_id)

        message = AgentMessage(
            sender="delegator",
            receiver=assigned_agent,
            command=f"cmd.execute.{required_skill}",
            payload={"task_id": task_id, "details": task_data["details"]}
        )
        agent_messenger.send(message)

        print(f"[Delegator] ✅ Assigned task {task_id} to agent {assigned_agent}.")
        RETRY_TRACKER.pop(task_id, None)  # Clear retry tracker on success

    def add_task(self, task_id: str, skill: str, priority: str, details: dict):
        if not all([task_id, skill, priority, details]):
            print(f"[Delegator] Invalid task input. Missing fields.")
            return

        timestamp = time()
        task_data = {
            "skill": skill,
            "priority": priority,
            "timestamp": timestamp,
            "details": details
        }
        queue_manager.enqueue_task(priority, task_id, task_data)
        print(f"[Delegator] 📝 Task {task_id} queued with priority '{priority}'.")

# Singleton instance
task_delegator = TaskDelegator()
