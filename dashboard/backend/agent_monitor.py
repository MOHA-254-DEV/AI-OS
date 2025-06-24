import json
import os

class AgentMonitor:
    def __init__(self, agent_file='core/data/agent_status.json'):
        self.agent_file = agent_file

    def get_all_agents(self):
        if not os.path.exists(self.agent_file):
            return {"agents": []}
        with open(self.agent_file, 'r') as f:
            return json.load(f)
