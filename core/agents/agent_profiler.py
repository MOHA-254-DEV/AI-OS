# core/agent_profiling/agent_profiler.py

import psutil
import time
import logging
from typing import Dict, Union

# Configure logger
logger = logging.getLogger("AgentProfiler")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

class AgentProfiler:
    """
    Monitors system resource usage of a given process using its PID.
    Provides CPU, memory, and I/O metrics in real time.
    """

    def __init__(self, pid: int):
        """
        Initialize the profiler for a specific process.

        Args:
            pid (int): The process ID to profile.
        """
        self.pid = pid
        try:
            self.process = psutil.Process(pid)
            logger.info(f"[AgentProfiler] Initialized for PID {pid}")
        except psutil.NoSuchProcess as e:
            logger.error(f"[AgentProfiler] No such process with PID {pid}: {e}")
            raise
        except Exception as e:
            logger.exception(f"[AgentProfiler] Unexpected error during initialization: {e}")
            raise

    def profile(self) -> Dict[str, Union[float, int, str]]:
        """
        Collect CPU, memory, and I/O usage for the process.

        Returns:
            Dict[str, Union[float, int, str]]: Profiling data or error details.
        """
        try:
            cpu_percent = self.process.cpu_percent(interval=1.0)
            memory_rss = self.process.memory_info().rss / (1024 * 1024)  # in MB
            io_counters = self.process.io_counters()

            result = {
                "cpu_percent": round(cpu_percent, 2),
                "memory_mb": round(memory_rss, 2),
                "read_bytes": io_counters.read_bytes,
                "write_bytes": io_counters.write_bytes,
                "timestamp": round(time.time(), 2)
            }

            logger.debug(f"[AgentProfiler] Profiled PID {self.pid}: {result}")
            return result

        except psutil.NoSuchProcess:
            error_msg = f"Process {self.pid} no longer exists."
        except psutil.AccessDenied:
            error_msg = f"Access denied to process {self.pid}."
        except psutil.ZombieProcess:
            error_msg = f"Process {self.pid} is a zombie."
        except Exception as e:
            error_msg = f"Unexpected error profiling process {self.pid}: {e}"
        logger.warning(f"[AgentProfiler] {error_msg}")
        return {
            "error": error_msg,
            "timestamp": round(time.time(), 2)
        }
