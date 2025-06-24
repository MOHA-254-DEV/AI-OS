# File: core/orchestrator/fault_detector.py

import os
import json
import time
from typing import Dict
from core.orchestrator.healing_rules import HealingRules
from core.orchestrator.orchestrator import AutoHealer
from core.logging.plugin_logger import PluginLogger


class FaultDetector:
    def __init__(self, log_file: str = 'core/logs/fault_events.json'):
        self.log_file = log_file
        self.logger = PluginLogger()
        self.auto_healer = AutoHealer()
        self.last_size = 0

    def listen_for_faults(self, poll_interval: int = 5):
        """
        Continuously listens for fault events and triggers healing logic based on rules.
        """
        print("[FaultDetector] Listening for fault events...")
        while True:
            if not os.path.exists(self.log_file):
                time.sleep(poll_interval)
                continue

            current_size = os.path.getsize(self.log_file)
            if current_size == self.last_size:
                time.sleep(poll_interval)
                continue

            try:
                with open(self.log_file, 'r') as f:
                    lines = f.readlines()[-10:]  # Read last 10 lines
            except Exception as e:
                self.logger.log(
                    plugin_name="FaultDetector",
                    input_code="Reading log file",
                    output="",
                    error=str(e),
                    success=False
                )
                time.sleep(poll_interval)
                continue

            for line in lines:
                self._process_event_line(line)

            self.last_size = current_size
            time.sleep(poll_interval)

    def _process_event_line(self, line: str):
        """
        Processes a single JSON fault line and triggers healing if valid.
        """
        try:
            event: Dict = json.loads(line.strip())
            fault_type = event.get("fault_type")
            agent_id = event.get("agent_id")
            metadata = event.get("metadata", {})

            if not fault_type or not agent_id:
                raise ValueError("Missing fault_type or agent_id in event")

            rule = HealingRules.get_action(fault_type)
            self.logger.log(
                plugin_name="FaultDetector",
                input_code=f"Detected {fault_type} on {agent_id}",
                output=f"Triggering action: {rule['action']}",
                success=True,
                metadata={"severity": rule.get("severity", "unknown"), **metadata}
            )
            self.auto_healer.handle(agent_id, fault_type, rule)

        except Exception as e:
            self.logger.log(
                plugin_name="FaultDetector",
                input_code=line,
                output="",
                error=str(e),
                success=False
            )
