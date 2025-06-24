from collections import Counter

class PluginConfidenceAnalyzer:
    def __init__(self, feedback_tracker):
        self.feedback_tracker = feedback_tracker
        self.confidence_scores = {}

    def analyze(self):
        all_feedback = self.feedback_tracker.get_all_feedback()
        for plugin, entries in all_feedback.items():
            outcomes = [entry["outcome"] for entry in entries]
            outcome_counts = Counter(outcomes)
            success = outcome_counts.get("success", 0)
            fail = outcome_counts.get("fail", 0)
            total = success + fail

            if total == 0:
                self.confidence_scores[plugin] = 1.0  # assume full trust
                continue

            score = success / total
            self.confidence_scores[plugin] = round(score, 3)

    def get_confidence_scores(self):
        return self.confidence_scores

    def get_low_confidence_plugins(self, threshold=0.7):
        return {p: s for p, s in self.confidence_scores.items() if s < threshold}
