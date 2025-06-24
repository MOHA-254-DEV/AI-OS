from voice.listener import VoiceListener
from voice.nlp_parser import NLPParser
from voice.command_router import CommandRouter
import time

class VoiceAssistant:
    def __init__(self):
        self.listener = VoiceListener()
        self.parser = NLPParser()
        self.router = CommandRouter()

    def run_loop(self):
        print("🎙️ Voice Assistant Ready. Say 'exit' to quit.")
        while True:
            try:
                spoken_text = self.listener.listen_and_transcribe()
                print("👂 Heard:", spoken_text)
                if "exit" in spoken_text.lower():
                    print("👋 Exiting voice loop.")
                    break

                parsed = self.parser.extract_context(spoken_text)
                print("🧠 Detected Task:", parsed["detected_task"])
                self.router.route(parsed["detected_task"])

            except KeyboardInterrupt:
                print("⛔ Manual interruption.")
                break
            except Exception as e:
                print("❌ Error:", e)
            time.sleep(2)

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run_loop()
