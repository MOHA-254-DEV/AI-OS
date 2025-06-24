import json
from datetime import datetime

class ReportEngine:
    def __init__(self):
        self.data_sources = {}

    def add_data_source(self, name, data_func):
        self.data_sources[name] = data_func

    def collect_data(self):
        result = {"generated_at": str(datetime.now()), "sections": {}}
        for name, func in self.data_sources.items():
            try:
                result["sections"][name] = func()
            except Exception as e:
                result["sections"][name] = {"error": str(e)}
        return result

    def to_json(self, data, path="reporting/output/report.json"):
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"[REPORT] JSON saved at {path}")

if __name__ == "__main__":
    engine = ReportEngine()
    engine.add_data_source("test", lambda: {"status": "ok", "entries": 3})
    report_data = engine.collect_data()
    engine.to_json(report_data)
