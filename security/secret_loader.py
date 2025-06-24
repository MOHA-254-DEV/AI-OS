import os
from dotenv import dotenv_values
from security.encryption import Encryptor

class SecretLoader:
    def __init__(self, password):
        self.encryptor = Encryptor(password)

    def load_env(self, enc_path="config/secrets.env.enc"):
        decrypted = self.encryptor.decrypt(open(enc_path, "r").read())
        with open(".env.temp", "w") as f:
            f.write(decrypted)

        secrets = dotenv_values(".env.temp")
        for key, val in secrets.items():
            os.environ[key] = val
        os.remove(".env.temp")
        print("[SECRETS] Secure ENV variables loaded.")

if __name__ == "__main__":
    pwd = input("Enter key to decrypt secrets: ")
    loader = SecretLoader(pwd)
    loader.load_env()
