# agent_executor/task_worker.py

import threading
import logging
from typing import Callable, Optional, Any


class TaskWorker(threading.Thread):
    def __init__(
        self,
        task_id: str,
        task_fn: Callable,
        *args,
        on_complete: Optional[Callable[[str, Any], None]] = None,
        **kwargs
    ):
        """
        Threaded task executor.

        :param task_id: Unique task identifier.
        :param task_fn: Callable function to execute.
        :param args: Positional arguments for the task function.
        :param kwargs: Keyword arguments for the task function.
        :param on_complete: Optional callback with signature (task_id, result).
        """
        super().__init__(daemon=True)
        self.task_id = task_id
        self.task_fn = task_fn
        self.args = args
        self.kwargs = kwargs
        self.on_complete = on_complete

        self.result = None
        self.exception = None
        self.success = False

        self.logger = logging.getLogger(f"TaskWorker-{self.task_id}")
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False  # Prevent duplicate logs

        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def run(self):
        self.logger.info("🚀 Starting task...")
        try:
            self.result = self.task_fn(*self.args, **self.kwargs)
            self.success = True
            self.logger.info(f"✅ Task completed successfully. Result: {self.result}")

            if self.on_complete:
                try:
                    self.on_complete(self.task_id, self.result)
                except Exception as cb_error:
                    self.logger.error(f"⚠️ on_complete callback error: {cb_error}")

        except Exception as e:
            self.exception = e
            self.success = False
            self.logger.error(f"❌ Task failed with error: {e}", exc_info=True)
