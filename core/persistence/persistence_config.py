# File: core/persistence/persistence_config.py

import os

# Ensure the state directory exists
STATE_DIR = "./data/agent_state"
os.makedirs(STATE_DIR, exist_ok=True)

# Persistence configuration used across persistence modules
CONFIG = {
    "max_retries": 5,
    "retry_backoff": [2, 5, 10, 20, 40],  # Seconds between retries
    "state_dir": STATE_DIR
}
