import pandas as pd
import openai
import os

class ReportEngine:
    def __init__(self, api_key=None):
        openai.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.data = None
        self.summary = ""

    def load_csv(self, path: str):
        self.data = pd.read_csv(path)
        print(f"[DATA] Loaded {len(self.data)} rows from {path}")

    def analyze_data(self):
        desc = self.data.describe(include="all").to_string()
        print("[ANALYSIS] Generating AI Summary...")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Summarize the following data description:"},
                {"role": "user", "content": desc}
            ]
        )
        self.summary = response.choices[0].message.content
        return self.summary

    def get_raw_data(self):
        return self.data

    def get_summary(self):
        return self.summary or "Run analyze_data() first."

if __name__ == "__main__":
    engine = ReportEngine()
    engine.load_csv("sample_data.csv")
    print(engine.analyze_data())
