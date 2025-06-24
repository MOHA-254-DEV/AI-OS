import logging

class BehaviorMatrix:
    def __init__(self, profile):
        """
        Initialize with an agent's behavior profile.
        :param profile: Dictionary with keys like 'focus', 'verbosity', 'communication_style', etc.
        """
        self.profile = profile or {}
        self.logger = logging.getLogger("BehaviorMatrix")
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def decide_strategy(self, task_type: str) -> str:
        """
        Determine strategy for a task based on profile and type.
        :param task_type: Task category (e.g., 'research', 'coding', 'ideation').
        :return: Strategy string.
        """
        strategy_map = {
            "research": self._research_strategy,
            "coding": self._coding_strategy,
            "ideation": self._ideation_strategy
        }

        strategy_func = strategy_map.get(task_type)
        if strategy_func:
            strategy = strategy_func()
            self.logger.info(f"[Strategy] For task '{task_type}', selected: {strategy}")
            return strategy

        self.logger.warning(f"[Strategy] Unknown task type '{task_type}', using fallback strategy.")
        return "standard"

    def _research_strategy(self) -> str:
        focus = self.profile.get("focus", "")
        return "deep_search" if focus == "research" else "quick_scan"

    def _coding_strategy(self) -> str:
        focus = self.profile.get("focus", "")
        return "modular" if focus == "integration" else "monolithic"

    def _ideation_strategy(self) -> str:
        focus = self.profile.get("focus", "")
        return "divergent" if focus == "ideation" else "convergent"

    def communication_style(self) -> str:
        return self.profile.get("communication_style", "neutral")

    def verbosity_level(self) -> int:
        return int(self.profile.get("verbosity", 0))

    def is_risk_averse(self) -> bool:
        return float(self.profile.get("risk_tolerance", 0.0)) < 0.5

    def prefers_collaboration(self) -> bool:
        return float(self.profile.get("collaboration", 0.0)) > 0.6

    def describe(self) -> dict:
        """
        Summarizes all core behavioral attributes of the agent.
        """
        summary = {
            "communication_style": self.communication_style(),
            "verbosity": self.verbosity_level(),
            "risk_averse": self.is_risk_averse(),
            "collaborative": self.prefers_collaboration(),
            "focus": self.profile.get("focus", "undefined")
        }
        self.logger.info(f"[Agent Profile Summary] {summary}")
        return summary
