import asyncio
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class TaskScheduler:
    def __init__(self):
        self.plugins = {}
        self.initialized = False
        logger.info("TaskScheduler initialized")

    async def initialize(self):
        """Initialize the task scheduler"""
        try:
            # Load default plugins
            self.plugins["echo"] = self._echo_plugin
            self.plugins["custom_echo"] = self._custom_echo_plugin
            self.initialized = True
            logger.info("TaskScheduler initialization complete")
        except Exception as e:
            logger.error(f"Failed to initialize TaskScheduler: {e}")
            raise

    async def run_task(self, task_name: str, *args, **kwargs) -> Any:
        """Run a specific task"""
        if not self.initialized:
            raise RuntimeError("TaskScheduler not initialized")

        if task_name not in self.plugins:
            raise ValueError(f"Task '{task_name}' not found")

        try:
            result = await self.plugins[task_name](*args, **kwargs)
            logger.info(f"Task '{task_name}' completed successfully")
            return result
        except Exception as e:
            logger.error(f"Task '{task_name}' failed: {e}")
            raise

    async def _echo_plugin(self, message: str) -> str:
        """Default echo plugin"""
        return f"Echo: {message}"

    async def _custom_echo_plugin(self, message: str) -> str:
        """Custom echo plugin"""
        return f"Custom Echo: {message.upper()}"