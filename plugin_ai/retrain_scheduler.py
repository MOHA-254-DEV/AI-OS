from plugin_ai.plugin_feedback_tracker import PluginFeedbackTracker
from plugin_ai.plugin_confidence_analyzer import PluginConfidenceAnalyzer
from plugin_ai.plugin_retrainer import PluginRetrainer

class RetrainScheduler:
    def __init__(self):
        self.tracker = PluginFeedbackTracker()
        self.analyzer = PluginConfidenceAnalyzer(self.tracker)
        self.retrainer = PluginRetrainer()

    def simulate_feedback_stream(self):
        # Simulated feedback for testing
        sample_data = [
            ("pluginA", "agent1", "data_entry", "success", "Worked well."),
            ("pluginA", "agent2", "design", "fail", "Didn't finish."),
            ("pluginB", "agent3", "finance", "success", "Quick response."),
            ("pluginC", "agent2", "trading", "fail", "Timeout."),
            ("pluginC", "agent1", "trading", "fail", "Bad prediction."),
        ]
        for entry in sample_data:
            self.tracker.add_feedback(*entry)

    def run_retrain_loop(self):
        self.analyzer.analyze()
        low_confidence = self.analyzer.get_low_confidence_plugins(threshold=0.75)

        retrained = {}
        for plugin, score in low_confidence.items():
            feedback = self.tracker.get_feedback(plugin)
            dataset = self.retrainer.generate_retraining_dataset(plugin, feedback)
            new_model = self.retrainer.simulate_retrain(plugin, dataset)
            self.retrainer.record_retrain_result(plugin, new_model)
            retrained[plugin] = new_model

        return retrained
