from cryptography.fernet import Fernet
import os

KEY_FILE = "secure/secret.key"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)

def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, "rb") as f:
        return f.read()

def encrypt_data(data: str) -> bytes:
    f = Fernet(load_key())
    return f.encrypt(data.encode())

def decrypt_data(token: bytes) -> str:
    f = Fernet(load_key())
    return f.decrypt(token).decode()
