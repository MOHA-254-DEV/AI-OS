import os
import logging
import speech_recognition as sr
from pydub import AudioSegment
from datetime import datetime

# Optional: required for microphone recording
try:
    import sounddevice as sd
    from scipy.io.wavfile import write
    MICROPHONE_ENABLED = True
except ImportError:
    MICROPHONE_ENABLED = False

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class SpeechToText:
    def __init__(self, save_dir="data/audio/recordings"):
        self.recognizer = sr.Recognizer()
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)

    def transcribe_audio_file(self, file_path: str) -> dict:
        """
        Transcribes a WAV audio file to text using Google Speech Recognition API.
        :param file_path: Full path to the WAV audio file.
        :return: Dictionary with transcription or error.
        """
        try:
            with sr.AudioFile(file_path) as source:
                audio_data = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio_data)
                logger.info(f"[OK] Transcribed: {file_path}")
                return {"transcript": text, "source": file_path}
        except sr.UnknownValueError:
            logger.warning(f"[WARN] Unintelligible audio: {file_path}")
            return {"error": "Could not understand audio", "source": file_path}
        except sr.RequestError as e:
            logger.error(f"[ERR] Speech API error: {str(e)}")
            return {"error": f"Speech recognition API error: {str(e)}", "source": file_path}
        except Exception as e:
            logger.error(f"[ERR] Unexpected error during transcription: {str(e)}")
            return {"error": f"Unexpected error: {str(e)}", "source": file_path}

    def transcribe_wav_or_mp3(self, path: str) -> dict:
        """
        Handles transcription for both WAV and MP3 files.
        If MP3, converts to WAV before processing.
        :param path: Full path to audio file (.wav or .mp3)
        :return: Transcription result dict
        """
        if path.endswith(".mp3"):
            try:
                audio = AudioSegment.from_mp3(path)
                wav_path = path.replace(".mp3", ".wav")
                audio.export(wav_path, format="wav")
                logger.info(f"[INFO] Converted {path} to {wav_path}")
                os.remove(path)
                path = wav_path
            except Exception as e:
                logger.error(f"[ERR] MP3 conversion failed: {str(e)}")
                return {"error": f"Failed to convert MP3 to WAV: {str(e)}"}

        return self.transcribe_audio_file(path)

    def record_microphone(self, duration=5, filename=None) -> dict:
        """
        Records audio from the microphone for a specified duration and transcribes it.
        :param duration: Length of recording in seconds
        :param filename: Optional custom filename
        :return: Transcription result
        """
        if not MICROPHONE_ENABLED:
            return {"error": "Microphone recording is not supported (missing dependencies)."}

        filename = filename or f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        file_path = os.path.join(self.save_dir, filename)

        try:
            fs = 44100  # Sample rate
            logger.info(f"[🎙️] Recording {duration}s from microphone...")
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
            sd.wait()

            write(file_path, fs, recording)
            logger.info(f"[✅] Recording saved: {file_path}")
            return self.transcribe_audio_file(file_path)

        except Exception as e:
            logger.error(f"[ERR] Microphone recording failed: {str(e)}")
            return {"error": f"Microphone recording failed: {str(e)}"}

    def cleanup_files(self, *files):
        """
        Deletes specified files if they exist.
        :param files: List of file paths to delete.
        """
        for file in files:
            try:
                if os.path.exists(file):
                    os.remove(file)
                    logger.info(f"[🧹] Deleted: {file}")
            except Exception as e:
                logger.warning(f"[WARN] Failed to delete {file}: {str(e)}")

    def batch_transcribe_folder(self, folder_path: str) -> list:
        """
        Batch transcribes all WAV/MP3 files in a folder.
        :param folder_path: Folder path containing audio files
        :return: List of transcription results
        """
        if not os.path.isdir(folder_path):
            logger.error(f"[ERR] Folder does not exist: {folder_path}")
            return []

        results = []
        for file in os.listdir(folder_path):
            full_path = os.path.join(folder_path, file)
            if file.endswith(".wav") or file.endswith(".mp3"):
                logger.info(f"[📂] Processing: {file}")
                result = self.transcribe_wav_or_mp3(full_path)
                results.append(result)

        return results
