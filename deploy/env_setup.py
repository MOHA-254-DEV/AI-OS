import os
import json

class EnvSetup:
    def __init__(self):
        self.env_path = ".env"
        self.default_vars = {
            "ENV": "production",
            "PORT": "7860",
            "OPENAI_API_KEY": "",
            "DEPLOY_ENV": "replit"
        }

    def generate_env(self):
        with open(self.env_path, "w") as f:
            for key, value in self.default_vars.items():
                f.write(f"{key}={value}\n")
        print(f"[ENV] .env file created at {self.env_path}")

    def generate_requirements(self):
        deps = [
            "flask", "requests", "beautifulsoup4", "cryptography",
            "python-dotenv", "transformers", "torch", "schedule"
        ]
        with open("requirements.txt", "w") as f:
            f.write("\n".join(deps))
        print("[ENV] requirements.txt created.")

    def generate_procfile(self):
        with open("Procfile", "w") as f:
            f.write("web: python app.py\n")
        print("[ENV] Procfile created.")

    def run_all(self):
        self.generate_env()
        self.generate_requirements()
        self.generate_procfile()

if __name__ == "__main__":
    EnvSetup().run_all()
