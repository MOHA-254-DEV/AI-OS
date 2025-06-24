from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import time


@dataclass
class FeedbackEntry:
    task_id: str
    agent_id: str
    skill: str
    success: bool
    timestamp: Optional[float] = None
    score: float = 0.0
    notes: str = ""

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()

    def __str__(self):
        status = "✅ Success" if self.success else "❌ Fail"
        return (f"[{self.task_id}] Agent: {self.agent_id} | Skill: {self.skill} | "
                f"Score: {self.score} | {status} | Note: {self.notes}")


class FeedbackDatabase:
    def __init__(self):
        self.data: Dict[str, List[FeedbackEntry]] = {}

    def add_feedback(self, feedback: FeedbackEntry) -> None:
        """Add feedback entry to the database."""
        if not isinstance(feedback, FeedbackEntry):
            raise TypeError("Expected FeedbackEntry instance")
        self.data.setdefault(feedback.agent_id, []).append(feedback)

    def get_agent_feedback(self, agent_id: str) -> List[FeedbackEntry]:
        return self.data.get(agent_id, [])

    def get_latest_feedback(self, agent_id: str) -> Optional[FeedbackEntry]:
        feedback_list = self.get_agent_feedback(agent_id)
        return max(feedback_list, key=lambda x: x.timestamp, default=None)

    def get_feedback_for_task(self, task_id: str) -> List[FeedbackEntry]:
        return [
            entry for entries in self.data.values() for entry in entries
            if entry.task_id == task_id
        ]

    def average_score(self, agent_id: str) -> float:
        feedback_list = self.get_agent_feedback(agent_id)
        if not feedback_list:
            return 0.0
        return round(sum(f.score for f in feedback_list) / len(feedback_list), 2)

    def filter_feedback(
        self,
        agent_id: Optional[str] = None,
        skill: Optional[str] = None,
        success: Optional[bool] = None,
        since: Optional[float] = None,
        until: Optional[float] = None
    ) -> List[FeedbackEntry]:
        """
        Filter feedback by various criteria.
        """
        entries = []
        agents = [agent_id] if agent_id else list(self.data.keys())

        for aid in agents:
            for entry in self.data.get(aid, []):
                if skill and entry.skill != skill:
                    continue
                if success is not None and entry.success != success:
                    continue
                if since and entry.timestamp < since:
                    continue
                if until and entry.timestamp > until:
                    continue
                entries.append(entry)
        return entries

    def to_dict(self) -> Dict[str, List[Dict]]:
        """Convert to a JSON-serializable dictionary."""
        return {
            agent_id: [asdict(entry) for entry in entries]
            for agent_id, entries in self.data.items()
        }

    def __str__(self):
        all_entries = [str(entry) for entries in self.data.values() for entry in entries]
        return "\n".join(all_entries)
