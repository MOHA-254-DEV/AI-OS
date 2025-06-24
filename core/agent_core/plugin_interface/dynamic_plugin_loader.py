import importlib.util
import os
import traceback
import logging

class DynamicPluginLoader:
    def __init__(self, plugin_path, cache_loaded=True, log_level=logging.INFO):
        self.plugin_path = plugin_path
        self.plugins = {}  # plugin_name -> file_path
        self.loaded_plugins = {} if cache_loaded else None

        self.logger = logging.getLogger("PluginLoader")
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.logger.setLevel(log_level)

    def discover_plugins(self):
        """ Scan plugin directory and populate plugin names and paths. """
        self.plugins.clear()
        if not os.path.isdir(self.plugin_path):
            self.logger.warning("Plugin path does not exist: %s", self.plugin_path)
            return []

        for file in os.listdir(self.plugin_path):
            if file.endswith(".py") and not file.startswith("__"):
                module_name = file[:-3]
                self.plugins[module_name] = os.path.join(self.plugin_path, file)

        if not self.plugins:
            self.logger.warning("No plugins found in: %s", self.plugin_path)
        else:
            self.logger.info("Discovered plugins: %s", list(self.plugins.keys()))

        return list(self.plugins.keys())

    def load_plugin(self, plugin_name, force_reload=False):
        """
        Dynamically load or reload a plugin module.
        """
        if plugin_name not in self.plugins:
            self.logger.error("Plugin '%s' not found in discovered plugins.", plugin_name)
            return None

        if self.loaded_plugins is not None:
            if plugin_name in self.loaded_plugins and not force_reload:
                self.logger.info("Returning cached plugin: %s", plugin_name)
                return self.loaded_plugins[plugin_name]
            elif plugin_name in self.loaded_plugins and force_reload:
                self.unload_plugin(plugin_name)

        try:
            spec = importlib.util.spec_from_file_location(plugin_name, self.plugins[plugin_name])
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Optional: Check for a mandatory method or class
            if not hasattr(module, "run"):
                self.logger.warning("Plugin '%s' does not implement 'run()' method.", plugin_name)

            if self.loaded_plugins is not None:
                self.loaded_plugins[plugin_name] = module

            self.logger.info("Plugin '%s' loaded successfully.", plugin_name)
            return module
        except Exception as e:
            self.logger.error("Failed to load plugin '%s': %s", plugin_name, str(e))
            self.logger.debug(traceback.format_exc())
            return None

    def unload_plugin(self, plugin_name):
        """ Remove a plugin from cache. """
        if self.loaded_plugins and plugin_name in self.loaded_plugins:
            del self.loaded_plugins[plugin_name]
            self.logger.info("Unloaded plugin: %s", plugin_name)
        else:
            self.logger.warning("Plugin '%s' is not loaded or not cached.", plugin_name)

    def get_plugin_metadata(self, plugin_name):
        """
        Get plugin metadata like docstring or attributes.
        """
        plugin = self.loaded_plugins.get(plugin_name) if self.loaded_plugins else None
        if plugin:
            return {
                "name": plugin_name,
                "doc": plugin.__doc__,
                "has_run": hasattr(plugin, "run")
            }
        return None
