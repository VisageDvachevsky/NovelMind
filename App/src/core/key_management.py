import os
from cryptography.fernet import Fernet

class KeyManager:
    def __init__(self, key_file: str):
        self.key_file = key_file
        if not os.path.exists(self.key_file):
            self._generate_new_key()

    def _generate_new_key(self):
        key = Fernet.generate_key()
        with open(self.key_file, 'wb') as file:
            file.write(key)

    def get_key(self) -> bytes:
        with open(self.key_file, 'rb') as file:
            return file.read()

    def rotate_key(self):
        self._generate_new_key()
