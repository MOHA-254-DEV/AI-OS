import platform
import shutil
import os
import json

class ConfigScanner:
    def __init__(self):
        self.config = {}

    def detect_env(self):
        self.config['os'] = platform.system()
        self.config['python_version'] = platform.python_version()
        self.config['node_installed'] = shutil.which("node") is not None
        self.config['git_installed'] = shutil.which("git") is not None
        self.config['docker_installed'] = shutil.which("docker") is not None
        return self.config

    def detect_ports(self):
        self.config['default_port'] = 8000 if self.config['os'] != "Windows" else 5000

    def save_config(self, path="deploy/system_config.json"):
        with open(path, "w") as f:
            json.dump(self.config, f, indent=2)
        print(f"[CONFIG] Saved to {path}")

if __name__ == "__main__":
    scan = ConfigScanner()
    scan.detect_env()
    scan.detect_ports()
    scan.save_config()
    print(json.dumps(scan.config, indent=2))
