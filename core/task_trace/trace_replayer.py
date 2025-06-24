import time
from typing import Callable, Optional

class TraceReplayer:
    def __init__(self, storage):
        self.storage = storage

    def replay_trace(self, trace_id: str, on_step: Optional[Callable[[dict], None]] = None, simulate_delay: bool = False):
        trace = self.storage.get_trace_by_id(trace_id)
        if not trace:
            raise ValueError(f"❌ Trace ID {trace_id} not found.")

        # Optional hook for GUI or event system
        if on_step:
            on_step(trace)

        print(f"🔁 Replaying Task Trace ID: {trace_id}")
        print(f"🧠 Agent:     {trace.get('agent_id', 'unknown')}")
        print(f"📝 Task:      {trace.get('task', 'unknown')}")
        print(f"⚙️  Action:    {trace.get('action', 'N/A')}")
        print(f"✅ Result:    {trace.get('result', 'N/A')}")
        print(f"📦 Metadata:  {trace.get('metadata', {})}")
        print(f"🕒 Timestamp: {trace.get('timestamp', 'N/A')}")

        if simulate_delay:
            print("⏳ Simulating task replay delay...")
            time.sleep(1)  # Delay to simulate real-time replay

        print(f"✅ Trace {trace_id} replay complete.\n")
