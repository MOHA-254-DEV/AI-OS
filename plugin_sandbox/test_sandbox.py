# plugin_sandbox/test_sandbox.py

from plugin_sandbox.sandbox import run_code_snippet
from plugin_sandbox.rate_limiter import PluginRateLimiter

def test_code_execution():
    code = '''
result = input_data["a"] + input_data["b"]
'''
    result = run_code_snippet(code, {"a": 5, "b": 10})
    print("Execution Result:", result)

def test_rate_limiter():
    limiter = PluginRateLimiter(limit=3, window_sec=10)
    plugin = "sample_plugin"

    for i in range(5):
        allowed = limiter.allow(plugin)
        print(f"Attempt {i+1}: {'Allowed' if allowed else 'Rate Limited'}")

if __name__ == "__main__":
    test_code_execution()
    test_rate_limiter()
