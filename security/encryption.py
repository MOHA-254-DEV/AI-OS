from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import json
import os

class SecureStore:
    def __init__(self, key_path="config/secret.key"):
        self.key_path = key_path
        if not os.path.exists(self.key_path):
            with open(self.key_path, 'wb') as f:
                f.write(get_random_bytes(16))
        with open(self.key_path, 'rb') as f:
            self.key = f.read()

    def encrypt(self, data: dict) -> str:
        json_data = json.dumps(data).encode()
        cipher = AES.new(self.key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(json_data)
        return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

    def decrypt(self, encrypted: str) -> dict:
        raw = base64.b64decode(encrypted.encode())
        nonce = raw[:16]
        tag = raw[16:32]
        ciphertext = raw[32:]
        cipher = AES.new(self.key, AES.MODE_EAX, nonce)
        return json.loads(cipher.decrypt_and_verify(ciphertext, tag).decode())

    def save_encrypted(self, data: dict, filepath="config/users.json"):
        encrypted = self.encrypt(data)
        with open(filepath, "w") as f:
            f.write(encrypted)

    def load_encrypted(self, filepath="config/users.json") -> dict:
        with open(filepath, "r") as f:
            encrypted = f.read()
        return self.decrypt(encrypted)
from cryptography.fernet import Fernet
import base64
import hashlib
import os

class Encryptor:
    def __init__(self, password):
        key = hashlib.sha256(password.encode()).digest()
        self.fernet = Fernet(base64.urlsafe_b64encode(key))

    def encrypt(self, data: str) -> str:
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt(self, data: str) -> str:
        return self.fernet.decrypt(data.encode()).decode()

    def encrypt_file(self, in_file, out_file):
        with open(in_file, "r") as f:
            plaintext = f.read()
        with open(out_file, "w") as f:
            f.write(self.encrypt(plaintext))

    def decrypt_file(self, in_file, out_file):
        with open(in_file, "r") as f:
            ciphertext = f.read()
        with open(out_file, "w") as f:
            f.write(self.decrypt(ciphertext))

if __name__ == "__main__":
    key = input("Enter password for encryption: ")
    e = Encryptor(key)
    e.encrypt_file("config/secrets.env", "config/secrets.env.enc")
    print("[INFO] Encrypted secrets saved.")
