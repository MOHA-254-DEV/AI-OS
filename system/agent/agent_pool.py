# system/agent/agent_pool.py

from collections import defaultdict

class DummyAgent:
    def __init__(self, agent_id):
        self.agent_id = agent_id

    def execute(self, task_payload):
        print(f"[DummyAgent {self.agent_id}] Executing task with payload: {task_payload}")
        return {"status": "success", "output": f"Result from agent {self.agent_id}"}

class AgentPool:
    def __init__(self):
        self.pool = defaultdict(dict)

    def get_or_create(self, agent_type: str, agent_id: str):
        if agent_id in self.pool[agent_type]:
            return self.pool[agent_type][agent_id]
        else:
            print(f"[AgentPool] Creating new agent instance: {agent_id}")
            agent = DummyAgent(agent_id)
            self.pool[agent_type][agent_id] = agent
            return agent

    def recycle(self, agent_id: str):
        print(f"[AgentPool] Recycling agent {agent_id}")
        for agent_type in self.pool:
            if agent_id in self.pool[agent_type]:
                del self.pool[agent_type][agent_id]
                break

    def remove(self, agent_id: str):
        print(f"[AgentPool] Removing agent {agent_id} from pool")
        for agent_type in self.pool:
            if agent_id in self.pool[agent_type]:
                del self.pool[agent_type][agent_id]
                return
