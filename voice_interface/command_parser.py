# voice_interface/command_parser.py
def parse_command(transcript: str):
    if "apply to" in transcript.lower():
        platform = "Upwork" if "upwork" in transcript.lower() else "Freelancer"
        return {
            "intent": "apply",
            "platform": platform
        }
    return {
        "intent": "unknown"
    }
