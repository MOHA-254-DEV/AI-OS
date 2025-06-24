import os

class CommandRouter:
    def __init__(self):
        self.handlers = {
            "task:browser_open": self.open_browser,
            "task:web_search": self.web_search,
            "task:design_init": self.start_design,
            "task:auto_apply": self.apply_jobs,
            "task:data_analysis": self.analyze_data,
            "task:report_gen": self.generate_report,
            "task:deploy_self": self.deploy_system,
            "task:unknown": self.unknown_command
        }

    def route(self, command: str):
        handler = self.handlers.get(command, self.unknown_command)
        handler()

    def open_browser(self):
        print("[ACTION] Opening secure browser...")
        os.system("python modules/browser.py")

    def web_search(self):
        print("[ACTION] Performing web search...")
        os.system("python modules/search_engine.py")

    def start_design(self):
        print("[ACTION] Starting design task...")
        os.system("python modules/graphic_studio.py")

    def apply_jobs(self):
        print("[ACTION] Applying to jobs...")
        os.system("python jobs/auto_apply.py")

    def analyze_data(self):
        print("[ACTION] Analyzing data set...")
        os.system("python modules/data_engine.py")

    def generate_report(self):
        print("[ACTION] Generating report...")
        os.system("python modules/report_builder.py")

    def deploy_system(self):
        print("[ACTION] Deploying system...")
        os.system("python deploy/deploy_replit.py")

    def unknown_command(self):
        print("[ERROR] Unrecognized voice command.")

if __name__ == "__main__":
    router = CommandRouter()
    router.route("task:report_gen")
    def generate_report(self):
        print("[ACTION] Generating AI report...")
        os.system("python reports/report_engine.py")
        os.system("python reports/report_renderer.py")
