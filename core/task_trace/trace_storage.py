import json
import os
from typing import List, Dict, Optional

class TraceStorage:
    def __init__(self, storage_path: str = None):
        self._traces: List[Dict] = []
        self.storage_path = storage_path
        if storage_path and os.path.exists(storage_path):
            self.load_from_disk()

    def store_trace(self, trace: Dict):
        self._traces.append(trace)
        self._autosave()

    def get_trace_by_agent(self, agent_id: str) -> List[Dict]:
        return [t for t in self._traces if t.get('agent_id') == agent_id]

    def get_trace_by_id(self, trace_id: str) -> Optional[Dict]:
        return next((t for t in self._traces if t.get('trace_id') == trace_id), None)

    def get_all_traces(self) -> List[Dict]:
        return self._traces

    def delete_trace(self, trace_id: str) -> bool:
        original_len = len(self._traces)
        self._traces = [t for t in self._traces if t.get('trace_id') != trace_id]
        if len(self._traces) < original_len:
            self._autosave()
            return True
        return False

    def clear_all(self):
        self._traces = []
        self._autosave()

    def save_to_disk(self):
        if self.storage_path:
            with open(self.storage_path, 'w') as f:
                json.dump(self._traces, f, indent=2)

    def load_from_disk(self):
        if self.storage_path and os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                self._traces = json.load(f)

    def _autosave(self):
        if self.storage_path:
            self.save_to_disk()
