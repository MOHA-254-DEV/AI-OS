from plugins.evaluator.plugin_scorecard import PluginScore

class PluginRatingEngine:
    def __init__(self):
        self.scores = {}

    def get_or_create_score(self, plugin_id: str) -> PluginScore:
        if plugin_id not in self.scores:
            self.scores[plugin_id] = PluginScore(plugin_id)
        return self.scores[plugin_id]

    def update_plugin_score(self, plugin_id: str, success: bool, cpu: float, mem: float, exec_time: float):
        score = self.get_or_create_score(plugin_id)
        score.update_stats(success, cpu, mem, exec_time)
        self.recalculate_rating(score)

    def recalculate_rating(self, score: PluginScore):
        success_ratio = score.success_count / max(score.total_runs, 1)
        fail_penalty = score.failure_count / max(score.total_runs, 1)
        cpu_penalty = min(sum(score.cpu_usage[-10:]) / 10, 100.0)
        mem_penalty = min(sum(score.memory_usage[-10:]) / 10, 100.0)
        speed_factor = min(sum(score.exec_times[-10:]) / 10, 5.0)

        score.rating = (
            (success_ratio * 60)
            - (fail_penalty * 10)
            - (cpu_penalty * 0.1)
            - (mem_penalty * 0.1)
            - (speed_factor * 2)
        )

    def get_scorecard(self):
        return [s.to_dict() for s in self.scores.values()]
