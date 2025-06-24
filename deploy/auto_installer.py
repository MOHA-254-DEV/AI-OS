import subprocess
import sys
import os

class AutoInstaller:
    def pip_install(self, package):
        print(f"[INSTALL] Installing {package}")
        subprocess.call([sys.executable, "-m", "pip", "install", package])

    def check_installations(self):
        packages = ["flask", "transformers", "torch", "python-dotenv"]
        for pkg in packages:
            try:
                __import__(pkg)
                print(f"[CHECK] {pkg} installed.")
            except ImportError:
                self.pip_install(pkg)

    def node_install(self):
        if os.path.exists("package.json"):
            print("[NODE] Installing Node dependencies...")
            os.system("npm install")

if __name__ == "__main__":
    ai = AutoInstaller()
    ai.check_installations()
    ai.node_install()
