from cryptography.fernet import Fernet # type: ignore
import hmac
import hashlib

class FileEncryption:
    def __init__(self, key: bytes):
        self.cipher = Fernet(key)

    def encrypt_file(self, file_path: str) -> bytes:
        """Encrypts the file at the given path."""
        with open(file_path, 'rb') as file:
            data = file.read()
        encrypted_data = self.cipher.encrypt(data)
        file_hash = self._generate_hash(encrypted_data)
        return encrypted_data + file_hash

    def decrypt_file(self, encrypted_data: bytes) -> bytes:
        """Decrypts the encrypted data and verifies its integrity."""
        data, file_hash = encrypted_data[:-32], encrypted_data[-32:]
        if not self._verify_hash(data, file_hash):
            raise ValueError("Data integrity check failed.")
        return self.cipher.decrypt(data)

    def _generate_hash(self, data: bytes) -> bytes:
        """Generates an HMAC hash for integrity verification."""
        return hmac.new(self.cipher._signing_key, data, hashlib.sha256).digest()

    def _verify_hash(self, data: bytes, hash: bytes) -> bool:
        """Verifies the integrity of the data using HMAC."""
        return hmac.compare_digest(self._generate_hash(data), hash)