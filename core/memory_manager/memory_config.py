import json
import os

DEFAULT_CONFIG = {
    "short_term_ttl": 3600,
    "long_term_storage": "long_term_mem.json",
    "max_token_length": 1000
}

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "memory_config.json")

def load_config():
    if not os.path.exists(CONFIG_PATH):
        return DEFAULT_CONFIG
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except Exception:
        return DEFAULT_CONFIG
