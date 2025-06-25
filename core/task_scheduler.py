from utils.logger import logger
from typing import Dict, Any, Callable, Awaitable

class TaskScheduler:
    def __init__(self):
        self.plugins: Dict[str, Callable[..., Awaitable[Any]]] = {}
        self.initialized = False
        logger.info("TaskScheduler initialized")

    async def initialize(self):
        try:
            self.plugins["echo"] = self._echo_plugin
            self.plugins["custom_echo"] = self._custom_echo_plugin
            self.initialized = True
            logger.info("TaskScheduler initialization complete")
        except Exception as e:
            logger.error(f"Failed to initialize TaskScheduler: {e}", exc_info=True)
            raise

    async def handle_command(self, command: str) -> Any:
        if not self.initialized:
            raise RuntimeError("TaskScheduler not initialized")
        parts = command.strip().split()
        if not parts:
            logger.warning("Received empty command.")
            return None
        task_name = parts[0]
        args = parts[1:]
        if task_name not in self.plugins:
            logger.warning(f"Unknown task/plugin: '{task_name}'")
            return f"Unknown command: {task_name}"
        try:
            result = await self.plugins[task_name](*args)
            logger.info(f"Task '{task_name}' executed successfully")
            return result
        except Exception as e:
            logger.error(f"Task '{task_name}' failed: {e}", exc_info=True)
            return f"Error executing '{task_name}': {e}"

    async def run_task(self, task_name: str, *args, **kwargs) -> Any:
        if not self.initialized:
            raise RuntimeError("TaskScheduler not initialized")
        if task_name not in self.plugins:
            raise ValueError(f"Task '{task_name}' not found")
        try:
            result = await self.plugins[task_name](*args, **kwargs)
            logger.info(f"Task '{task_name}' completed successfully")
            return result
        except Exception as e:
            logger.error(f"Task '{task_name}' failed: {e}", exc_info=True)
            raise

    async def shutdown(self):
        logger.info("Shutting down TaskScheduler...")
        self.initialized = False
        logger.info("TaskScheduler shutdown complete.")

    async def _echo_plugin(self, *args) -> str:
        message = " ".join(args)
        return f"Echo: {message}"

    async def _custom_echo_plugin(self, *args) -> str:
        message = " ".join(args)
        return f"Custom Echo: {message.upper()}"
