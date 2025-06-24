# agent_manager/plugin_loader.py

import importlib
import os
import sys
import logging
from agent_manager.plugins.plugin_base import PluginBase

def load_plugins(plugin_dir="agent_manager/plugins"):
    """
    Dynamically loads all *_plugin.py files in the specified directory,
    instantiates them, and returns a dictionary of plugin instances.

    :param plugin_dir: Path to the plugins directory
    :return: Dictionary of plugin_name: plugin_instance
    """
    logger = logging.getLogger("PluginLoader")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    sys.path.insert(0, os.getcwd())  # Ensure project root is importable
    plugins = {}

    if not os.path.exists(plugin_dir):
        logger.warning(f"Plugin directory '{plugin_dir}' does not exist.")
        return plugins

    for filename in os.listdir(plugin_dir):
        if filename.endswith("_plugin.py") and filename != "plugin_base.py":
            try:
                module_name = filename[:-3]  # Strip .py
                full_module_path = f"{plugin_dir.replace('/', '.')}.{module_name}".replace(".py", "")

                module = importlib.import_module(full_module_path)

                # Expected class name (e.g., design_plugin.py => DesignPlugin)
                class_name = ''.join([part.capitalize() for part in module_name.split('_')])
                plugin_class = getattr(module, class_name)

                if not issubclass(plugin_class, PluginBase):
                    logger.warning(f"{class_name} does not inherit from PluginBase. Skipping.")
                    continue

                plugins[module_name] = plugin_class()
                logger.info(f"✅ Loaded plugin: {module_name}")

            except Exception as e:
                logger.error(f"❌ Error loading plugin '{filename}': {e}")

    return plugins
