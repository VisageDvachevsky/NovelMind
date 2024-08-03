import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from LogSystem.LoggerSystem import Logger

logger = Logger(use_json=True)
log_class = logger.log_class()

@log_class
class AdvancedEncryptor:
    """
    A class to handle encryption and decryption of data using AES encryption.
    """

    def __init__(self, key_file: str = None, salt_file: str = None) -> None:
        """
        Initialize the AdvancedEncryptor with specified key and salt files.

        :param key_file: The file path to store the encryption key.
        :param salt_file: The file path to store the salt.
        """
        self.key_file = key_file or 'master_key.key'
        self.salt_file = salt_file or 'salt.key'
        self.master_key = self._load_or_generate_key(self.key_file)
        self.salt = self._load_or_generate_key(self.salt_file)

    def _load_or_generate_key(self, file_path: str) -> bytes:
        """
        Load an existing key from the file path or generate a new key if the file does not exist.

        :param file_path: The file path to load or generate the key.
        :return: The key as bytes.
        """
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                return f.read()
        else:
            key = os.urandom(32)  # 256-bit key
            with open(file_path, 'wb') as f:
                f.write(key)
            return key

    def _derive_key(self, password: str) -> bytes:
        """
        Derive a cryptographic key from a password using PBKDF2 HMAC.

        :param password: The password to derive the key from.
        :return: The derived key as bytes.
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(password.encode())

    def encrypt(self, data: bytes, password: str) -> bytes:
        """
        Encrypt the provided data using the derived key from the password.

        :param data: The data to encrypt.
        :param password: The password to derive the encryption key.
        :return: The encrypted data as bytes.
        """
        key = self._derive_key(password)
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(data) + encryptor.finalize()
        return base64.urlsafe_b64encode(iv + encrypted_data)

    def decrypt(self, encrypted_data: bytes, password: str) -> bytes:
        """
        Decrypt the provided encrypted data using the derived key from the password.

        :param encrypted_data: The encrypted data to decrypt.
        :param password: The password to derive the decryption key.
        :return: The decrypted data as bytes.
        """
        key = self._derive_key(password)
        decoded_data = base64.urlsafe_b64decode(encrypted_data)
        iv = decoded_data[:16]
        ciphertext = decoded_data[16:]
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()
