import json
import os

class AdminReviewPanel:
    def __init__(self, registry_path='plugin_store/plugin_registry.json'):
        self.registry_path = registry_path
        self._load_registry()

    def _load_registry(self):
        with open(self.registry_path, 'r') as f:
            self.registry = json.load(f)

    def _save_registry(self):
        with open(self.registry_path, 'w') as f:
            json.dump(self.registry, f, indent=2)

    def list_pending_plugins(self):
        return [p for p in self.registry["plugins"] if not p["approved"]]

    def approve_plugin(self, plugin_id, trust_score=100.0):
        for plugin in self.registry["plugins"]:
            if plugin["id"] == plugin_id:
                plugin["approved"] = True
                plugin["trust_score"] = trust_score
                self._save_registry()
                print(f"✅ Approved plugin: {plugin['name']}")
                return
        print("❌ Plugin ID not found.")

    def reject_plugin(self, plugin_id):
        for i, plugin in enumerate(self.registry["plugins"]):
            if plugin["id"] == plugin_id:
                del self.registry["plugins"][i]
                self._save_registry()
                print("❌ Rejected plugin.")
                return
        print("❌ Plugin ID not found.")
