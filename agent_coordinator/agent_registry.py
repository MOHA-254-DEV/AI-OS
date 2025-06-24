import uuid
import threading
import logging

# Setup logging for traceability
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Agent:
    def __init__(self, name, skills):
        self.id = str(uuid.uuid4())
        self.name = name
        self.skills = set(skills)  # Ensures no duplicates
        self.status = "idle"  # Can be "idle", "busy", etc.
        self.load = 0  # Number of tasks currently being handled


class AgentRegistry:
    def __init__(self):
        self.agents = {}
        self.lock = threading.Lock()

    def register_agent(self, name, skills):
        """
        Register a new agent with name and skills.
        Returns the unique ID of the registered agent.
        """
        agent = Agent(name, skills)
        with self.lock:
            if any(a.name == name for a in self.agents.values()):
                logger.warning(f"[Registry] Agent with name '{name}' already exists.")
            self.agents[agent.id] = agent
        logger.info(f"[Registry] Registered Agent: {agent.name} (ID: {agent.id})")
        return agent.id

    def update_status(self, agent_id, status, load=None):
        """
        Update the status and optionally the load of an agent.
        """
        with self.lock:
            agent = self.agents.get(agent_id)
            if agent:
                agent.status = status
                if load is not None:
                    agent.load = max(0, load)
                logger.info(f"[Registry] Updated Agent {agent.name} (ID: {agent.id}) -> status={status}, load={agent.load}")
            else:
                logger.warning(f"[Registry] Attempted to update unknown agent ID: {agent_id}")

    def get_available_agents(self):
        """
        Retrieve a list of agents currently marked as idle.
        """
        with self.lock:
            available = [agent for agent in self.agents.values() if agent.status == "idle"]
        logger.info(f"[Registry] Found {len(available)} available agent(s).")
        return list(available)  # Return a safe copy

    def get_all_agents(self):
        """
        Get a list of all registered agents.
        """
        with self.lock:
            all_agents = list(self.agents.values())
        logger.info(f"[Registry] Total registered agents: {len(all_agents)}")
        return all_agents

    def get_agent_by_id(self, agent_id):
        """
        Retrieve a single agent by their unique ID.
        """
        with self.lock:
            agent = self.agents.get(agent_id)
        if agent:
            return agent
        logger.warning(f"[Registry] Agent ID {agent_id} not found.")
        return None


# Optional test usage
if __name__ == "__main__":
    registry = AgentRegistry()

    # Register agents
    id1 = registry.register_agent("Agent-Alpha", ["design", "coding"])
    id2 = registry.register_agent("Agent-Beta", ["coding", "testing"])

    # View available agents
    available = registry.get_available_agents()
    logger.info(f"Available agents: {[a.name for a in available]}")

    # Update one agent's status
    registry.update_status(id1, "busy", load=1)

    # List all agents
    for a in registry.get_all_agents():
        logger.info(f"Agent {a.name} | ID: {a.id} | Status: {a.status} | Load: {a.load}")
