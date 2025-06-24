# File: core/updater/self_updater.py

import subprocess
import os
from utils.logger import logger

class SelfUpdater:
    def __init__(self, repo_url="https://github.com/your-repo/ai-os", branch="main"):
        self.repo_url = repo_url
        self.branch = branch
        self.local_path = os.getcwd()

    def pull_latest(self):
        """
        Pull the latest updates from the remote GitHub repository.
        """
        logger.info(f"🔄 Checking for updates from {self.repo_url} on branch {self.branch}...")
        if not os.path.exists(os.path.join(self.local_path, ".git")):
            logger.warning("🚫 Not a Git repository. Skipping pull.")
            return False

        try:
            result = subprocess.run(
                ["git", "pull", "origin", self.branch],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            logger.info("✅ Update pulled successfully.")
            logger.debug(result.stdout.decode())
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Git pull failed: {e.stderr.decode() if e.stderr else str(e)}")
            return False

    def upgrade_requirements(self, requirements_path="requirements.txt"):
        """
        Install or upgrade Python dependencies from requirements.txt.
        """
        logger.info("📦 Checking for dependency updates...")

        if not os.path.exists(requirements_path):
            logger.warning(f"⚠️ No {requirements_path} file found. Skipping dependency upgrade.")
            return

        try:
            result = subprocess.run(
                ["pip", "install", "--upgrade", "-r", requirements_path],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            logger.info("✅ Dependencies installed/updated successfully.")
            logger.debug(result.stdout.decode())

        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to update dependencies: {e.stderr.decode() if e.stderr else str(e)}")
