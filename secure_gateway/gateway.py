from secure_gateway.token_manager import TokenManager
from secure_gateway.access_control import AccessControl

class SecureGateway:
    def __init__(self, secret="ai_os_secure_key"):
        self.tm = TokenManager(secret)
        self.ac = AccessControl()

    def handle_request(self, token, permission_required):
        valid, payload_or_error = self.tm.verify_token(token)
        if not valid:
            return {"status": "error", "message": payload_or_error}

        role = payload_or_error.get("role")
        if not self.ac.check_permission(role, permission_required):
            return {"status": "forbidden", "message": "Permission denied"}

        return {"status": "ok", "user": payload_or_error}

if __name__ == "__main__":
    gw = SecureGateway()
    token = gw.tm.generate_token({"uid": 10, "role": "user"}, expires_in=3600)
    print("Testing user:", gw.handle_request(token, "can_generate_report"))
    print("Testing deploy:", gw.handle_request(token, "can_deploy"))
