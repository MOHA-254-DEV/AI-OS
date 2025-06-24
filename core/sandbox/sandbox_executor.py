# File: core/sandbox/executor.py

import subprocess
import os
import tempfile
import shutil
import uuid
import json
import sys
from core.sandbox.limits import set_limits

class SandboxExecutor:
    def __init__(self, config_path="core/sandbox/sandbox_config.json"):
        self.config_path = config_path
        self._load_config()

    def _load_config(self):
        default_config = {
            "max_cpu_seconds": 2,
            "max_memory_mb": 128,
            "max_runtime": 5,
            "use_docker": False,
            "docker_image": "python:3.11-slim"
        }
        if not os.path.exists(self.config_path):
            self.config = default_config
            with open(self.config_path, 'w') as f:
                json.dump(default_config, f, indent=2)
        else:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)

    def _write_temp_script(self, code_str):
        temp_dir = tempfile.mkdtemp(prefix="sandbox_")
        script_path = os.path.join(temp_dir, "plugin.py")
        with open(script_path, 'w') as f:
            f.write(code_str)
        return temp_dir, script_path

    def _run_with_subprocess(self, script_path):
        try:
            return subprocess.run(
                [sys.executable, script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=self.config["max_runtime"],
                preexec_fn=lambda: set_limits(
                    self.config["max_cpu_seconds"],
                    self.config["max_memory_mb"]
                )
            )
        except subprocess.TimeoutExpired as e:
            raise TimeoutError("Execution exceeded time limit") from e

    def _run_with_docker(self, script_path):
        container_name = f"sandbox_{uuid.uuid4().hex[:8]}"
        cmd = [
            "docker", "run", "--rm",
            "--name", container_name,
            "--memory", f"{self.config['max_memory_mb']}m",
            "--cpus", "0.5",
            "-v", f"{os.path.dirname(script_path)}:/sandbox:ro",
            "-w", "/sandbox",
            self.config["docker_image"],
            "python", "plugin.py"
        ]
        try:
            return subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=self.config["max_runtime"]
            )
        except subprocess.TimeoutExpired as e:
            raise TimeoutError("Docker execution timeout") from e

    def execute(self, plugin_code: str) -> dict:
        temp_dir, script_path = self._write_temp_script(plugin_code)
        try:
            result = (self._run_with_docker(script_path)
                      if self.config.get("use_docker")
                      else self._run_with_subprocess(script_path))

            return {
                "success": result.returncode == 0,
                "output": result.stdout.decode().strip(),
                "error": result.stderr.decode().strip()
            }

        except TimeoutError as e:
            return {
                "success": False,
                "output": "",
                "error": f"⏱️ {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": f"❌ Execution failed: {str(e)}"
            }
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
