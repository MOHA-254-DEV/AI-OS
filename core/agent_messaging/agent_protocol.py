"""
agent_protocol.py

Defines the AgentMessage class used for inter-agent communication
in the autonomous AI operating system.
"""

from datetime import datetime
from typing import Dict, Any


class AgentMessage:
    """
    Represents a message exchanged between agents.
    Includes metadata such as sender, receiver, command, payload, and timestamp.
    """

    def __init__(
        self,
        sender: str,
        receiver: str,
        command: str,
        payload: Dict[str, Any],
        timestamp: str = None
    ):
        if not all([sender, receiver, command]):
            raise ValueError("Sender, receiver, and command must be provided.")
        if not isinstance(payload, dict):
            raise TypeError("Payload must be a dictionary.")

        self.sender = sender
        self.receiver = receiver
        self.command = command
        self.payload = payload
        self.timestamp = timestamp or datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the AgentMessage to a dictionary.
        """
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "command": self.command,
            "payload": self.payload,
            "timestamp": self.timestamp,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "AgentMessage":
        """
        Deserialize a dictionary into an AgentMessage instance.
        Performs minimal validation and sets fallback values where appropriate.
        """
        required_keys = ["sender", "receiver", "command", "payload"]

        if not isinstance(data, dict):
            raise TypeError("Input data must be a dictionary.")

        missing_keys = [key for key in required_keys if key not in data]
        if missing_keys:
            raise ValueError(f"Missing required keys in message: {', '.join(missing_keys)}")

        sender = str(data["sender"])
        receiver = str(data["receiver"])
        command = str(data["command"])
        payload = data["payload"]
        timestamp = data.get("timestamp", datetime.utcnow().isoformat())

        return AgentMessage(
            sender=sender,
            receiver=receiver,
            command=command,
            payload=payload,
            timestamp=timestamp
        )
