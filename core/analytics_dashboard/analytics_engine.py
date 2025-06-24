from typing import Dict, Any
import logging

from .metrics_collector import MetricsCollector
from .trends import TrendAnalyzer


class AnalyticsEngine:
    """
    Coordinates logging and analysis of agent performance metrics.
    Supports recording task outcomes and generating trend reports.
    """

    def __init__(self, collector: MetricsCollector = None, trend_analyzer: TrendAnalyzer = None):
        """
        Initialize the Analytics Engine with optional injected components.

        Args:
            collector (MetricsCollector, optional): Custom metrics collector (defaults to new instance).
            trend_analyzer (TrendAnalyzer, optional): Custom trend analyzer (defaults to new instance).
        """
        self.collector = collector or MetricsCollector()
        self.trend_analyzer = trend_analyzer or TrendAnalyzer()

        self.logger = logging.getLogger("AnalyticsEngine")
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def log_task(self, agent_id: str, task_type: str, status: str) -> None:
        """
        Records a task execution outcome for analytics.

        Args:
            agent_id (str): Unique agent identifier.
            task_type (str): Type of the task (e.g., 'design', 'marketing').
            status (str): Task result status (e.g., 'success', 'failure').
        """
        try:
            self.collector.record_task(agent_id, task_type, status)
            self.logger.info(f"Logged task for agent '{agent_id}': {task_type} [{status}]")
        except Exception as e:
            self.logger.exception(f"Failed to log task for agent '{agent_id}': {e}")

    def log_error(self, agent_id: str, error_message: str) -> None:
        """
        Records an error reported by the agent.

        Args:
            agent_id (str): Agent's unique ID.
            error_message (str): Descriptive error message.
        """
        try:
            self.collector.record_error(agent_id, error_message)
            self.logger.error(f"Logged error for agent '{agent_id}': {error_message}")
        except Exception as e:
            self.logger.exception(f"Failed to log error for agent '{agent_id}': {e}")

    def analyze(self) -> Dict[str, Any]:
        """
        Generates an analytics report with task trends and success rates.

        Returns:
            Dict[str, Any]: {
                'task_completion_trend': <dict>,
                'agent_success_rate': <dict>
            }
        """
        try:
            metrics = self.collector.get_metrics()
            trends = self.trend_analyzer(metrics)

            result = {
                "task_completion_trend": trends.task_completion_trend(),
                "agent_success_rate": trends.agent_success_rate(),
            }

            self.logger.info("Analytics analysis completed.")
            return result

        except Exception as e:
            self.logger.exception("Analytics analysis failed.")
            return {
                "task_completion_trend": {},
                "agent_success_rate": {}
            }
