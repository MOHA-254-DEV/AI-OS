import json
import os

class TaskLoader:
    def __init__(self, plugin_directory="plugins/"):
        self.plugin_directory = plugin_directory

    def list_plugins(self):
        return [f for f in os.listdir(self.plugin_directory) if f.endswith(".json")]

    def load_manifest(self, manifest_file):
        full_path = os.path.join(self.plugin_directory, manifest_file)
        if not os.path.exists(full_path):
            raise FileNotFoundError("Manifest not found.")
        with open(full_path, "r") as f:
            return json.load(f)

    def validate_manifest(self, manifest):
        required_keys = ["name", "entry", "runtime", "permissions"]
        for key in required_keys:
            if key not in manifest:
                raise ValueError(f"Missing manifest field: {key}")
        return True

if __name__ == "__main__":
    loader = TaskLoader()
    for plugin in loader.list_plugins():
        print("Found Plugin Manifest:", plugin)
        manifest = loader.load_manifest(plugin)
        print("Validated:", loader.validate_manifest(manifest))
