# /core/task_router_ai/router.py

class TaskRouter:
    def __init__(self, predictor):
        self.predictor = predictor

    def route_task(self, task_type: str, prefer_success=0.7, prefer_speed=0.3):
        """
        Route a task to the best available agent based on performance score.
        You can tune preference:
        - prefer_success: weight for success rate
        - prefer_speed: weight for speed (inverse of duration)
        """
        predictions = self.predictor.predict(task_type, weight_success=prefer_success, weight_speed=prefer_speed)
        if not predictions:
            print(f"[Router] No agent has history for task type: {task_type}")
            return None

        # Return agent with highest score
        best_agent = next(iter(predictions))  # predictions already sorted
        print(f"[Router] Best agent for '{task_type}': {best_agent} (Score: {predictions[best_agent]['score']})")
        return best_agent
