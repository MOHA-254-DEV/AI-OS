import os
from pathlib import Path

def load_config():
    """
    Load system configuration from environment variables and set defaults.
    Ensures the data and plugins directories exist.
    """
    config = {
        "debug": os.getenv("DEBUG", "false").lower() == "true",
        "host": os.getenv("HOST", "0.0.0.0"),
        "port": int(os.getenv("PORT", 5000)),
        "voice_enabled": os.getenv("VOICE_ENABLED", "true").lower() == "true",
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
        "data_dir": Path("data"),
        "plugins_dir": Path("plugins"),
    }
    try:
        config["data_dir"].mkdir(exist_ok=True)
        config["plugins_dir"].mkdir(exist_ok=True)
    except Exception as e:
        raise RuntimeError(f"Failed to create config directories: {e}")
    return config
