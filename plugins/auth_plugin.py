from security.auth import AuthManager
from utils.logger import log_task

auth = AuthManager()

async def create_user(args):
    if len(args) < 2:
        return {"error": "Usage: create_user <username> <role>"}
    username, role = args[0], args[1]
    result = auth.create_user(username, role)
    log_task("create_user", "registered", str(result))
    return result

async def validate(args):
    if not args:
        return {"error": "Usage: validate <token>"}
    token = args[0]
    result = auth.validate_token(token)
    return result or {"error": "Invalid token"}

async def get_role(args):
    if not args:
        return {"error": "Usage: get_role <token>"}
    token = args[0]
    result = auth.get_user_info(token)
    return result or {"error": "Invalid or expired"}

def register():
    return {
        "create_user": create_user,
        "validate": validate,
        "get_role": get_role
    }

