# voice_interface/mic_listener.py
import speech_recognition as sr

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("[VOICE] Listening for command...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"[VOICE] Recognized: {text}")
            return text
        except sr.UnknownValueError:
            print("[VOICE] Could not understand audio.")
        except sr.RequestError:
            print("[VOICE] STT service failed.")
    return None
