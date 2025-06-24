# agent_manager/run_agents.py

import logging
from agent_manager.agent_core import Agent
from agent_manager.plugin_loader import load_plugins
from agent_manager.agent_registry import AgentRegistry
from agent_manager.task_delegator import TaskDelegator

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')
logger = logging.getLogger("RunAgents")

def initialize_agents():
    """Load plugins and register corresponding agents."""
    logger.info("🔄 Loading plugins...")
    plugins = load_plugins()

    if not plugins:
        logger.warning("⚠️ No plugins loaded. Exiting...")
        return None, None

    registry = AgentRegistry()
    for plugin_name, plugin_instance in plugins.items():
        agent_name = plugin_name.split('_')[0].capitalize()
        agent = Agent(agent_name, plugin_instance)
        registry.register(agent_name, agent)

    logger.info(f"✅ Registered {len(plugins)} agents.")
    return registry, plugins

def simulate_task_queue():
    """Simulates a queue of incoming tasks."""
    return [
        {"type": "design", "data": {"type": "logo", "payload": {"brand": "OpenAI"}}},
        {"type": "marketing", "data": {"campaign_type": "seo", "payload": {"url": "https://openai.com"}}},
        {"type": "nonexistent", "data": "This task type does not exist"}
    ]

def main():
    registry, plugins = initialize_agents()
    if registry is None:
        return

    delegator = TaskDelegator(registry)
    tasks = simulate_task_queue()

    logger.info("🚀 Delegating tasks...")
    for task in tasks:
        try:
            result = delegator.delegate(task)
            logger.info(f"[RESULT] {result}")
        except KeyError:
            logger.error(f"[ERROR] No agent found for task type: {task['type']}")
        except Exception as e:
            logger.exception(f"[ERROR] Failed to process task: {e}")

if __name__ == "__main__":
    main()
