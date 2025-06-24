# commander/decision_engine.py

import traceback
import logging
from orchestrator.task_model import AITask
from plugin_runtime.registry import PluginRegistry

# Logger setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class DecisionEngine:
    def __init__(self):
        self.registry = PluginRegistry()

    def analyze_goal(self, goal):
        """
        Analyze a goal and return a list of AITasks to execute.
        """
        if not goal:
            logger.warning("[DECISION ENGINE] No goal provided to analyze.")
            return []

        try:
            goal_desc = getattr(goal, "description", str(goal))
            goal_priority = getattr(goal, "priority", 5)

            logger.info(f"[DECISION ENGINE] 🔍 Analyzing goal: '{goal_desc}'")

            plugins = self.registry.find_plugins_for_goal(goal_desc)

            if not plugins:
                logger.warning(f"[DECISION ENGINE] No matching plugins found for goal: '{goal_desc}'")
                return []

            logger.info(f"[DECISION ENGINE] ✅ Found {len(plugins)} plugin(s) for goal: '{goal_desc}'")

            tasks = []
            for plugin in plugins:
                try:
                    task = AITask(
                        plugin=plugin,
                        args={"goal": goal_desc},
                        priority=goal_priority
                    )
                    tasks.append(task)
                    logger.info(f"[DECISION ENGINE] 🧠 Task created for plugin: {getattr(plugin, 'name', str(plugin))}")
                except Exception as task_err:
                    logger.error(f"[DECISION ENGINE] ⚠️ Failed to create task for plugin '{plugin}':\n{traceback.format_exc()}")

            return tasks

        except Exception as e:
            logger.error(f"[DECISION ENGINE] ❌ Unexpected error during goal analysis:\n{traceback.format_exc()}")
            return []
