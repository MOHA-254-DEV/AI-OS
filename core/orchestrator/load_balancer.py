import json
import os
import time
import random
import threading

class LoadBalancer:
    def __init__(self, agent_status_file='core/data/agent_status.json', ttl=120):
        self.agent_status_file = agent_status_file
        self.last_index = 0
        self.ttl = ttl  # Time-to-live in seconds for stale agents
        self.lock = threading.Lock()

    def _load_agents(self):
        if not os.path.exists(self.agent_status_file):
            return []
        with self.lock, open(self.agent_status_file, 'r') as f:
            try:
                return json.load(f).get("agents", [])
            except json.JSONDecodeError:
                return []

    def _save_agents(self, agents):
        with self.lock, open(self.agent_status_file, 'w') as f:
            json.dump({"agents": agents}, f, indent=2)

    def _cleanup_stale_agents(self, agents):
        now = time.time()
        return [a for a in agents if now - a.get("timestamp", now) <= self.ttl]

    def register_agent(self, agent_id, cpu_usage, memory_usage, task_queue):
        now = time.time()
        agents = self._load_agents()
        existing = next((a for a in agents if a["id"] == agent_id), None)

        if existing:
            existing.update({
                "cpu": cpu_usage,
                "memory": memory_usage,
                "queue": task_queue,
                "timestamp": now
            })
        else:
            agents.append({
                "id": agent_id,
                "cpu": cpu_usage,
                "memory": memory_usage,
                "queue": task_queue,
                "timestamp": now
            })

        agents = self._cleanup_stale_agents(agents)
        self._save_agents(agents)

    def choose_agent(self, strategy="least_loaded"):
        agents = self._cleanup_stale_agents(self._load_agents())
        if not agents:
            raise Exception("❌ No active agents registered")

        if strategy == "round_robin":
            selected = agents[self.last_index % len(agents)]
            self.last_index += 1
            return selected

        elif strategy == "least_loaded":
            return min(agents, key=lambda x: (x["cpu"] + x["memory"]))

        elif strategy == "priority_weighted":
            weights = [100 / (a["cpu"] + a["memory"] + 1) for a in agents]
            return random.choices(agents, weights=weights, k=1)[0]

        else:
            raise ValueError(f"⚠️ Unknown strategy: {strategy}")

    def deregister_agent(self, agent_id):
        agents = self._load_agents()
        agents = [a for a in agents if a["id"] != agent_id]
        self._save_agents(agents)

    def list_agents(self):
        return self._cleanup_stale_agents(self._load_agents())
