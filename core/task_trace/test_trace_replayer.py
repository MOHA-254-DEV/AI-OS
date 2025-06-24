from .execution_logger import ExecutionLogger
from .trace_replayer import TraceReplayer
from .trace_storage import TraceStorage


def test_trace_logging_and_replay():
    logger = ExecutionLogger()
    
    # Step 1: Log a trace
    trace_id = logger.log(
        agent_id='agent-test-1',
        task_name='write_code',
        action='generate_function',
        result='success',
        metadata={'file': 'main.py', 'lines': 42}
    )

    print(f"[TEST] Logged trace_id: {trace_id}")
    
    # Step 2: Access underlying storage
    storage = logger.storage
    
    # Step 3: Check if trace exists
    trace = storage.get_trace(trace_id)
    assert trace is not None, f"[ERROR] Trace ID {trace_id} not found in storage"
    print(f"[TEST] Retrieved trace: {trace}")
    
    # Step 4: Replay trace
    replayer = TraceReplayer(storage)
    replayer.replay_trace(trace_id)

    print("[TEST] Trace replay successful ✅")


if __name__ == '__main__':
    test_trace_logging_and_replay()
