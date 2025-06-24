from cryptography.fernet import Fernet
import os
import json

class SecureEnv:
    def __init__(self, key_path="security/.enc_key"):
        self.key_path = key_path
        self.key = self.load_key()

    def generate_key(self):
        key = Fernet.generate_key()
        with open(self.key_path, "wb") as f:
            f.write(key)
        return key

    def load_key(self):
        if not os.path.exists(self.key_path):
            return self.generate_key()
        with open(self.key_path, "rb") as f:
            return f.read()

    def encrypt(self, data: str):
        f = Fernet(self.key)
        return f.encrypt(data.encode()).decode()

    def decrypt(self, token: str):
        f = Fernet(self.key)
        return f.decrypt(token.encode()).decode()

    def save_env(self, config: dict, path="security/.env.enc"):
        secure = {k: self.encrypt(v) for k, v in config.items()}
        with open(path, "w") as f:
            json.dump(secure, f)

    def load_env(self, path="security/.env.enc"):
        with open(path, "r") as f:
            enc = json.load(f)
        return {k: self.decrypt(v) for k, v in enc.items()}

if __name__ == "__main__":
    sec = SecureEnv()
    config = {"API_KEY": "topsecret123", "DB_PASS": "securepass"}
    sec.save_env(config)
    print(sec.load_env())
