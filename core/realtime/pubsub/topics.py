# File: /core/realtime/pubsub/topics.py

class Topics:
    """
    Central definition of Pub/Sub communication channels.
    Used across the real-time event bus for agent coordination.
    """
    AGENT_STATUS = 'agent.status'   # Agent lifecycle and health changes
    TASK_UPDATE = 'task.update'     # Task progress or completion notifications
    ERROR_EVENT = 'event.error'     # Faults, exceptions, and critical errors
