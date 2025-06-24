# plugin_sandbox/sandbox.py

import multiprocessing
import time

def run_code_snippet(code: str, input_data: dict = {}, timeout: int = 3):
    def target(queue, code, input_data):
        try:
            local_vars = {"input_data": input_data}
            exec(code, {}, local_vars)
            queue.put(local_vars.get("result", "No result."))
        except Exception as e:
            queue.put(f"Error: {e}")

    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=target, args=(queue, code, input_data))
    process.start()
    process.join(timeout)

    if process.is_alive():
        process.terminate()
        return "Execution timed out."

    return queue.get() if not queue.empty() else "No output."

