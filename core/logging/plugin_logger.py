import json
import os
import time
from datetime import datetime
from uuid import uuid4
from threading import Lock

LOG_DIR = "logs"
JSON_LOG_PATH = os.path.join(LOG_DIR, "plugin_log.jsonl")
TXT_LOG_PATH = os.path.join(LOG_DIR, "plugin_log.txt")
MAX_LOG_SIZE_MB = 10  # Set log rotation limit (optional)


class PluginLogger:
    def __init__(self):
        self.lock = Lock()
        os.makedirs(LOG_DIR, exist_ok=True)

    def log(self, plugin_name, input_code, output, error, success, metadata=None):
        """
        Logs the execution of a plugin.
        """
        timestamp = datetime.utcnow().isoformat()
        log_id = str(uuid4())
        log_entry = {
            "id": log_id,
            "timestamp": timestamp,
            "plugin": plugin_name,
            "input": input_code,
            "output": output,
            "error": error,
            "success": success,
            "metadata": metadata or {},
            "level": "error" if not success else "info"
        }

        try:
            with self.lock:
                self._rotate_logs_if_needed()

                with open(JSON_LOG_PATH, "a", encoding="utf-8") as f_json:
                    f_json.write(json.dumps(log_entry) + "\n")

                with open(TXT_LOG_PATH, "a", encoding="utf-8") as f_txt:
                    f_txt.write(self.format_readable(log_entry))
        except Exception as e:
            print(f"[PluginLogger] Failed to write logs: {e}")

    def format_readable(self, entry):
        """
        Formats a log entry in a human-readable form.
        """
        lines = [
            f"\n--- Plugin Execution Log [{entry['timestamp']}] ---",
            f"ID       : {entry['id']}",
            f"Plugin   : {entry['plugin']}",
            f"Success  : {entry['success']}",
            f"Level    : {entry['level']}",
            f"Input    : {entry['input']}",
            f"Output   : {entry['output']}",
            f"Error    : {entry['error']}",
            f"Metadata : {json.dumps(entry['metadata'], indent=2)}",
            f"------------------------------------------------------\n"
        ]
        return "\n".join(lines)

    def _rotate_logs_if_needed(self):
        """
        Rotates log files if they exceed the defined size limit.
        """
        try:
            if os.path.exists(JSON_LOG_PATH):
                size_mb = os.path.getsize(JSON_LOG_PATH) / (1024 * 1024)
                if size_mb > MAX_LOG_SIZE_MB:
                    timestamp = int(time.time())
                    os.rename(JSON_LOG_PATH, JSON_LOG_PATH.replace(".jsonl", f"_{timestamp}.jsonl"))

            if os.path.exists(TXT_LOG_PATH):
                size_mb = os.path.getsize(TXT_LOG_PATH) / (1024 * 1024)
                if size_mb > MAX_LOG_SIZE_MB:
                    timestamp = int(time.time())
                    os.rename(TXT_LOG_PATH, TXT_LOG_PATH.replace(".txt", f"_{timestamp}.txt"))

        except Exception as e:
            print(f"[PluginLogger] Log rotation failed: {e}")
