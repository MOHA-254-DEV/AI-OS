from ai.speech_input import SpeechToText
from ai.planner import Planner
from utils.logger import log_task

speech = SpeechToText()
planner = Planner()

async def transcribe_audio(args):
    if not args:
        return {"error": "Usage: transcribe_audio <audio_file.wav/mp3>"}
    file_path = " ".join(args)
    result = speech.transcribe_wav_or_mp3(file_path)
    log_task("transcribe_audio", "transcribed", str(result))
    return result

async def record_voice(args):
    duration = int(args[0]) if args else 5
    result = speech.record_microphone(duration)
    log_task("record_voice", "recorded", str(result))
    return result

async def voice_to_task(args):
    duration = int(args[0]) if args else 5
    transcript_result = speech.record_microphone(duration)
    if "transcript" not in transcript_result:
        return transcript_result
    result = planner.plan_from_prompt(transcript_result["transcript"])
    log_task("voice_to_task", "planned", str(result))
    return result

def register():
    return {
        "transcribe_audio": transcribe_audio,
        "record_voice": record_voice,
        "voice_to_task": voice_to_task
    }
