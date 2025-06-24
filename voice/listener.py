import speech_recognition as sr
import whisper
import os

class VoiceListener:
    def __init__(self, model_name="base"):
        self.recognizer = sr.Recognizer()
        self.model = whisper.load_model(model_name)
        self.audio_path = "voice/input.wav"

    def record(self, duration=5):
        with sr.Microphone() as source:
            print("[VOICE] Listening...")
            audio = self.recognizer.record(source, duration=duration)
            with open(self.audio_path, "wb") as f:
                f.write(audio.get_wav_data())
        print("[VOICE] Recording complete.")

    def transcribe(self):
        print("[VOICE] Transcribing...")
        result = self.model.transcribe(self.audio_path)
        return result['text']

    def listen_and_transcribe(self, duration=5):
        self.record(duration)
        return self.transcribe()

if __name__ == "__main__":
    listener = VoiceListener()
    command = listener.listen_and_transcribe(5)
    print("You said:", command)
