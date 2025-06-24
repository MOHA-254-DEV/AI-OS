import json
import hashlib

class TrustScorecard:
    def __init__(self, database_path="plugin_eval/trusted_plugins.json"):
        self.database_path = database_path
        self._load_db()

    def _load_db(self):
        if os.path.exists(self.database_path):
            with open(self.database_path, 'r') as f:
                self.db = json.load(f)
        else:
            self.db = {}

    def _save_db(self):
        with open(self.database_path, 'w') as f:
            json.dump(self.db, f, indent=2)

    def _hash_plugin(self, path):
        with open(path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()

    def score_plugin(self, test_results, plugin_path):
        total = len(test_results)
        success = sum(1 for r in test_results if r['status'] == "success")
        fail = total - success

        trust_score = round((success / total) * 100, 2)

        plugin_id = self._hash_plugin(plugin_path)
        self.db[plugin_id] = {
            "score": trust_score,
            "tests_run": total,
            "success": success,
            "fail": fail,
            "path": plugin_path
        }

        self._save_db()
        return trust_score, plugin_id

    def get_plugin_score(self, plugin_path):
        plugin_id = self._hash_plugin(plugin_path)
        return self.db.get(plugin_id, None)
from plugin_eval.sandbox_runner import SandboxRunner
from plugin_eval.test_suite import PluginTestSuite
from plugin_eval.trust_scorecard import TrustScorecard

def evaluate_plugin(path):
    sandbox = SandboxRunner(timeout=6)
    tester = PluginTestSuite(sandbox)
    scorecard = TrustScorecard()

    test_results = tester.test_plugin(path)
    score, pid = scorecard.score_plugin(test_results, path)

    print(f"[✓] Plugin ID: {pid}")
    print(f"[✓] Trust Score: {score}%")
    if score >= 80:
        print("[✓] Plugin Approved")
    else:
        print("[✗] Plugin Blocked or Needs Review")
