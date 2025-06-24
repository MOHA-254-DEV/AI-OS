# agent_coordinator/test_coordinator.py

import unittest
import time
import logging
from agent_coordinator.agent_registry import AgentRegistry
from agent_coordinator.load_balancer import LoadBalancer
from agent_coordinator.agent_manager import AgentManager

# Configure logging (optional)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("TestAgentCoordinator")

class TestAgentCoordinator(unittest.TestCase):

    def test_task_assignment_and_completion(self):
        logger.info("Starting Agent Coordinator Test...")

        # Step 1: Setup system
        registry = AgentRegistry()
        load_balancer = LoadBalancer(registry)
        manager = AgentManager(registry, load_balancer)

        # Step 2: Register agents
        alpha_id = registry.register_agent("AI-Bot-Alpha", ["design", "code"])
        beta_id = registry.register_agent("AI-Bot-Beta", ["marketing", "code"])
        gamma_id = registry.register_agent("AI-Bot-Gamma", ["data", "code", "finance"])

        self.assertIsNotNone(alpha_id)
        self.assertIsNotNone(beta_id)
        self.assertIsNotNone(gamma_id)

        # Step 3: Assign tasks
        manager.assign_task("Web App Development", "code", task_duration=3)
        manager.assign_task("Design Banner", "design", task_duration=2)
        manager.assign_task("Financial Report", "finance", task_duration=2.5)
        manager.assign_task("SEO Audit", "marketing", task_duration=2)

        # Wait a bit longer than the max task duration to allow all to complete
        time.sleep(4)

        # Step 4: Validate post-task state
        all_agents = registry.get_all_agents()
        self.assertEqual(len(all_agents), 3, "There should be 3 agents registered.")

        for agent in all_agents:
            with self.subTest(agent=agent.name):
                logger.info(f"Checking agent {agent.name} (ID: {agent.id})...")
                self.assertEqual(agent.status, "idle", f"{agent.name} should be idle after tasks complete.")
                self.assertEqual(agent.load, 0, f"{agent.name} should have load = 0 after tasks complete.")

        # Step 5: Shutdown manager to release thread pool
        manager.shutdown()
        logger.info("Agent Coordinator Test Completed Successfully.")

if __name__ == "__main__":
    unittest.main()
