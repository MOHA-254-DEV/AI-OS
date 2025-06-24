import os
from dotenv import load_dotenv

# Load variables from .env file if available
load_dotenv()

def get_env_variable(key: str, default=None, required: bool = False, cast: callable = None):
    """
    Fetches an environment variable with optional type casting and fallback default.
    
    Args:
        key (str): Environment variable key
        default (Any): Default value if variable is not found
        required (bool): If True, throws error when variable is missing
        cast (callable): Function to cast the variable type, e.g., bool, int

    Returns:
        Any: Value of the environment variable
    """
    value = os.getenv(key, default)
    if value is None and required:
        raise ValueError(f"⚠️ Environment variable '{key}' is missing or empty.")

    if cast and value is not None:
        try:
            return cast(value)
        except Exception as e:
            raise ValueError(f"⚠️ Failed to cast environment variable '{key}': {e}")
    return value

# Centralized settings dictionary
SETTINGS = {
    "api_token": get_env_variable("API_TOKEN", "secure-token-123", required=True),
    "voice_enabled": get_env_variable("VOICE_ENABLED", "True", cast=lambda v: v.lower() == "true"),
    "debug_mode": get_env_variable("DEBUG_MODE", "false", cast=lambda v: v.lower() == "true"),
    "env": get_env_variable("ENV", "development")
}

# Example usage for CLI/test/debug
if __name__ == "__main__":
    masked_token = f"{SETTINGS['api_token'][:4]}...{SETTINGS['api_token'][-4:]}"
    print(f"API Token: {masked_token}")
    print(f"Voice Enabled: {SETTINGS['voice_enabled']}")
    print(f"Debug Mode: {SETTINGS['debug_mode']}")
    print(f"Environment: {SETTINGS['env']}")
