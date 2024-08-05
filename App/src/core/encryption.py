import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
from LogSystem.LoggerSystem import Logger
import secrets

logger = Logger(use_json=True)
log_class = logger.log_class()

@log_class
class AdvancedEncryptor:
    def __init__(self, key_file: str = None, salt_file: str = None, rsa_key_file: str = None):
        self.key_file = key_file or 'master_key.key'
        self.salt_file = salt_file or 'salt.key'
        self.rsa_key_file = rsa_key_file or 'rsa_key.pem'
        self.master_key = self._load_or_generate_key(self.key_file)
        self.salt = self._load_or_generate_key(self.salt_file)
        self.rsa_key = self._load_or_generate_rsa_key()

    def _load_or_generate_key(self, file_path: str) -> bytes:
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                return f.read()
        else:
            key = secrets.token_bytes(32)
            with open(file_path, 'wb') as f:
                f.write(key)
            return key

    def _load_or_generate_rsa_key(self):
        if os.path.exists(self.rsa_key_file):
            with open(self.rsa_key_file, 'rb') as f:
                return serialization.load_pem_private_key(
                    f.read(),
                    password=None,
                    backend=default_backend()
                )
        else:
            key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=4096,
                backend=default_backend()
            )
            pem = key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            with open(self.rsa_key_file, 'wb') as f:
                f.write(pem)
            return key

    def _derive_key(self, password: str) -> bytes:
        kdf = Scrypt(
            salt=self.salt,
            length=32,
            n=2**16,
            r=8,
            p=1,
            backend=default_backend()
        )
        return kdf.derive(password.encode())

    def encrypt(self, data: bytes, password: str) -> bytes:
        try:
            symmetric_key = self._derive_key(password)
            chacha = ChaCha20Poly1305(symmetric_key)
            nonce = secrets.token_bytes(12)
            encrypted_data = chacha.encrypt(nonce, data, None)

            public_key = self.rsa_key.public_key()
            encrypted_symmetric_key = public_key.encrypt(
                symmetric_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            return base64.urlsafe_b64encode(nonce + encrypted_symmetric_key + encrypted_data)
        except Exception as e:
            logger.error(f"Encryption failed: {str(e)}")
            raise

    def decrypt(self, encrypted_data: bytes, password: str) -> bytes:
        try:
            decoded_data = base64.urlsafe_b64decode(encrypted_data)
            nonce = decoded_data[:12]
            encrypted_symmetric_key = decoded_data[12:524]
            ciphertext = decoded_data[524:]

            symmetric_key = self.rsa_key.decrypt(
                encrypted_symmetric_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            chacha = ChaCha20Poly1305(symmetric_key)
            decrypted_data = chacha.decrypt(nonce, ciphertext, None)

            derived_key = self._derive_key(password)
            if derived_key != symmetric_key:
                raise ValueError("Invalid password")

            return decrypted_data
        except Exception as e:
            logger.error(f"Decryption failed: {str(e)}")
            raise

    def rotate_keys(self):
        self.master_key = secrets.token_bytes(32)
        with open(self.key_file, 'wb') as f:
            f.write(self.master_key)
        
        self.salt = secrets.token_bytes(16)
        with open(self.salt_file, 'wb') as f:
            f.write(self.salt)
        
        self.rsa_key = self._load_or_generate_rsa_key()

    def export_public_key(self) -> bytes:
        return self.rsa_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )