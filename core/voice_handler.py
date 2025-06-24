import speech_recognition as sr
import asyncio
from utils.logger import logger

class VoiceHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    async def initialize(self):
        logger.info("Initializing voice input handler...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

    async def listen_for_command(self):
        logger.info("Listening for voice input...")
        with self.microphone as source:
            try:
                audio = self.recognizer.listen(source, timeout=5)
                command = self.recognizer.recognize_google(audio)
                return command.lower()
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                logger.warning("Voice not recognized.")
                return None
            except Exception as e:
                logger.error(f"Voice handler error: {e}")
                return None
