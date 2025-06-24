# plugin_sandbox/resource_limiter.py

import resource
import signal
import os

class ResourceLimiter:
    def __init__(self, memory_mb=50, cpu_seconds=2):
        self.memory_mb = memory_mb
        self.cpu_seconds = cpu_seconds

    def apply_limits(self):
        soft, hard = resource.getrlimit(resource.RLIMIT_AS)
        resource.setrlimit(resource.RLIMIT_AS, (self.memory_mb * 1024 * 1024, hard))
        
        signal.signal(signal.SIGXCPU, self._cpu_timeout)
        resource.setrlimit(resource.RLIMIT_CPU, (self.cpu_seconds, self.cpu_seconds + 1))

    def _cpu_timeout(self, signum, frame):
        print("CPU time limit exceeded")
        os._exit(1)
