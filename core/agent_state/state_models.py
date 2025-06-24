# core/agent_state/state_models.py

from typing import Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime
from enum import Enum


class AgentStatus(str, Enum):
    """
    Defines all allowed agent lifecycle statuses.
    """
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
    OFFLINE = "offline"
    BOOTING = "booting"
    TERMINATED = "terminated"


class AgentState(BaseModel):
    """
    A full snapshot of an agent's operational state.
    Includes task reference, status, and optional metadata.
    """
    agent_id: str = Field(..., description="Unique ID for the agent.")
    task_id: str = Field(..., description="ID of the task the agent is (or was) working on.")
    status: AgentStatus = Field(..., description="Current operational status.")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when this state was recorded.")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Optional metadata for debugging or diagnostics.")

    @validator("agent_id", "task_id")
    def validate_non_empty(cls, value, field):
        if not value or not value.strip():
            raise ValueError(f"{field.name} must be a non-empty string.")
        return value

    class Config:
        schema_extra = {
            "example": {
                "agent_id": "agent_42",
                "task_id": "task_1234",
                "status": "running",
                "timestamp": "2025-05-14T15:27:45Z",
                "metadata": {
                    "cpu": "low",
                    "memory_usage": "512MB",
                    "location": "us-central"
                }
            }
        }


class StateUpdate(BaseModel):
    """
    Describes a targeted field update to an agent's state.
    Used for partial, incremental updates.
    """
    agent_id: str = Field(..., description="ID of the agent being updated.")
    field: str = Field(..., description="Field to update in the agent's state.")
    new_value: Any = Field(..., description="New value for the specified field.")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When this update occurred.")

    @validator("agent_id", "field")
    def validate_non_empty_fields(cls, value, field):
        if not value or not value.strip():
            raise ValueError(f"{field.name} must be a non-empty string.")
        return value

    class Config:
        schema_extra = {
            "example": {
                "agent_id": "agent_42",
                "field": "status",
                "new_value": "completed",
                "timestamp": "2025-05-14T15:30:00Z"
            }
        }
