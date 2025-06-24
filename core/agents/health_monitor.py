# core/agents/agent_health_monitor.py

import threading
import time
from typing import Dict
from core.agents.agent_profiler import AgentProfiler
from core.logging.plugin_logger import PluginLogger
from core.agents.recovery_manager import RecoveryManager


class AgentHealthMonitor:
    """
    Monitors agents by profiling system resource usage and triggering recovery logic.
    """

    def __init__(self, cpu_threshold: float = 90.0, memory_threshold: float = 100.0):
        """
        Initializes the health monitor.

        Args:
            cpu_threshold (float): CPU usage % beyond which agent recovery is triggered.
            memory_threshold (float): Memory usage in MB beyond which agent recovery is triggered.
        """
        self.watchlist: Dict[str, int] = {}  # agent_id -> pid
        self.cpu_threshold = cpu_threshold
        self.memory_threshold = memory_threshold
        self.logger = PluginLogger()
        self._stop_event = threading.Event()

    def add_agent(self, agent_id: str, pid: int) -> None:
        """
        Add an agent to be monitored.

        Args:
            agent_id (str): Unique identifier of the agent.
            pid (int): Process ID of the agent.
        """
        self.watchlist[agent_id] = pid
        self.logger.log(
            plugin_name="AgentHealthMonitor",
            input_code="add_agent",
            output=f"Agent {agent_id} with PID {pid} added to monitor list.",
            error="",
            success=True,
            metadata={"agent_id": agent_id, "pid": pid}
        )

    def stop(self) -> None:
        """
        Stop the monitoring loop gracefully.
        """
        self._stop_event.set()

    def monitor_loop(self, interval: int = 10) -> None:
        """
        Run the monitoring loop. Profiles agent resource usage and logs stats.

        Args:
            interval (int): Seconds between monitoring checks.
        """
        self.logger.log(
            plugin_name="AgentHealthMonitor",
            input_code="monitor_loop",
            output=f"Monitoring started with interval={interval}s",
            error="",
            success=True,
            metadata={}
        )

        try:
            while not self._stop_event.is_set():
                for agent_id, pid in list(self.watchlist.items()):
                    profiler = AgentProfiler(pid)
                    stats = profiler.profile()

                    if "error" in stats:
                        self.logger.log(
                            plugin_name="AgentProfiler",
                            input_code=f"Health check for PID {pid}",
                            output="",
                            error=stats["error"],
                            success=False,
                            metadata={"agent_id": agent_id, "pid": pid}
                        )
                        continue

                    self.logger.log(
                        plugin_name="AgentProfiler",
                        input_code=f"Health stats for PID {pid}",
                        output=str(stats),
                        error="",
                        success=True,
                        metadata={"agent_id": agent_id, "pid": pid}
                    )

                    if stats["cpu_percent"] > self.cpu_threshold or stats["memory_mb"] > self.memory_threshold:
                        self.logger.log(
                            plugin_name="AgentHealthMonitor",
                            input_code="Threshold breach",
                            output=f"Triggering restart due to high usage. CPU={stats['cpu_percent']}%, Mem={stats['memory_mb']}MB",
                            error="",
                            success=True,
                            metadata={"agent_id": agent_id, "pid": pid}
                        )
                        RecoveryManager.restart_agent(agent_id, pid)

                time.sleep(interval)

        except KeyboardInterrupt:
            self.logger.log(
                plugin_name="AgentHealthMonitor",
                input_code="KeyboardInterrupt",
                output="Monitoring loop interrupted by user.",
                error="",
                success=False,
                metadata={}
            )
        except Exception as e:
            self.logger.log(
                plugin_name="AgentHealthMonitor",
                input_code="monitor_loop_error",
                output="Monitoring loop encountered an error.",
                error=str(e),
                success=False,
                metadata={}
            )
        finally:
            self.logger.log(
                plugin_name="AgentHealthMonitor",
                input_code="monitor_loop_exit",
                output="Monitoring loop exited.",
                error="",
                success=True,
                metadata={}
            )
