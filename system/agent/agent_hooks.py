# system/agent/agent_hooks.py

class AgentHooks:
    def on_start(self, agent_id, agent_type, payload):
        print(f"[AgentHooks] Agent {agent_id} of type {agent_type} is starting with payload: {payload}")

    def on_complete(self, agent_id, result):
        print(f"[AgentHooks] Agent {agent_id} completed task. Result: {result}")

    def on_error(self, agent_id, error):
        print(f"[AgentHooks] Agent {agent_id} encountered an error: {error}")
