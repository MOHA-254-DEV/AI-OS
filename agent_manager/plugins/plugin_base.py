# agent_manager/plugins/plugin_base.py

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict


class PluginBase(ABC):
    """
    Abstract base class for all plugins in the AI OS.
    Ensures a consistent structure and logging behavior.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)

        if not self.logger.handlers:
            stream_handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s')
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)

    def initialize(self) -> None:
        """
        Optional initialization hook for any resource allocation or setup
        logic that should be run when the plugin is loaded.
        """
        self.logger.debug("Initializing plugin resources...")

    @abstractmethod
    def run(self, task_data: Dict[str, Any]) -> Any:
        """
        Abstract method to execute the plugin's logic.
        Every subclass must implement this method.

        :param task_data: A dictionary containing task-specific input.
        :return: The result of the task execution.
        """
        raise NotImplementedError(f"{self.__class__.__name__} must implement the run() method.")

    def log_task_start(self, task_name: str) -> None:
        """
        Logs the beginning of a task.

        :param task_name: Name or ID of the task.
        """
        self.logger.info(f"🚀 Starting task: {task_name}")

    def log_task_end(self, task_name: str, success: bool = True) -> None:
        """
        Logs the result of a task.

        :param task_name: Name or ID of the task.
        :param success: Boolean indicating if the task succeeded.
        """
        status = "✅ completed successfully" if success else "❌ failed"
        self.logger.info(f"🏁 Task '{task_name}' {status}")

    def handle_error(self, error_message: str) -> None:
        """
        Logs an error that occurred during execution.

        :param error_message: A description of the error.
        """
        self.logger.error(f"⚠️ Error occurred: {error_message}")
