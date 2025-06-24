import importlib.util
import os

class PluginSandbox:
    def __init__(self, allowed_paths=None):
        self.allowed_paths = allowed_paths or ["plugins/", "tasks/"]

    def is_safe(self, path):
        return any(path.startswith(ap) for ap in self.allowed_paths)

    def load_plugin(self, path):
        if not self.is_safe(path):
            raise PermissionError("Access denied to unsafe plugin path.")
        if not os.path.exists(path):
            raise FileNotFoundError("Plugin not found.")
        
        spec = importlib.util.spec_from_file_location("plugin", path)
        plugin = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(plugin)
        return plugin

if __name__ == "__main__":
    sb = PluginSandbox()
    try:
        plugin = sb.load_plugin("plugins/sample_plugin.py")
        plugin.run()
    except Exception as e:
        print("[SANDBOX] Error:", e)
