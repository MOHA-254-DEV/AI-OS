import asyncio
from utils.logger import logger

try:
    import speech_recognition as sr
    VOICE_ENABLED = True
except ImportError:
    VOICE_ENABLED = False
    logger.warning("Speech recognition not available - voice features disabled")

class VoiceHandler:
    def __init__(self):
        if VOICE_ENABLED:
            self.recognizer = sr.Recognizer()
            try:
                self.microphone = sr.Microphone()
            except:
                self.microphone = None
                logger.warning("No microphone detected - voice input disabled")
        else:
            self.recognizer = None
            self.microphone = None

    async def initialize(self):
        logger.info("Initializing voice input handler...")
        if not VOICE_ENABLED or not self.microphone:
            logger.info("Voice input not available - running in text-only mode")
            return
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
        except Exception as e:
            logger.error(f"Voice initialization failed: {e}")

    async def listen_for_command(self):
        if not VOICE_ENABLED or not self.microphone:
            return None
            
        logger.info("Listening for voice input...")
        try:
            with self.microphone as source:
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
