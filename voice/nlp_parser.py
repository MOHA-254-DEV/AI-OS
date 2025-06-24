import re

class NLPParser:
    def __init__(self):
        self.command_map = {
            "open browser": "task:browser_open",
            "search": "task:web_search",
            "create design": "task:design_init",
            "apply job": "task:auto_apply",
            "analyze data": "task:data_analysis",
            "generate report": "task:report_gen",
            "deploy system": "task:deploy_self"
        }

    def parse(self, text: str) -> str:
        text = text.lower()
        for phrase, cmd in self.command_map.items():
            if phrase in text:
                return cmd
        return "task:unknown"

    def extract_context(self, text: str) -> dict:
        return {
            "raw": text,
            "detected_task": self.parse(text)
        }

if __name__ == "__main__":
    parser = NLPParser()
    example = "Please deploy the system now"
    print(parser.extract_context(example))
