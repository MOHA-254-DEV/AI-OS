# /core/agent_learning/skill_adaptive_engine.py

import logging
from collections import defaultdict
from typing import Dict

from core.task_delegation.agent_registry import agent_registry
from core.agent_learning.models.feedback_model import feedback_db

# Configure module logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    from logging import StreamHandler
    handler = StreamHandler()
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class SkillAdaptiveEngine:
    """
    Dynamically updates agents' skill sets based on accumulated feedback.
    Adds or removes skills based on success/failure performance thresholds.
    """

    def __init__(self, success_threshold: float = 3.0, failure_threshold: float = 3.0):
        self.success_threshold = success_threshold
        self.failure_threshold = failure_threshold
        logger.debug("SkillAdaptiveEngine initialized.")

    def adapt_skills(self) -> None:
        """
        Iterates through all registered agents, evaluates their feedback history,
        and updates their skill profiles.
        """
        try:
            for agent_id, agent_data in agent_registry.agents.items():
                feedback_entries = feedback_db.get_agent_feedback(agent_id)

                if not feedback_entries:
                    logger.debug(f"[SkillAdapt] No feedback found for agent '{agent_id}'. Skipping.")
                    continue

                skill_scores = self._accumulate_skill_scores(feedback_entries)

                for skill, score in skill_scores.items():
                    skills = agent_data.get("skills", [])

                    if score >= self.success_threshold and skill not in skills:
                        skills.append(skill)
                        logger.info(f"[SkillAdapt] ✅ Skill '{skill}' ADDED to '{agent_id}' (score: {score})")

                    elif score <= -self.failure_threshold and skill in skills:
                        skills.remove(skill)
                        logger.info(f"[SkillAdapt] ❌ Skill '{skill}' REMOVED from '{agent_id}' (score: {score})")

        except Exception as e:
            logger.exception(f"[SkillAdapt] Error during skill adaptation: {str(e)}")

    def _accumulate_skill_scores(self, feedback_entries: list) -> Dict[str, float]:
        """
        Aggregates scores per skill from feedback entries.

        Returns:
            Dictionary of skill => cumulative_score
        """
        scores = defaultdict(float)
        for entry in feedback_entries:
            if hasattr(entry, "skill") and hasattr(entry, "score"):
                scores[entry.skill] += entry.score
        return scores


# Singleton instance
skill_adaptive_engine = SkillAdaptiveEngine()
