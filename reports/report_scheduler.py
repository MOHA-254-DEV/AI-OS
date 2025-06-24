import schedule
import time
from reports.report_engine import ReportEngine
from reports.report_renderer import ReportRenderer

class ReportScheduler:
    def __init__(self, data_path, schedule_time="09:00"):
        self.engine = ReportEngine()
        self.renderer = ReportRenderer()
        self.data_path = data_path
        self.schedule_time = schedule_time

    def job(self):
        print("[SCHEDULER] Running scheduled report job...")
        self.engine.load_csv(self.data_path)
        summary = self.engine.analyze_data()
        df = self.engine.get_raw_data()
        self.renderer.render_pdf(df, summary, "scheduled_report")
        self.renderer.render_html(df, summary, "scheduled_report")
        self.renderer.render_chart(df, "scheduled_chart")

    def start(self):
        print(f"[SCHEDULER] Scheduling daily report at {self.schedule_time}")
        schedule.every().day.at(self.schedule_time).do(self.job)
        while True:
            schedule.run_pending()
            time.sleep(60)

if __name__ == "__main__":
    scheduler = ReportScheduler("sample_data.csv", "10:00")
    scheduler.start()
