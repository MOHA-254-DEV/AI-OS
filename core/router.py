# File: core/router/task_router.py

import os
import json
import uuid
from datetime import datetime
from importlib import import_module
from utils.logger import log_task

class TaskRouter:
    def __init__(self, plugin_paths=None, history_path="data/tasks/task_history.json"):
        # List of plugin modules to load commands from
        self.plugin_paths = plugin_paths or [
            "plugins.assistant_plugin",
            "plugins.dropship_plugin",
            "plugins.market_plugin",
            "plugins.dev_plugin",
            "plugins.finance_plugin",
            "plugins.web_plugin",
        ]
        self.plugins = {}  # Command name to function mapping
        self.history_path = history_path

        # Ensure history directory exists
        os.makedirs(os.path.dirname(self.history_path), exist_ok=True)

        # Load all plugins now
        self._load_plugins()

    def _load_plugins(self):
        """
        Load plugin modules and register their commands into the system.
        Each plugin must define a `register()` function that returns a dict:
        e.g., { "deploy_api": deploy_api_function }
        """
        for path in self.plugin_paths:
            try:
                mod = import_module(path)
                registered = mod.register()
                if isinstance(registered, dict):
                    self.plugins.update(registered)
                else:
                    print(f"[WARN] Plugin {path} register() did not return a dict.")
            except Exception as e:
                print(f"[ERROR] Failed to load plugin {path}: {e}")

    def execute_task(self, task_str, user_id="system"):
        """
        Parse and execute a command from a task string like:
        'deploy_api staging'
        """
        task_id = str(uuid.uuid4())
        timestamp = str(datetime.now())
        tokens = task_str.strip().split()

        if not tokens:
            return {"error": "No command provided."}

        command = tokens[0]
        args = tokens[1:]

        if command not in self.plugins:
            return {"error": f"Unknown command: {command}"}

        try:
            func = self.plugins[command]
            result = func(args)

            record = {
                "task_id": task_id,
                "user_id": user_id,
                "timestamp": timestamp,
                "command": command,
                "args": args,
                "result": result,
                "status": "success"
            }
            self._log_task(record)
            return result

        except Exception as e:
            record = {
                "task_id": task_id,
                "user_id": user_id,
                "timestamp": timestamp,
                "command": command,
                "args": args,
                "result": str(e),
                "status": "error"
            }
            self._log_task(record)
            return {"error": str(e)}

    def list_tasks(self, limit=50):
        """
        Return the last `limit` task logs.
        """
        tasks = self._load_history()
        return tasks[-limit:]

    def find_tasks(self, keyword):
        """
        Search task history by command keyword.
        """
        return [t for t in self._load_history() if keyword.lower() in t['command'].lower()]

    def available_commands(self):
        """
        List all currently loaded commands.
        """
        return list(self.plugins.keys())

    def _log_task(self, record):
        """
        Log task to disk and to system logger.
        """
        history = self._load_history()
        history.append(record)

        with open(self.history_path, "w") as f:
            json.dump(history, f, indent=4)

        log_task("router", record["status"], record["command"])

    def _load_history(self):
        """
        Load task history from disk. Return empty list if file doesn't exist or is corrupted.
        """
        if not os.path.exists(self.history_path):
            return []

        try:
            with open(self.history_path, "r") as f:
                return json.load(f)
        except Exception:
            return []
