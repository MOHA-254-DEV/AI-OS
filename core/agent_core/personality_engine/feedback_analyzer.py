import logging
from textblob import TextBlob

class FeedbackAnalyzer:
    def __init__(self):
        self.logger = logging.getLogger("FeedbackAnalyzer")
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

        # Style preference keyword map
        self.style_keywords = {
            "concise": ["brief", "short", "straightforward", "summary"],
            "verbose": ["detailed", "explain more", "elaborate", "long"],
            "empathetic": ["friendly", "polite", "kind", "respectful"]
        }

    def analyze(self, raw_feedback: str) -> dict:
        if not raw_feedback or not isinstance(raw_feedback, str):
            self.logger.error("Invalid feedback provided.")
            return {"satisfaction": 0.0, "style_preference": "unknown"}

        self.logger.info("Analyzing feedback...")

        result = {
            "satisfaction": self._extract_score(raw_feedback),
            "style_preference": self._extract_style(raw_feedback)
        }

        self.logger.info(f"Analysis result: {result}")
        return result

    def _extract_score(self, text: str) -> float:
        """
        Convert sentiment polarity into a 0-1 satisfaction score.
        """
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            self.logger.debug(f"Sentiment polarity: {polarity}")

            if polarity >= 0.5:
                return 0.9
            elif polarity >= 0.0:
                return 0.5
            else:
                return 0.2
        except Exception as e:
            self.logger.error(f"Error in sentiment analysis: {e}")
            return 0.0

    def _extract_style(self, text: str) -> str:
        """
        Determines communication style preference using keyword matching.
        """
        lowered = text.lower()
        for style, keywords in self.style_keywords.items():
            if any(word in lowered for word in keywords):
                return style
        return "balanced"

# === Example usage ===
if __name__ == "__main__":
    feedback = "The service was excellent! However, please be more detailed next time."
    analyzer = FeedbackAnalyzer()
    result = analyzer.analyze(feedback)
    print(result)
