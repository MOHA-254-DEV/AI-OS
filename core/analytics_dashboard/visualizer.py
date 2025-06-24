import matplotlib.pyplot as plt
import seaborn as sns
from .analytics_engine import AnalyticsEngine
from typing import Optional

class Visualiser:
    def __init__(self, engine: AnalyticsEngine):
        """
        Initializes the Visualiser with an AnalyticsEngine to fetch metrics data.

        Args:
            engine (AnalyticsEngine): The engine used to fetch analytics results.
        """
        self.engine = engine

    def plot_task_completion_trend(self, save_path: Optional[str] = None):
        """
        Plots the task completion trend over time.

        Args:
            save_path (str, optional): If provided, saves the plot to this path instead of displaying it.
        """
        task_trend = self.engine.analyze().get("task_completion_trend", {})

        if not task_trend:
            print("[Visualiser] No data available for task completion trend.")
            return

        dates = list(task_trend.keys())
        task_counts = list(task_trend.values())

        plt.figure(figsize=(10, 6))
        plt.plot(dates, task_counts, marker='o', color='b', linestyle='-', linewidth=2, markersize=6)
        plt.title("📈 Task Completion Trend", fontsize=16)
        plt.xlabel("Date", fontsize=12)
        plt.ylabel("Number of Tasks Completed", fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path)
            print(f"[Visualiser] Task trend chart saved to: {save_path}")
        else:
            plt.show()

        plt.close()

    def plot_agent_success_rate(self, save_path: Optional[str] = None):
        """
        Plots the agent success rates.

        Args:
            save_path (str, optional): If provided, saves the plot to this path instead of displaying it.
        """
        success_rate = self.engine.analyze().get("agent_success_rate", {})

        if not success_rate:
            print("[Visualiser] No data available for agent success rate.")
            return

        agents = list(success_rate.keys())
        success_percentages = [rate * 100 for rate in success_rate.values()]  # Convert to %

        plt.figure(figsize=(10, 6))
        sns.barplot(x=agents, y=success_percentages, palette="viridis")
        plt.title("✅ Agent Success Rate", fontsize=16)
        plt.xlabel("Agent ID", fontsize=12)
        plt.ylabel("Success Rate (%)", fontsize=12)
        plt.xticks(rotation=45)
        plt.ylim(0, 100)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path)
            print(f"[Visualiser] Success rate chart saved to: {save_path}")
        else:
            plt.show()

        plt.close()

    def generate_dashboard(self, save: bool = False, output_dir: str = "charts"):
        """
        Generates a visual dashboard of key agent performance metrics.

        Args:
            save (bool): If True, saves plots to files instead of displaying them.
            output_dir (str): Directory where charts will be saved if save=True.
        """
        if save:
            import os
            os.makedirs(output_dir, exist_ok=True)
            self.plot_task_completion_trend(save_path=f"{output_dir}/task_trend.png")
            self.plot_agent_success_rate(save_path=f"{output_dir}/agent_success.png")
        else:
            self.plot_task_completion_trend()
            self.plot_agent_success_rate()
