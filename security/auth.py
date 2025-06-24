import uuid
import time
from security.encryption import SecureStore

class AuthManager:
    def __init__(self):
        self.store = SecureStore()
        try:
            self.users = self.store.load_encrypted()
        except:
            self.users = {}
            self.store.save_encrypted(self.users)

    def create_user(self, username, role="basic"):
        token = str(uuid.uuid4())
        self.users[username] = {
            "token": token,
            "role": role,
            "created_at": time.time()
        }
        self.store.save_encrypted(self.users)
        return {"username": username, "token": token, "role": role}

    def validate_token(self, token):
        for user, data in self.users.items():
            if data["token"] == token:
                return {"username": user, "role": data["role"]}
        return None

    def require_role(self, token, required_role):
        user = self.validate_token(token)
        if not user:
            return False
        roles = ["guest", "basic", "pro", "admin"]
        return roles.index(user["role"]) >= roles.index(required_role)

    def get_user_info(self, token):
        return self.validate_token(token)
