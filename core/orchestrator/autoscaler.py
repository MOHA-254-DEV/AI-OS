# File: core/autoscaler/plugin_autoscaler.py

import subprocess
import threading
import time
from typing import List, Dict
from core.orchestrator.load_balancer import LoadBalancer

class PluginAutoscaler:
    def __init__(self, interval: int = 15, cpu_threshold: int = 80, max_instances: int = 5):
        """
        Initializes the autoscaler with load balancer and config thresholds.
        """
        self.interval = interval
        self.cpu_threshold = cpu_threshold
        self.max_instances = max_instances
        self.load_balancer = LoadBalancer()
        self.running = False
        self.thread = None

    def scale(self):
        """
        Continuously checks agent load and spawns clones if overloaded.
        """
        while self.running:
            agents: List[Dict] = self.load_balancer.list_agents()
            overloaded = [agent for agent in agents if agent.get("cpu", 0) > self.cpu_threshold]

            for agent in overloaded:
                instance_count = agent.get("instances", 1)
                if instance_count < self.max_instances:
                    new_id = f"{agent['id']}_clone_{instance_count + 1}"
                    print(f"[Autoscaler] Spawning clone: {new_id}")
                    try:
                        subprocess.Popen(["python", "core/runtime/agent.py", new_id])
                        agent["instances"] = instance_count + 1
                    except Exception as e:
                        print(f"[Autoscaler] Failed to spawn agent {new_id}: {e}")

            time.sleep(self.interval)

    def start(self):
        """
        Starts the autoscaling loop in a daemon thread.
        """
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.scale, daemon=True)
            self.thread.start()
            print("[Autoscaler] Started.")

    def stop(self):
        """
        Gracefully stops the autoscaling loop.
        """
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
            print("[Autoscaler] Stopped.")
