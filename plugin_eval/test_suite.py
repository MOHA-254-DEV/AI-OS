import importlib.util
import os

class PluginTestSuite:
    def __init__(self, sandbox_runner):
        self.sandbox_runner = sandbox_runner

    def load_plugin(self, path):
        try:
            spec = importlib.util.spec_from_file_location("plugin", path)
            plugin = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(plugin)
            return plugin
        except Exception as e:
            return None, str(e)

    def test_plugin(self, plugin_path):
        plugin, err = self.load_plugin(plugin_path)
        if plugin is None:
            return {"status": "load_failed", "error": err}
        
        tests = [
            {"func": "run", "args": []},
            {"func": "run", "args": ["sample input"]}
        ]

        results = []
        for test in tests:
            result = self.sandbox_runner.run_plugin(plugin, entry_function=test["func"], args=test["args"])
            results.append(result)
        
        return results
