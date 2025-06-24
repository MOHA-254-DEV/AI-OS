import importlib.util
import os
from plugins.plugin_utils import PluginUtils

class PluginLoader:
    def __init__(self, plugin_dir="plugins/user_plugins"):
        self.plugin_dir = plugin_dir
        self.utils = PluginUtils()
        os.makedirs(plugin_dir, exist_ok=True)

    def list_plugins(self):
        return [f for f in os.listdir(self.plugin_dir) if f.endswith(".py")]

    def load_plugin(self, name: str):
        plugin_path = os.path.join(self.plugin_dir, name)
        if not os.path.exists(plugin_path):
            raise FileNotFoundError(f"Plugin not found: {plugin_path}")

        audit = self.utils.audit_plugin(plugin_path)
        if audit:
            raise PermissionError("Plugin failed security audit:\n" + "\n".join(audit))

        spec = importlib.util.spec_from_file_location(name[:-3], plugin_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

if __name__ == "__main__":
    loader = PluginLoader()
    print("Available plugins:", loader.list_plugins())
    mod = loader.load_plugin("example_plugin.py")
    mod.run()
