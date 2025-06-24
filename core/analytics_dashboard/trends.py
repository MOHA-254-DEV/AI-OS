from collections import Counter
from datetime import datetime
import pandas as pd
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class TrendAnalyzer:
    def __init__(self, metrics: Dict[str, Any]):
        """
        Initialize the TrendAnalyzer with collected metrics.

        Args:
            metrics (Dict[str, Any]): Dictionary containing "tasks" and "errors" logs.
        """
        self.metrics = metrics

    def task_completion_trend(self) -> Dict[str, int]:
        """
        Aggregates the number of tasks completed per day.

        Returns:
            Dict[str, int]: Mapping of date (YYYY-MM-DD) to number of completed tasks.
        """
        try:
            tasks = self.metrics.get("tasks", [])
            if not tasks:
                logger.info("No tasks found in metrics for trend analysis.")
                return {}

            df = pd.DataFrame(tasks)
            if "timestamp" not in df:
                logger.warning("Missing 'timestamp' in tasks data.")
                return {}

            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
            df = df.dropna(subset=["timestamp"])  # Remove any invalid timestamps

            # Group by date and count occurrences
            trend = df.groupby(df["timestamp"].dt.date).size().to_dict()
            return {str(date): int(count) for date, count in trend.items()}

        except Exception as e:
            logger.exception("Error while analyzing task completion trend.")
            return {}

    def agent_success_rate(self) -> Dict[str, float]:
        """
        Computes each agent's task success rate (successes / total tasks).

        Returns:
            Dict[str, float]: Agent ID mapped to success percentage (0.00 to 1.00).
        """
        try:
            tasks = self.metrics.get("tasks", [])
            if not tasks:
                logger.info("No task data available to compute success rate.")
                return {}

            df = pd.DataFrame(tasks)
            if "agent_id" not in df or "status" not in df:
                logger.warning("Required fields ('agent_id', 'status') missing from tasks data.")
                return {}

            # Filter for success cases
            success_df = df[df["status"] == "success"]
            success_counts = success_df["agent_id"].value_counts()
            total_counts = df["agent_id"].value_counts()

            success_rate = {
                agent: round(success_counts.get(agent, 0) / total_counts[agent], 2)
                for agent in total_counts.index
            }
            return success_rate

        except Exception as e:
            logger.exception("Error while calculating agent success rate.")
            return {}
