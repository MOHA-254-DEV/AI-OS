# agent_executor/test_executor.py

import random
import time
import logging

from agent_executor.thread_pool import ThreadPoolManager
from agent_executor.performance_balancer import PerformanceBalancer

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

def mock_task(duration, result):
    """Mock task that simulates work."""
    time.sleep(duration)
    return result

def run_test():
    balancer = PerformanceBalancer(threshold_cpu=80)
    pool = ThreadPoolManager(max_threads=3)

    def on_complete(task_id, result):
        print(f"[Callback] ✅ {task_id} finished with result: {result}")

    # Add 6 tasks
    for i in range(6):
        duration = round(random.uniform(1, 3), 2)
        task_id = f"Task-{i}"
        print(f"[Test] Scheduling {task_id} (duration: {duration}s)...")

        # Wait until CPU usage is acceptable
        balancer.wait_until_safe()

        # Add to pool
        pool.add_task(mock_task, duration, f"{task_id}-done", on_complete=on_complete, task_id=task_id)

    # Wait for all to finish
    pool.wait_for_completion()
    print("[Test] 🎉 All tasks completed.")

if __name__ == "__main__":
    run_test()
