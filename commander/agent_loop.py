# core/agent_loop.py

import time
import traceback
import logging
from commander.goal_manager import GoalManager
from commander.decision_engine import DecisionEngine
from orchestrator.scheduler import Scheduler

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class AgentLoop:
    def __init__(self, idle_wait=5, error_wait=2):
        self.goal_manager = GoalManager()
        self.decision_engine = DecisionEngine()
        self.scheduler = Scheduler()
        self.running = False
        self.idle_wait = idle_wait
        self.error_wait = error_wait

    def add_goal(self, description: str, priority: int = 5):
        """
        Add a new goal to the queue.
        """
        return self.goal_manager.add_goal(description, priority)

    def stop(self):
        """
        Stop the agent loop and scheduler.
        """
        logger.info("[AGENT LOOP] Stopping loop.")
        self.running = False
        self.scheduler.stop()

    def run(self):
        """
        Start the main loop for processing autonomous goals.
        """
        logger.info(f"[{self._timestamp()}] [AGENT LOOP] Starting autonomous agent loop...")
        self.running = True

        try:
            self.scheduler.start()

            while self.running:
                try:
                    goal = self.goal_manager.get_next_goal()

                    if not goal:
                        logger.info(f"[{self._timestamp()}] [AGENT LOOP] No goals in queue. Sleeping for {self.idle_wait}s...")
                        time.sleep(self.idle_wait)
                        continue

                    goal_desc = getattr(goal, 'description', str(goal))
                    logger.info(f"[{self._timestamp()}] [AGENT LOOP] Processing goal: {goal_desc}")

                    tasks = self.decision_engine.analyze_goal(goal)

                    if not tasks:
                        logger.warning(f"[{self._timestamp()}] [AGENT LOOP] No tasks generated for goal: {goal_desc}. Skipping.")
                        self.goal_manager.mark_failed(goal)
                        time.sleep(1)
                        continue

                    for task in tasks:
                        self.scheduler.schedule_task(task)

                    self.goal_manager.mark_completed(goal)
                    logger.info(f"[{self._timestamp()}] [AGENT LOOP] Goal completed: {goal_desc}")
                    time.sleep(2)

                except Exception as goal_err:
                    logger.error(f"[{self._timestamp()}] [AGENT LOOP] ⚠️ Error during goal processing:\n{traceback.format_exc()}")
                    time.sleep(self.error_wait)

        except KeyboardInterrupt:
            logger.warning(f"[{self._timestamp()}] [AGENT LOOP] KeyboardInterrupt received. Exiting gracefully.")
            self.stop()

    def _timestamp(self):
        return time.strftime("%Y-%m-%d %H:%M:%S")
