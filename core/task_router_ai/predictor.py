# /core/task_router_ai/predictor.py

class AgentBehaviorPredictor:
    def __init__(self, profile_engine):
        self.profile_engine = profile_engine

    def predict(self, task_type: str, weight_success=0.7, weight_speed=0.3):
        """
        Predicts agent performance for a task.
        Returns ranked prediction scores.
        """
        profiles = self.profile_engine.build_profiles()
        predictions = {}

        for agent_id, stats in profiles.items():
            if task_type in stats:
                agent_stats = stats[task_type]
                success_rate = agent_stats["success_rate"]
                avg_duration = agent_stats["avg_duration"]

                # Normalize duration inversely (lower is better)
                # Avoid division by zero
                duration_score = 1 / (avg_duration + 1e-5)

                # Weighted score (customizable)
                score = (weight_success * success_rate) + (weight_speed * duration_score)

                predictions[agent_id] = {
                    "predicted_success": success_rate,
                    "predicted_duration": avg_duration,
                    "score": round(score, 4)
                }

        return dict(sorted(predictions.items(), key=lambda x: -x[1]["score"]))

    def best_agent(self, task_type: str):
        predictions = self.predict(task_type)
        if not predictions:
            return None
        return next(iter(predictions))  # highest ranked agent
