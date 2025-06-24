# File: /tests/test_persistence.py

import unittest
import os
import json
from core.persistence.state_manager import StateManager
from core.persistence.retry_handler import RetryHandler

class TestPersistence(unittest.TestCase):
    def setUp(self):
        self.agent_id = "agent-test"
        self.state_file = f"core/persistence/states/{self.agent_id}_state.json"
        self.manager = StateManager(self.agent_id)

    def tearDown(self):
        if os.path.exists(self.state_file):
            os.remove(self.state_file)

    def test_state_saving_and_loading(self):
        """
        Test saving and loading agent state.
        """
        state = {"step": 5, "context": "some data", "status": "running"}
        self.manager.save_state(state)
        loaded = self.manager.load_state()
        self.assertEqual(state, loaded)

    def test_state_deletion(self):
        """
        Ensure that deleting state removes the file.
        """
        self.manager.save_state({"delete_test": True})
        self.manager.delete_state()
        self.assertFalse(os.path.exists(self.state_file))

    def test_retry_mechanism_success_on_retry(self):
        """
        Test that RetryHandler retries on failure and eventually succeeds.
        """
        handler = RetryHandler()
        counter = {"attempts": 0}

        def flaky_function():
            counter["attempts"] += 1
            if counter["attempts"] < 3:
                raise ValueError("Fail until 3rd try")
            return "Success"

        result = handler.retry("task-id-1", flaky_function)
        self.assertEqual(result, "Success")
        self.assertEqual(counter["attempts"], 3)

    def test_retry_mechanism_exceeds_max_attempts(self):
        """
        Test that RetryHandler raises after exhausting retries.
        """
        handler = RetryHandler(max_attempts=2)
        def always_fail():
            raise RuntimeError("Always fails")

        with self.assertRaises(RuntimeError):
            handler.retry("task-id-2", always_fail)

if __name__ == '__main__':
    unittest.main()
