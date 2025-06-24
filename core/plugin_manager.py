import importlib.util
import os
from utils.logger import logger

class PluginManager:
    def __init__(self, plugin_dir="plugins"):
        self.plugin_dir = plugin_dir
        self.plugins = {}

    def load_plugins(self):
        logger.info(f"🔌 Loading plugins from '{self.plugin_dir}'...")
        if not os.path.exists(self.plugin_dir):
            logger.warning(f"⚠️ Plugin directory '{self.plugin_dir}' does not exist.")
            return

        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                path = os.path.join(self.plugin_dir, filename)

                try:
                    spec = importlib.util.spec_from_file_location(module_name, path)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)

                    if hasattr(mod, "register"):
                        self.plugins[module_name] = mod.register()
                        logger.info(f"✅ Plugin loaded: {module_name}")
                    else:
                        logger.warning(f"⚠️ No 'register()' function in plugin '{module_name}'")
                except Exception as e:
                    logger.error(f"❌ Failed to load plugin '{module_name}': {e}")

    def get_plugin(self, name):
        return self.plugins.get(name)

    def list_plugins(self):
        return list(self.plugins.keys())
