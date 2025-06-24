from typing import Dict, Any, Optional, List, Tuple
from .role_manager import RoleManager
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContextSwitcher:
    """
    Dynamically recommends and switches roles for agents based on task context and semantic capabilities.
    """

    def __init__(self, fallback_role: str = "BusinessStrategist"):
        self.role_mgr = RoleManager()
        self.fallback_role = fallback_role

    def recommend_role(self, task_description: str, top_n: int = 1) -> Union[str, List[Tuple[str, float]]]:
        """
        Recommend the best-matching role(s) based on task description using fuzzy semantic matching.

        :param task_description: Description of the task in natural language
        :param top_n: Return top-N matches with confidence scores if > 1
        :return: Best matching role name or list of (role, score) tuples
        """
        if not task_description or not isinstance(task_description, str):
            return self.fallback_role

        keywords = self._extract_keywords(task_description)
        if not keywords:
            return self.fallback_role

        match_scores: Dict[str, float] = {}

        for role, meta in self.role_mgr.roles.items():
            capabilities = meta.get("capabilities", [])
            if not isinstance(capabilities, list):
                continue

            score = self._calculate_score(capabilities, keywords)
            if score > 0:
                match_scores[role] = score

        if not match_scores:
            return self.fallback_role

        sorted_roles = sorted(match_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_roles[0][0] if top_n == 1 else sorted_roles[:top_n]

    def _extract_keywords(self, text: str) -> List[str]:
        """ Extracts cleaned keywords from text. """
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", "", text)
        return text.split()

    def _calculate_score(self, capabilities: List[str], keywords: List[str]) -> float:
        """ Compute match score based on overlap with weighting. """
        score = 0.0
        for cap in capabilities:
            cap = cap.lower()
            cap_words = cap.split()

            match_strength = sum(
                1.0 if cap_word in keywords else 0.5 if any(cap_word in kw for kw in keywords) else 0
                for cap_word in cap_words
            )
            score += match_strength / len(cap_words) if cap_words else 0
        return round(score, 3)

    def auto_switch(self, agent: Any, task: Dict[str, Any]) -> Optional[str]:
        """
        Automatically switches the agent's role based on task description.

        :param agent: Agent object with `set_role()` and `name` attributes
        :param task: Dictionary containing a `description` field
        :return: Role name or None if failed
        """
        if not hasattr(agent, 'set_role') or not hasattr(agent, 'name'):
            logger.error("[RoleSwitch][Error] Invalid agent interface.")
            return None

        description = task.get("description", "")
        recommended = self.recommend_role(description)

        if isinstance(recommended, list):
            new_role = recommended[0][0]  # Use the top-scored role
        else:
            new_role = recommended

        agent.set_role(new_role)
        logger.info(f"[RoleSwitch] Agent '{agent.name}' switched to role: '{new_role}'")
        return new_role
