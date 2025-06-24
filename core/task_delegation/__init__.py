"""
Task Delegation Core Package

This package provides interfaces and singletons for:
- Task delegation logic (`task_delegator`)
- Agent tracking and management (`agent_registry`)
- Task queue operations (`queue_manager`)
"""

# Lazy-import singleton instances to avoid circular import issues
from .task_delegator import task_delegator
from .agent_registry import agent_registry
from .queue_manager import queue_manager

__all__ = [
    "task_delegator",
    "agent_registry",
    "queue_manager"
]
