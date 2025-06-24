import os
import subprocess

class GitUpdater:
    def __init__(self, repo_url=None):
        self.repo = repo_url

    def init_repo(self):
        os.system("git init")
        print("[GIT] Initialized local repo.")

    def add_remote(self):
        if self.repo:
            os.system(f"git remote add origin {self.repo}")
            print(f"[GIT] Remote added: {self.repo}")

    def commit_push(self, msg="AIOS update"):
        os.system("git add .")
        os.system(f"git commit -m \"{msg}\"")
        os.system("git push origin main")

    def pull_updates(self):
        os.system("git pull origin main")

if __name__ == "__main__":
    updater = GitUpdater("https://github.com/yourusername/ai-os.git")
    updater.init_repo()
    updater.add_remote()
    updater.commit_push("Initial commit")
