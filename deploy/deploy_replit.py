import os
import shutil

class ReplitDeployer:
    def __init__(self):
        self.files_to_copy = ["requirements.txt", "Procfile", ".env", "app.py"]

    def setup(self):
        os.makedirs(".replit", exist_ok=True)
        with open(".replit/main.sh", "w") as f:
            f.write("python3 app.py")
        print("[REPLIT] Main entry created.")

    def copy_files(self):
        for file in self.files_to_copy:
            if os.path.exists(file):
                shutil.copy(file, f"./.replit/{file}")
        print("[REPLIT] Copied config files.")

    def deploy(self):
        self.setup()
        self.copy_files()
        print("[REPLIT] Project ready to import to Replit.")

if __name__ == "__main__":
    deployer = ReplitDeployer()
    deployer.deploy()
