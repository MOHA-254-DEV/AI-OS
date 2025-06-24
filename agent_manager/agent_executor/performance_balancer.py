# agent_executor/performance_balancer.py

import psutil
import time
import logging
from typing import Callable, Optional


class PerformanceBalancer:
    def __init__(
        self,
        threshold_cpu: float = 75.0,
        check_interval: float = 1.0,
        wait_interval: float = 2.0,
        on_wait: Optional[Callable[[], None]] = None
    ):
        """
        Initialize the PerformanceBalancer.

        :param threshold_cpu: Max allowed CPU usage % before blocking tasks.
        :param check_interval: Time (seconds) to measure CPU load.
        :param wait_interval: Time to sleep while overloaded.
        :param on_wait: Optional callback called when waiting (e.g. for UI update).
        """
        self.threshold_cpu = threshold_cpu
        self.check_interval = check_interval
        self.wait_interval = wait_interval
        self.on_wait = on_wait

        # Setup logging
        self.logger = logging.getLogger("PerformanceBalancer")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        # Warm up CPU stats to prevent inaccurate first reading
        psutil.cpu_percent(interval=None)

    def is_under_load(self) -> bool:
        """
        Check current CPU load.
        :return: True if CPU is below the threshold.
        """
        usage = psutil.cpu_percent(interval=self.check_interval)
        self.logger.info(f"CPU Usage: {usage:.2f}%")
        return usage < self.threshold_cpu

    def wait_until_safe(self, max_wait_time: float = 60.0):
        """
        Block until CPU usage falls below threshold or timeout.

        :param max_wait_time: Maximum time (in seconds) to wait before aborting.
        :raises TimeoutError: If system doesn't stabilize within max_wait_time.
        """
        start_time = time.time()
        while not self.is_under_load():
            elapsed = time.time() - start_time
            if elapsed >= max_wait_time:
                raise TimeoutError("System did not recover from high load in time.")

            self.logger.warning("⚠️ System under heavy load. Waiting to proceed...")
            if self.on_wait:
                try:
                    self.on_wait()
                except Exception as e:
                    self.logger.error(f"on_wait callback error: {e}")
            time.sleep(self.wait_interval)
