# /core/task_router_ai/agent_profile.py

from collections import defaultdict

class AgentProfile:
    def __init__(self, history_db):
        self.history_db = history_db

    def build_profiles(self):
        """
        Build performance profiles for each agent based on historical task data.
        Each profile includes per-task-type success rate and average duration.
        """
        profiles = {}
        all_data = self.history_db.get_all_data()

        for agent_id, task_records in all_data.items():
            task_summary = defaultdict(lambda: {
                "total": 0,
                "success": 0,
                "total_duration": 0.0
            })

            for task in task_records:
                task_type = task.get("task_type")
                success = task.get("success", False)
                duration = task.get("duration", 0.0)

                entry = task_summary[task_type]
                entry["total"] += 1
                entry["total_duration"] += duration
                if success:
                    entry["success"] += 1

            # Post-process to compute averages and success rate
            for task_type, stats in task_summary.items():
                total = stats["total"]
                stats["avg_duration"] = round(stats["total_duration"] / total, 2) if total else 0.0
                stats["success_rate"] = round(stats["success"] / total, 2) if total else 0.0
                # Clean up the temp variable
                del stats["total_duration"]

            profiles[agent_id] = dict(task_summary)

        return profiles
