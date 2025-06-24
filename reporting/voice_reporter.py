from voice_engine.stt_engine import STTEngine
from voice_engine.nlp_parser import NLPParser
from reporting.report_engine import ReportEngine
from reporting.html_generator import generate_html
from reporting.pdf_exporter import export_to_pdf

class VoiceReporter:
    def __init__(self):
        self.stt = STTEngine()
        self.nlp = NLPParser()
        self.engine = ReportEngine()

        self.engine.add_data_source("system_status", lambda: {"cpu": "35%", "ram": "2.1GB used"})
        self.engine.add_data_source("jobs_today", lambda: {"tasks": ["data entry", "deploy"], "completed": 2})

    def listen_and_generate(self):
        print("[REPORTER] Say: 'generate report' or similar...")
        voice = self.stt.listen()
        intent = self.nlp.parse_command(voice)
        if intent == "analytics":
            data = self.engine.collect_data()
            self.engine.to_json(data)
            generate_html(data)
            export_to_pdf()
            print("[REPORTER] Full report generated and saved.")
        else:
            print("[REPORTER] No matching reporting command.")

if __name__ == "__main__":
    VoiceReporter().listen_and_generate()
