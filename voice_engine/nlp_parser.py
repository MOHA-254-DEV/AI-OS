import re
import json

class NLPParser:
    def __init__(self):
        self.commands = {
            "freelance": ["find freelance", "get me a freelance", "apply job"],
            "analytics": ["generate report", "analyze sales", "monthly summary"],
            "deploy": ["deploy app", "host", "push project"],
            "search": ["search", "look up", "find on internet"],
            "exit": ["shutdown", "exit", "terminate"]
        }

    def parse_command(self, text):
        for key, keywords in self.commands.items():
            for phrase in keywords:
                if phrase in text:
                    print(f"[NLP] Matched intent: {key}")
                    return key
        print("[NLP] No matching intent.")
        return "unknown"

    def expand_commands(self, new_map):
        self.commands.update(new_map)

if __name__ == "__main__":
    parser = NLPParser()
    command = parser.parse_command("can you deploy app now")
    print("Parsed Command:", command)
