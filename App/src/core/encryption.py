from cryptography.fernet import Fernet
import hashlib

class EncryptionManager:
    def __init__(self, key: bytes): 
        self.cipher = Fernet(key)

    def encrypt(self, data: bytes) -> bytes:
        return self.cipher.encrypt(data)

    def decrypt(self, data: bytes) -> bytes:
        return self.cipher.decrypt(data)

    @staticmethod
    def generate_key() -> bytes:
        return Fernet.generate_key()

    @staticmethod
    def hash_data(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()
