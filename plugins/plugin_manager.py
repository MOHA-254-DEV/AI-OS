# plugin_manager.py - placeholder
import importlib.util
import os
from utils.logger import logger

class PluginManager:
    def __init__(self, plugin_dir="plugins"):
        self.plugin_dir = plugin_dir
        self.plugins = {}

    def load_plugins(self):
        logger.info(f"Loading plugins from {self.plugin_dir}")
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py"):
                module_name = filename[:-3]
                path = os.path.join(self.plugin_dir, filename)
                spec = importlib.util.spec_from_file_location(module_name, path)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                if hasattr(mod, "register"):
                    self.plugins[module_name] = mod.register()
                    logger.info(f"Plugin loaded: {module_name}")
                    if hasattr(mod, "register"):
    task_map = mod.register()
    for task_name, handler in task_map.items():
        self.plugins[task_name] = handler

