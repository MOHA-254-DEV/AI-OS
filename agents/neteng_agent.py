import os
import platform
import subprocess
import shutil
import sys
from datetime import datetime


class NetworkEngineeringAgent:
    def __init__(self, scripts_dir="scripts"):
        os.makedirs(scripts_dir, exist_ok=True)
        self.scripts_dir = scripts_dir

    def ping_server(self, hostname: str):
        """
        Pings a server using system-native ping command.
        """
        count_flag = "-n" if platform.system() == "Windows" else "-c"
        cmd = ["ping", count_flag, "4", hostname]
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
            return {
                "output": result.stdout.decode(errors="ignore"),
                "status": "success" if result.returncode == 0 else "fail"
            }
        except subprocess.TimeoutExpired:
            return {"status": "error", "error": "Ping request timed out"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def check_usage(self):
        """
        Retrieves system usage stats: disk, CPU load, memory.
        """
        usage = {}
        try:
            usage["disk"] = self._format_disk_usage(shutil.disk_usage("/"))
        except Exception as e:
            usage["disk"] = f"Error retrieving disk usage: {e}"

        try:
            usage["cpu_load"] = os.getloadavg() if hasattr(os, "getloadavg") else "N/A"
        except Exception as e:
            usage["cpu_load"] = f"Error retrieving CPU load: {e}"

        try:
            usage["memory"] = self._get_memory()
        except Exception as e:
            usage["memory"] = f"Error retrieving memory: {e}"

        return usage

    def _format_disk_usage(self, usage):
        return {
            "total_gb": round(usage.total / (1024**3), 2),
            "used_gb": round(usage.used / (1024**3), 2),
            "free_gb": round(usage.free / (1024**3), 2)
        }

    def _get_memory(self):
        if platform.system() == "Linux":
            with open('/proc/meminfo', 'r') as f:
                lines = f.readlines()
            meminfo = {line.split(":")[0]: line.split(":")[1].strip() for line in lines if ":" in line}
            return meminfo
        elif platform.system() == "Windows":
            import psutil
            memory = psutil.virtual_memory()
            return {
                "total_mb": round(memory.total / (1024**2), 2),
                "available_mb": round(memory.available / (1024**2), 2),
                "percent_used": memory.percent
            }
        else:
            return "Memory check not supported on this OS"

    def deploy_script(self, name: str, code: str, lang: str = "bash"):
        """
        Deploy a script to scripts directory with specified language extension.
        """
        extension = "sh" if lang == "bash" else "py"
        script_path = os.path.join(self.scripts_dir, f"{name}.{extension}")
        try:
            with open(script_path, "w") as f:
                f.write(code)
            os.chmod(script_path, 0o755)
            return {"status": "created", "path": script_path}
        except Exception as e:
            return {"status": "error", "error": f"Script deployment failed: {str(e)}"}

    def run_script(self, name: str, lang: str = "bash"):
        """
        Run a deployed script using subprocess.
        """
        extension = "sh" if lang == "bash" else "py"
        script_path = os.path.join(self.scripts_dir, f"{name}.{extension}")
        try:
            if lang == "bash":
                cmd = ["bash", script_path]
            elif lang == "python":
                cmd = [sys.executable, script_path]
            else:
                return {"status": "error", "error": "Unsupported language"}

            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20)
            return {
                "output": result.stdout.decode(errors="ignore"),
                "error": result.stderr.decode(errors="ignore"),
                "status": "success" if result.returncode == 0 else "fail"
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def monitor_logs(self, filepath: str, lines: int = 20):
        """
        Tail the last N lines of a log file.
        """
        try:
            with open(filepath, 'r', encoding="utf-8", errors="ignore") as f:
                content = f.readlines()[-lines:]
            return {"logs": content}
        except FileNotFoundError:
            return {"status": "error", "error": f"Log file not found: {filepath}"}
        except Exception as e:
            return {"status": "error", "error": f"Error reading log: {str(e)}"}
