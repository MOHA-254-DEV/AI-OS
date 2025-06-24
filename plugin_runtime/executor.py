import os
from plugin_runtime.runtimes.python_runtime import PythonRuntime
from plugin_runtime.runtimes.node_runtime import NodeRuntime
from plugin_runtime.runtimes.bash_runtime import BashRuntime

class PluginExecutor:
    def __init__(self):
        self.runtimes = {
            "python": PythonRuntime(),
            "node": NodeRuntime(),
            "bash": BashRuntime()
        }

    def execute(self, plugin_path, runtime="python", args=None):
        if runtime not in self.runtimes:
            raise ValueError(f"Unsupported runtime: {runtime}")
        if not os.path.exists(plugin_path):
            raise FileNotFoundError("Plugin path does not exist")
        return self.runtimes[runtime].run(plugin_path, args or {})

if __name__ == "__main__":
    executor = PluginExecutor()
    # Test Python plugin
    result = executor.execute("plugins/sample_plugin.py", "python", {"input": "Hello World"})
    print("Result:", result)
