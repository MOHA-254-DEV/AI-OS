import speech_recognition as sr
import threading
import time
import logging

logger = logging.getLogger(__name__)

class VoiceInput:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
    def listen_for_command(self):
        """Listen for voice commands"""
        try:
            with self.microphone as source:
                logger.info("Listening for voice command...")
                audio = self.recognizer.listen(source, timeout=5)
                command = self.recognizer.recognize_google(audio)
                logger.info(f"Voice command received: {command}")
                return command
        except Exception as e:
            logger.error(f"Voice input error: {e}")
            return None

class VoiceInputEngine:
    def __init__(self):
        self.router = TaskRouter()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.listening = False
        self.thread = None

    def start_listening(self):
        if self.listening:
            print("[INFO] Voice input already running.")
            return

        print("[INFO] Starting voice recognition...")
        self.listening = True
        self.thread = threading.Thread(target=self._listen_loop)
        self.thread.start()

    def stop_listening(self):
        if not self.listening:
            print("[INFO] Voice input is not running.")
            return
        print("[INFO] Stopping voice recognition...")
        self.listening = False
        if self.thread:
            self.thread.join()

    def _listen_loop(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("[Voice] Listening for commands. Say 'stop listening' to exit.")
            while self.listening:
                try:
                    print("[Voice] Awaiting speech...")
                    audio = self.recognizer.listen(source, timeout=10)
                    command = self.recognizer.recognize_google(audio)
                    print(f"[Voice] You said: {command}")
                    if command.lower() == "stop listening":
                        self.stop_listening()
                        break
                    self._process_command(command)
                except sr.WaitTimeoutError:
                    print("[Voice] Timeout: No speech detected.")
                except sr.UnknownValueError:
                    print("[Voice] Could not understand audio.")
                except sr.RequestError as e:
                    print(f"[Voice] Request error: {e}")

    def _process_command(self, command_text):
        print(f"[Voice] Executing: {command_text}")
        result = self.router.execute_task(command_text)
        print("[Voice] Result:", result)

# Entry point for manual CLI
if __name__ == "__main__":
    engine = VoiceInputEngine()
    engine.start_listening()
