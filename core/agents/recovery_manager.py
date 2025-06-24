# core/agents/recovery_manager.py

import os
import signal
import time
from subprocess import Popen
from typing import Dict
from core.logging.plugin_logger import PluginLogger
import psutil

class RecoveryManager:
    """
    Manages restart logic for agents. Can terminate and relaunch agents with pre-registered commands.
    """

    agents_config: Dict[str, Dict[str, str]] = {}  # {agent_id: {"cmd": "...", "pid": ...}}

    @staticmethod
    def register_agent(agent_id: str, cmd: str, pid: int) -> None:
        """
        Registers an agent and its execution command for future recovery.

        Args:
            agent_id (str): Unique agent identifier.
            cmd (str): Command used to launch the agent.
            pid (int): Process ID of the running agent.
        """
        RecoveryManager.agents_config[agent_id] = {"cmd": cmd, "pid": pid}

    @staticmethod
    def restart_agent(agent_id: str, pid: int) -> None:
        """
        Restarts a failed or overloaded agent.

        Args:
            agent_id (str): Agent to restart.
            pid (int): Current PID of the agent process.
        """
        logger = PluginLogger()

        try:
            # Validate agent registration
            if agent_id not in RecoveryManager.agents_config:
                logger.log(
                    plugin_name="RecoveryManager",
                    input_code="restart_agent",
                    output="",
                    error=f"Agent '{agent_id}' not registered.",
                    success=False,
                    metadata={"agent_id": agent_id}
                )
                return

            # Attempt graceful termination of the existing agent
            if psutil.pid_exists(pid):
                os.kill(pid, signal.SIGTERM)
                logger.log(
                    plugin_name="RecoveryManager",
                    input_code=f"os.kill(SIGTERM) for PID {pid}",
                    output="Sent termination signal.",
                    error="",
                    success=True,
                    metadata={"agent_id": agent_id}
                )
                time.sleep(2)  # Allow time to shut down

                # Ensure the process actually died
                if psutil.pid_exists(pid):
                    os.kill(pid, signal.SIGKILL)
                    logger.log(
                        plugin_name="RecoveryManager",
                        input_code=f"os.kill(SIGKILL) for PID {pid}",
                        output="Force killed the agent process.",
                        error="",
                        success=True,
                        metadata={"agent_id": agent_id}
                    )

            else:
                logger.log(
                    plugin_name="RecoveryManager",
                    input_code=f"PID {pid} not alive",
                    output="No running process found to kill.",
                    error="",
                    success=True,
                    metadata={"agent_id": agent_id}
                )

            # Relaunch agent
            cmd = RecoveryManager.agents_config[agent_id]["cmd"]
            new_process = Popen(cmd, shell=True)
            new_pid = new_process.pid
            RecoveryManager.agents_config[agent_id]["pid"] = new_pid

            logger.log(
                plugin_name="RecoveryManager",
                input_code=cmd,
                output=f"Restarted agent '{agent_id}' with new PID {new_pid}",
                error="",
                success=True,
                metadata={"agent_id": agent_id}
            )

        except Exception as e:
            logger.log(
                plugin_name="RecoveryManager",
                input_code=f"Restart failure for PID {pid}",
                output="",
                error=str(e),
                success=False,
                metadata={"agent_id": agent_id}
            )
