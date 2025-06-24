# /core/agent_learning/feedback_collector.py

import logging
from time import time
from typing import Optional

from core.agent_learning.models.feedback_model import FeedbackEntry, feedback_db

# Configure module-level logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    from logging import StreamHandler
    handler = StreamHandler()
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class FeedbackCollector:
    """
    Collects and records agent feedback after task execution.
    """

    def __init__(self, default_score_on_success: float = 1.0, default_score_on_failure: float = -1.0):
        self.success_score = default_score_on_success
        self.failure_score = default_score_on_failure
        logger.debug("FeedbackCollector initialized.")

    def compute_score(self, success: bool) -> float:
        """
        Basic binary scoring. Can be overridden for weighted or dynamic scoring logic.
        """
        return self.success_score if success else self.failure_score

    def collect(
        self,
        agent_id: str,
        task_id: str,
        skill: str,
        success: bool,
        notes: Optional[str] = "",
        score: Optional[float] = None
    ) -> None:
        """
        Collects structured feedback from task outcome.

        Parameters:
        - agent_id (str): Unique agent identifier
        - task_id (str): Task that feedback is associated with
        - skill (str): Skill involved in execution
        - success (bool): Outcome status
        - notes (Optional[str]): Analyst/system remarks
        - score (Optional[float]): Custom score override
        """
        if not all([agent_id, task_id, skill]):
            logger.error("Agent ID, Task ID, and Skill must all be non-empty strings.")
            raise ValueError("Missing required feedback fields.")

        try:
            feedback = FeedbackEntry(
                task_id=task_id,
                agent_id=agent_id,
                skill=skill,
                success=success,
                timestamp=time(),
                score=score if score is not None else self.compute_score(success),
                notes=notes or ""
            )
            feedback_db.add_feedback(feedback)
            logger.info(f"[Feedback] Recorded for agent='{agent_id}', task='{task_id}', skill='{skill}', success={success}")
        except Exception as e:
            logger.exception(f"[Feedback] Failed to record feedback for agent='{agent_id}' on task='{task_id}': {str(e)}")
            raise


# Singleton instance for use throughout the system
feedback_collector = FeedbackCollector()
