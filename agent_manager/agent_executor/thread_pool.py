# agent_executor/thread_pool.py

import threading
import queue
import uuid
import logging
from agent_executor.task_worker import TaskWorker

class ThreadPoolManager:
    def __init__(self, max_threads=5):
        self.max_threads = max_threads
        self.task_queue = queue.Queue()
        self.threads = []
        self.shutdown_event = threading.Event()

        self.logger = logging.getLogger("ThreadPoolManager")
        self.logger.setLevel(logging.INFO)

        for i in range(self.max_threads):
            t = threading.Thread(target=self._worker_loop, name=f"Worker-{i}", daemon=True)
            self.threads.append(t)
            t.start()
            self.logger.info(f"[ThreadPool] Started thread {t.name}")

    def _worker_loop(self):
        while not self.shutdown_event.is_set():
            try:
                task_id, task_fn, args, kwargs, callback = self.task_queue.get(timeout=1)

                self.logger.info(f"[ThreadPool] Executing Task {task_id}")
                worker = TaskWorker(task_id, task_fn, *args, on_complete=callback, **kwargs)
                worker.start()
                worker.join()  # Wait for task to complete

                self.task_queue.task_done()

            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"[ThreadPool] Worker encountered error: {e}", exc_info=True)

    def add_task(self, task_fn, *args, on_complete=None, **kwargs):
        """
        Add a task to the pool.
        :param task_fn: The function to execute
        :param args: Positional args for the function
        :param kwargs: Keyword args for the function
        :param on_complete: Optional callback(task_id, result)
        """
        task_id = str(uuid.uuid4())
        self.task_queue.put((task_id, task_fn, args, kwargs, on_complete))
        self.logger.info(f"[ThreadPool] Task {task_id} added to queue.")

    def wait_for_completion(self):
        """Wait for all enqueued tasks to complete."""
        self.logger.info("[ThreadPool] Waiting for all tasks to finish...")
        self.task_queue.join()
        self.logger.info("[ThreadPool] All tasks completed.")

    def shutdown(self):
        """Signal all threads to terminate and join them."""
        self.logger.info("[ThreadPool] Shutdown initiated...")
        self.shutdown_event.set()
        for t in self.threads:
            t.join()
            self.logger.info(f"[ThreadPool] Thread {t.name} terminated.")
        self.logger.info("[ThreadPool] Shutdown complete.")
