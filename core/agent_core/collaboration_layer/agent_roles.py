import os
import json
import logging

# Setup logging
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "agent_roles.log")),
        logging.StreamHandler()
    ]
)

# Default fallback roles
DEFAULT_AGENT_ROLES = {
    "planner": {
        "description": "Break down goals into subtasks",
        "capabilities": ["decompose_task", "assign_tasks"]
    },
    "executor": {
        "description": "Perform assigned tasks",
        "capabilities": ["run_task", "log_progress"]
    },
    "validator": {
        "description": "Review task results",
        "capabilities": ["review", "compare", "validate_output"]
    },
    "communicator": {
        "description": "Summarize and report outcomes",
        "capabilities": ["summarize", "report"]
    }
}

# Optional: load from external config
CONFIG_FILE = "config/agent_roles.json"
AGENT_ROLES = DEFAULT_AGENT_ROLES

if os.path.exists(CONFIG_FILE):
    try:
        with open(CONFIG_FILE, "r") as f:
            AGENT_ROLES = json.load(f)
        logging.info("Custom agent roles loaded from config.")
    except Exception as e:
        logging.warning(f"Failed to load roles from config: {e}. Using defaults.")

def get_role_config(role_name: str) -> dict:
    """
    Retrieve role configuration by name.
    """
    role = AGENT_ROLES.get(role_name)
    if role:
        logging.info(f"Retrieved configuration for role: {role_name}")
        return role
    else:
        logging.error(f"Role '{role_name}' not found.")
        return {}

def list_available_roles() -> dict:
    """
    Lists all available roles and their descriptions.
    """
    return {name: config["description"] for name, config in AGENT_ROLES.items()}

def validate_role(role_name: str) -> bool:
    """
    Check if a role exists.
    """
    exists = role_name in AGENT_ROLES
    logging.info(f"Role '{role_name}' exists: {exists}")
    return exists

# --- Example Usage ---
if __name__ == "__main__":
    selected_role = "planner"
    role_data = get_role_config(selected_role)

    if role_data:
        print(f"Role: {selected_role}")
        print(f"Description: {role_data['description']}")
        print(f"Capabilities: {', '.join(role_data['capabilities'])}")

    print("\nAvailable Roles:")
    for role, desc in list_available_roles().items():
        print(f"{role}: {desc}")
