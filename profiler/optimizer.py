import statistics

class Optimizer:
    def __init__(self, profiler_core):
        self.profiler = profiler_core
        self.plugin_scores = {}

    def analyze(self):
        results = self.profiler.get_all_results()
        plugin_data = {}

        for result in results:
            plugin = result["plugin"]
            plugin_data.setdefault(plugin, {"runtimes": [], "status": []})
            plugin_data[plugin]["runtimes"].append(result["runtime"])
            plugin_data[plugin]["status"].append(result["status"])

        for plugin, data in plugin_data.items():
            avg_runtime = statistics.mean(data["runtimes"])
            success_rate = data["status"].count("success") / len(data["status"])
            score = (1 / (avg_runtime + 0.01)) * success_rate
            self.plugin_scores[plugin] = round(score, 3)

        return self.plugin_scores

    def suggest_priorities(self):
        scores = self.analyze()
        sorted_plugins = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return {plugin: i+1 for i, (plugin, _) in enumerate(sorted_plugins)}
