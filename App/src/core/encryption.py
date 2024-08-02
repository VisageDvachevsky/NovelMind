import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64

class AdvancedEncryptor:
    def __init__(self, key_file='master_key.key', salt_file='salt.key'):
        self.key_file = key_file
        self.salt_file = salt_file
        self.master_key = self._load_or_generate_key(self.key_file)
        self.salt = self._load_or_generate_key(self.salt_file)

    def _load_or_generate_key(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                return f.read()
        else:
            key = os.urandom(32)  # 256-bit key
            with open(file_path, 'wb') as f:
                f.write(key)
            return key

    def _derive_key(self, password):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(password.encode())

    def encrypt(self, data, password):
        key = self._derive_key(password)
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(data) + encryptor.finalize()
        return base64.urlsafe_b64encode(iv + encrypted_data)

    def decrypt(self, encrypted_data, password):
        key = self._derive_key(password)
        decoded_data = base64.urlsafe_b64decode(encrypted_data)
        iv = decoded_data[:16]
        ciphertext = decoded_data[16:]
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()