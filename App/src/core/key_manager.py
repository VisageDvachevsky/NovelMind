import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode

class KeyManager:
    def __init__(self, password: str, salt: bytes = None):
        self.backend = default_backend()
        self.salt = salt if salt else os.urandom(16)
        self.key = self._derive_key(password)

    def _derive_key(self, password: str) -> bytes:
        """Derives a key from the password using PBKDF2."""
        kdf = PBKDF2HMAC(
            algorithm=SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=self.backend
        )
        key = kdf.derive(password.encode())
        return urlsafe_b64encode(key)

    def get_key(self) -> bytes:
        """Returns the derived encryption key."""
        return self.key