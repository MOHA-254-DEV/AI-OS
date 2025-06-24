import os
from utils.logger import logger

class DeployEngine:
    def generate_render_yaml(self, filename="render.yaml"):
        try:
            logger.info("Generating Render config...")
            content = """services:
  - type: web
    name: ai-os
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python main.py
    autoDeploy: true
"""
            with open(filename, "w") as f:
                f.write(content)
            logger.info(f"{filename} created successfully.")
            return True
        except Exception as e:
            logger.error(f"Failed to create {filename}: {e}")
            return False

    def generate_replit_config(self, filename=".replit"):
        try:
            logger.info("Generating .replit config...")
            content = """run = "python main.py"
language = "python3"
entrypoint = "main.py"
"""
            with open(filename, "w") as f:
                f.write(content)
            logger.info(f"{filename} created successfully.")
            return True
        except Exception as e:
            logger.error(f"Failed to create {filename}: {e}")
            return False

    def generate_railway_config(self):
        try:
            logger.info("Generating Railway deployment files...")
            os.makedirs("railway", exist_ok=True)
            script_path = "railway/start.sh"
            with open(script_path, "w") as f:
                f.write("#!/bin/bash\npip install -r requirements.txt\npython main.py\n")
            os.chmod(script_path, 0o755)  # Make it executable
            logger.info("Railway deployment script created successfully.")
            return True
        except Exception as e:
            logger.error(f"Failed to create Railway files: {e}")
            return False
