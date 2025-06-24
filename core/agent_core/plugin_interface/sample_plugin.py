import logging
from datetime import datetime
from typing import Any, Dict, Union
import time

# Configure logging
logging.basicConfig(
    filename='logs/process_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DataProcessor:
    def __init__(self):
        self.status = "initialized"

    def _validate_input(self, data: Any) -> bool:
        if data is None:
            raise ValueError("Input data cannot be None.")
        if isinstance(data, str) and not data.strip():
            raise ValueError("Input string cannot be empty or whitespace.")
        return True

    def _log_event(self, message: str, level: str = "info") -> None:
        log_func = getattr(logging, level, logging.info)
        log_func(message)

    def _process(self, data: Any) -> str:
        return f"Processed input: {data}. Generated result successfully with high fidelity."

    def run(self, data: Any) -> Dict[str, Union[str, Any]]:
        try:
            self._log_event(f"Received input: {repr(data)}")
            self._validate_input(data)

            start_time = time.perf_counter()
            result = self._process(data)
            elapsed = time.perf_counter() - start_time

            self.status = "success"
            self._log_event(f"Data processed in {elapsed:.4f} seconds.")
            return {
                "status": "success",
                "timestamp": datetime.utcnow().isoformat(),
                "input": data,
                "output": result,
                "duration_sec": round(elapsed, 4)
            }
        except Exception as e:
            self.status = "error"
            self._log_event(f"Error: {str(e)}", level="error")
            return {
                "status": "error",
                "timestamp": datetime.utcnow().isoformat(),
                "input": data,
                "error": str(e)
            }

# Optional: CLI/Testing
if __name__ == "__main__":
    processor = DataProcessor()
    sample_inputs = ["Hello, AI system.", "   ", 42, None]
    for item in sample_inputs:
        print(processor.run(item))
