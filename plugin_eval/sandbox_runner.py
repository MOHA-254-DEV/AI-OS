import multiprocessing
import os
import traceback
import time

def restricted_runner(plugin_func, args, timeout=5):
    def wrapper(q, plugin_func, args):
        try:
            result = plugin_func(*args)
            q.put(("success", result))
        except Exception as e:
            q.put(("error", str(e)))

    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=wrapper, args=(q, plugin_func, args))
    p.start()
    p.join(timeout)

    if p.is_alive():
        p.terminate()
        return "timeout", "Execution timed out"
    
    if not q.empty():
        return q.get()
    return "error", "No result returned"

class SandboxRunner:
    def __init__(self, timeout=5):
        self.timeout = timeout

    def run_plugin(self, plugin_module, entry_function='run', args=[]):
        try:
            func = getattr(plugin_module, entry_function)
            status, result = restricted_runner(func, args, timeout=self.timeout)
            return {"status": status, "result": result}
        except Exception as e:
            return {"status": "load_error", "result": str(e)}
