python -m pip install -r c:/Users/Mohammed/Downloads/ai_os_complete/ai_os/requirements.txt
from pip._vendor.rich.console import Console
console = Console()
with Live(console=console, refresh_per_second=4) as live:
    # Run your show.py program here
    runtime = PythonRuntime()
    result = runtime.run("show.py", {})
    live.update(result)
from pip._vendor.rich.console import Console
console = Console()
with Live(console=console, refresh_per_second=4) as live:
    # Run your show.py program here
    runtime = PythonRuntime()
    result = runtime.run("show.py", {})
    live.update(result)
runtime = PythonRuntime()
result = runtime.run("show.py", {})
print(result)
result = runtime.run("show.py", {})
print(result)

class PythonRuntime:
    def run(self, path, args):
        try:
            globals_dict = {"ARGS": args}
            result = runpy.run_path(path, init_globals=globals_dict)
            return result.get("OUTPUT", "No OUTPUT found.")
        except Exception as e:
            return f"[PYTHON ERROR] {e}"
