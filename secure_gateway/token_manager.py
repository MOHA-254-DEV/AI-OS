import hashlib
import hmac
import time
import base64
import secrets
import json

class TokenManager:
    def __init__(self, secret_key="super_secure_default"):
        self.secret_key = secret_key.encode()
        self.token_store = {}  # {token: expiry_ts}

    def generate_token(self, payload: dict, expires_in=3600):
        payload["exp"] = int(time.time()) + expires_in
        payload_bytes = json.dumps(payload).encode()
        signature = hmac.new(self.secret_key, payload_bytes, hashlib.sha256).digest()
        token = base64.urlsafe_b64encode(payload_bytes + b"." + signature).decode()
        self.token_store[token] = payload["exp"]
        return token

    def verify_token(self, token: str):
        try:
            decoded = base64.urlsafe_b64decode(token.encode())
            payload_bytes, signature = decoded.rsplit(b".", 1)
            expected_sig = hmac.new(self.secret_key, payload_bytes, hashlib.sha256).digest()
            if not hmac.compare_digest(signature, expected_sig):
                return False, "Signature mismatch"
            payload = json.loads(payload_bytes)
            if time.time() > payload["exp"]:
                return False, "Token expired"
            return True, payload
        except Exception as e:
            return False, str(e)

    def revoke_token(self, token):
        if token in self.token_store:
            del self.token_store[token]
            return True
        return False

if __name__ == "__main__":
    tm = TokenManager("my_secret")
    token = tm.generate_token({"role": "admin", "uid": 1})
    print("Token:", token)
    valid, result = tm.verify_token(token)
    print("Valid:", valid)
    print("Payload/Error:", result)
