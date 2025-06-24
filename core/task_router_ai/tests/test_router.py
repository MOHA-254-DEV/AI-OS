# /core/task_router_ai/tests/test_router.py

import unittest
from core.task_router_ai.history_db import AgentHistoryDB
from core.task_router_ai.agent_profile import AgentProfile
from core.task_router_ai.predictor import AgentBehaviorPredictor
from core.task_router_ai.router import TaskRouter

class TestTaskRouter(unittest.TestCase):

    def setUp(self):
        # Set up historical data
        self.db = AgentHistoryDB()
        self.db.record_task_result("agent-A", "translate", True, 4.2)
        self.db.record_task_result("agent-A", "translate", True, 4.0)
        self.db.record_task_result("agent-B", "translate", False, 8.0)
        self.db.record_task_result("agent-B", "translate", True, 6.5)

        self.profile = AgentProfile(self.db)
        self.predictor = AgentBehaviorPredictor(self.profile)
        self.router = TaskRouter(self.predictor)

    def test_best_agent_for_translate(self):
        best_agent = self.router.route_task("translate")
        self.assertEqual(best_agent, "agent-A", "Agent A should be selected due to better performance.")

    def test_no_data_for_unknown_skill(self):
        result = self.router.route_task("unknown_skill")
        self.assertIsNone(result, "Routing should return None for unknown skill with no data.")

    def test_tie_breaking_logic(self):
        # Add same score to another agent to force tie
        self.db.record_task_result("agent-C", "translate", True, 4.1)
        self.db.record_task_result("agent-C", "translate", True, 4.1)
        best_agent = self.router.route_task("translate")
        self.assertIn(best_agent, ["agent-A", "agent-C"], "Either agent-A or agent-C could be best.")

if __name__ == "__main__":
    unittest.main()
