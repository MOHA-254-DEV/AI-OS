import speech_recognition as sr

class STTEngine:
    def __init__(self, recognizer=None):
        self.recognizer = recognizer or sr.Recognizer()
        self.microphone = sr.Microphone()

    def listen(self, timeout=5):
        print("[STT] Listening for voice command...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source, timeout=timeout)
        return self.recognize(audio)

    def recognize(self, audio):
        try:
            text = self.recognizer.recognize_google(audio)
            print(f"[STT] Recognized: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("[STT] Could not understand audio.")
            return ""
        except sr.RequestError as e:
            print(f"[STT] Request error: {e}")
            return ""

if __name__ == "__main__":
    stt = STTEngine()
    print(stt.listen())
