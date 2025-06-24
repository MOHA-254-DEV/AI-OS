# config.py - placeholder
import os
import json
from pathlib import Path

def load_config():
    """Load system configuration"""
    config = {
        "debug": os.getenv("DEBUG", "false").lower() == "true",
        "host": os.getenv("HOST", "0.0.0.0"),
        "port": int(os.getenv("PORT", 5000)),
        "voice_enabled": os.getenv("VOICE_ENABLED", "true").lower() == "true",
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
        "data_dir": Path("data"),
        "plugins_dir": Path("plugins"),
    }
    
    # Ensure directories exist
    config["data_dir"].mkdir(exist_ok=True)
    config["plugins_dir"].mkdir(exist_ok=True)
    
    return config
