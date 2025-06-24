# voice_interface/voice_application_controller.py
from mic_listener import listen_command
from command_parser import parse_command
from auto_application.application_engine import auto_apply

def start_voice_loop(applicant_data):
    print("[AI VOICE] Start talking. Say 'apply to Upwork' or similar.")

    while True:
        transcript = listen_command()
        if transcript:
            parsed = parse_command(transcript)

            if parsed["intent"] == "apply":
                job = {
                    "title": "React Developer",
                    "platform": parsed["platform"],
                    "url": f"https://{parsed['platform'].lower()}.com/job/sample"
                }
                result = auto_apply(job, applicant_data)
                print("[AI VOICE] Application sent:", result)
            else:
                print("[AI VOICE] No actionable command detected.")
