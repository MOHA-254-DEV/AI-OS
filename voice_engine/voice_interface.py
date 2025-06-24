from voice_engine.stt_engine import STTEngine
from voice_engine.nlp_parser import NLPParser

class VoiceInterface:
    def __init__(self):
        self.stt = STTEngine()
        self.nlp = NLPParser()

    def execute_command(self, command):
        # Map NLP result to system task
        if command == "freelance":
            print("[TASK] Searching freelance jobs...")
            # trigger job aggregator here
        elif command == "analytics":
            print("[TASK] Generating reports...")
            # trigger reporting engine
        elif command == "deploy":
            print("[TASK] Deploying application...")
            # trigger deployment engine
        elif command == "search":
            print("[TASK] Performing web search...")
            # trigger search module
        elif command == "exit":
            print("[TASK] Shutting down...")
            exit(0)
        else:
            print("[TASK] Unrecognized command.")

    def run_voice_loop(self):
        while True:
            voice_input = self.stt.listen()
            if not voice_input:
                continue
            command = self.nlp.parse_command(voice_input)
            self.execute_command(command)

if __name__ == "__main__":
    interface = VoiceInterface()
    interface.run_voice_loop()
