import multiprocessing
import resource
import signal
import sys
import os

def run_with_limits(plugin_func, timeout=5, mem_limit_mb=100):
    def set_limits():
        resource.setrlimit(resource.RLIMIT_AS, (mem_limit_mb * 1024 * 1024, resource.RLIM_INFINITY))
        signal.signal(signal.SIGXCPU, signal.SIG_IGN)

    def worker(queue):
        try:
            set_limits()
            plugin_func()
            queue.put("done")
        except Exception as e:
            queue.put(f"error: {e}")

    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=worker, args=(q,))
    p.start()
    p.join(timeout)

    if p.is_alive():
        print("[SANDBOX] Plugin exceeded runtime or memory limit. Killing...")
        p.terminate()
        return "terminated"
    result = q.get() if not q.empty() else "no response"
    return result

if __name__ == "__main__":
    from plugins.example_plugin import run
    result = run_with_limits(run, 3, 50)
    print("Plugin result:", result)
