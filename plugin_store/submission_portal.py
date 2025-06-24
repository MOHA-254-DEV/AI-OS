import json
import hashlib
import shutil
import os

class PluginSubmissionPortal:
    def __init__(self, registry_path='plugin_store/plugin_registry.json'):
        self.registry_path = registry_path
        self._load_registry()

    def _load_registry(self):
        if os.path.exists(self.registry_path):
            with open(self.registry_path, 'r') as f:
                self.registry = json.load(f)
        else:
            self.registry = {"plugins": []}

    def _save_registry(self):
        with open(self.registry_path, 'w') as f:
            json.dump(self.registry, f, indent=2)

    def submit_plugin(self, name, author, filepath, description, price=0):
        plugin_id = hashlib.sha256(f"{name}:{author}".encode()).hexdigest()[:10]
        dest_path = f"plugins/{plugin_id}_{os.path.basename(filepath)}"
        shutil.copy(filepath, dest_path)

        plugin_entry = {
            "id": plugin_id,
            "name": name,
            "author": author,
            "version": "1.0.0",
            "description": description,
            "price": price,
            "rating": 0.0,
            "trust_score": 0.0,
            "approved": False,
            "filepath": dest_path
        }

        self.registry["plugins"].append(plugin_entry)
        self._save_registry()
        print(f"✅ Submitted plugin '{name}' for review.")
